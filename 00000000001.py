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