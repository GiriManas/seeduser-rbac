# ------------------------------
# FASTAPI ENTRYPOINT
# ------------------------------
import os

# IMPORTANT: Set env vars BEFORE importing any HF/torch/evaluate code
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

from fastapi import FastAPI
import pandas as pd

from evaluate import Evaluate
from enums import ComputationMethod, Metric, UseCase, AggregationMethod, ScoringMethod

app = FastAPI()

# Global evaluator (loaded once)
EVALUATOR = None


# ------------------------------
# LOAD MODELS ONCE AT STARTUP
# ------------------------------
@app.on_event("startup")
def init_evaluator():
    global EVALUATOR
    print("\n🔵 Loading Evaluate() once at startup…")

    # Create an empty evaluator shell.
    # We will replace df, placeholder_columns, prompts on each request.
    EVALUATOR = Evaluate(
        df=pd.DataFrame(),
        placeholder_columns={},
        metrics_prompts={},
        agg_method=AggregationMethod.WEIGHTED_AVERAGE,
        scoring_method=ScoringMethod.ONE_TO_FIVE,
        use_case=UseCase.RAG
    )

    print("✅ Evaluate() loaded successfully. Models/tokenizers cached.")


# ------------------------------
# ENDPOINT
# ------------------------------
@app.post("/metrics-evaluate")
def get_score(model_request):
    global EVALUATOR

    # Convert request to DF
    df_go = pd.DataFrame([{
        "utterance": model_request.question,
        "response": model_request.answer,
        "cited_snippet_text": model_request.context
    }])

    # Update evaluator with fresh data only
    EVALUATOR.df = df_go
    EVALUATOR.results = df_go.copy()
    EVALUATOR.placeholder_columns = {
        "question": "utterance",
        "response": "response",
        "cited_text": "cited_snippet_text"
    }
    EVALUATOR.metrics_prompts = {
        Metric.GROUNDEDNESS: (sys_prompt, rag_user_prompt)
    }
    EVALUATOR.use_case = UseCase.RAG
    EVALUATOR.computation_methods = [ComputationMethod.LLM_EVAL]

    print("⚡ Running evaluation...")
    result = EVALUATOR.jury_inference_scoring(jury_size=4)

    # Return results as JSON
    safe_df = result.replace({np.nan: None})
    return safe_df.to_dict(orient="records")
    
    
    
    
    
    
    
    
FIX 2 — Update Evaluate class to remove forking

In your Evaluate file, find:

batch_responses = Parallel(n_jobs=-1)(
    delayed(evaluate_row)(...)
    for row in batch
)

Replace it with this faster version (thread backend):


from joblib import Parallel, delayed, parallel_backend

if len(rows) == 1:
    # best case: no overhead
    responses = [
        evaluate_row(evaluator, self.placeholder_columns, rows[0], server)
    ]
else:
    with parallel_backend("threading", n_jobs=4):
        responses = Parallel()(
            delayed(evaluate_row)(
                evaluator,
                self.placeholder_columns,
                row,
                server
            )
            for row in rows
        )
        


from joblib import Parallel, delayed, parallel_backend

# Thread-optimized execution (no fork)
if len(batch) == 1:
    batch_responses = [
        evaluate_row(
            evaluator,
            self.placeholder_columns,
            batch[0],
            server
        )
    ]
else:
    with parallel_backend("threading", n_jobs=4):
        batch_responses = Parallel()(
            delayed(evaluate_row)(
                evaluator,
                self.placeholder_columns,
                row,
                server
            )
            for row in batch
        )

        




from joblib import Parallel, delayed, parallel_backend

# Thread-optimized execution (no process forking)
if len(batch) == 1:
    batch_responses = [
        transform_response(
            user_prompt=user_prompt,
            response_column=response_column,
            row=batch.iloc[0]
        )
    ]
else:
    with parallel_backend("threading", n_jobs=4):
        batch_responses = Parallel()(
            delayed(transform_response)(
                user_prompt=user_prompt,
                response_column=response_column,
                row=row
            )
            for _, row in batch.iterrows()
        )
        
        
        
        
python - << 'EOF'
from transformers import pipeline
print("Transformers import OK")
EOF


conda activate /commons/users/u763016/girii/testenv_v1
python - << 'EOF'
import transformers
print(transformers.__version__)
EOF


/home/k104630/.local/bin/conda-pack -o /commons/users/k104630/env-setup/jury_api_env_files/testenv_v1-packed.tar.gz











def judge(self, server: int = 1):
    """
    Run all judges (computation_methods) in parallel per row using threads.
    Keeps existing behaviour of writing one score/explanation column per judge.
    """

    from joblib import Parallel, delayed, parallel_backend
    import time

    # Collect all rows once
    rows = [row for _, row in self.df.iterrows()]
    batch_size = 20  # you can keep or adjust this

    for metric, (sys_prompt, user_prompt) in self.metrics_prompts.items():

        # ---- 1) Build evaluator for each judge ONCE ----
        evaluator_by_method = {}
        for computation_method in self.computation_methods:
            if computation_method.value.is_deterministic:
                evaluator = DeterministicMethodEvaluator(
                    metric,
                    computation_method,
                    self.scoring_method
                )
            else:
                evaluator = LLMMethodEvaluator(
                    metric,
                    computation_method,
                    user_prompt,
                    sys_prompt,
                    self.scoring_method
                )
            evaluator_by_method[computation_method] = evaluator

        # Prepare containers: one list of responses per judge
        responses_by_method = {
            method: [] for method in self.computation_methods
        }

        start_time = time.time()
        print(f"Metric: {metric.name}, Judges: "
              f"{[m.name for m in self.computation_methods]}")

        # ---- 2) Process rows in batches ----
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]

            # For each row, run all judges in parallel
            for row in batch:

                def run_for_method(method, evaluator, row_obj):
                    return method, evaluate_row(
                        evaluator,
                        self.placeholder_columns,
                        row_obj,
                        server
                    )

                if len(self.computation_methods) == 1:
                    # Only one judge -> no need for Parallel
                    method = self.computation_methods[0]
                    _, result = run_for_method(
                        method,
                        evaluator_by_method[method],
                        row
                    )
                    responses_by_method[method].append(result)
                else:
                    # Multiple judges -> run all in parallel threads
                    with parallel_backend("threading",
                                          n_jobs=len(self.computation_methods)):
                        results = Parallel()(
                            delayed(run_for_method)(
                                method,
                                evaluator_by_method[method],
                                row
                            )
                            for method in self.computation_methods
                        )

                    # Collect per-judge
                    for method, result in results:
                        responses_by_method[method].append(result)

        # ---- 3) Write results into DataFrame, one column per judge ----
        for computation_method in self.computation_methods:
            result_column_name = metric.name + "_" + computation_method.name
            score_column_name = result_column_name + "_score"
            explanation_column_name = result_column_name + "_explanation"

            method_responses = responses_by_method[computation_method]

            self.results.loc[:, score_column_name] = [
                r.get("score") if isinstance(r, dict) else None
                for r in method_responses
            ]
            self.results.loc[:, explanation_column_name] = [
                r.get("explanation") if isinstance(r, dict) else None
                for r in method_responses
            ]

        end_time = time.time()
        print(
            f"Completed metric {metric.name} with "
            f"{len(self.computation_methods)} judges in "
            f"{end_time - start_time:.2f} seconds"
        )

    return self.results