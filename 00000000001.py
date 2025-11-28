def judge(self, server: int = 1):
    """
    Run all judges (self.computation_methods) in parallel per batch of rows,
    using threads (no multiprocessing). Works for single-row and multi-row data.
    """
    import time

    # Collect all rows once
    rows = [row for _, row in self.df.iterrows()]
    batch_size = 20

    for metric, (sys_prompt, user_prompt) in self.metrics_prompts.items():

        start_time = time.time()
        print(
            f"Metric: {metric.name}, Judges: "
            f"{[m.name for m in self.computation_methods]}"
        )

        # For each judge (computation_method), keep a list of responses
        responses_by_method = {m: [] for m in self.computation_methods}

        # Helper: run ONE judge on ONE batch of rows
        def run_method_on_batch(method, batch_rows):
            # Build evaluator for this judge
            if method.value.is_deterministic:
                evaluator = DeterministicMethodEvaluator(
                    metric,
                    method,
                    self.scoring_method,
                )
            else:
                evaluator = LLMMethodEvaluator(
                    metric,
                    method,
                    user_prompt,
                    sys_prompt,
                    self.scoring_method,
                    self.use_case,  # required extra arg in your repo
                )

            local_responses = []
            for row in batch_rows:
                local_responses.append(
                    evaluate_row(
                        evaluator,
                        self.placeholder_columns,
                        row,
                        server,
                    )
                )
            return method, local_responses

        # ---- Process rows in batches ----
        for i in range(0, len(rows), batch_size):
            batch_rows = rows[i : i + batch_size]
            if not batch_rows:
                continue

            # If there is only one judge, no need for Parallel
            if len(self.computation_methods) == 1:
                method = self.computation_methods[0]
                method, batch_resps = run_method_on_batch(method, batch_rows)
                responses_by_method[method].extend(batch_resps)

            else:
                # Run all judges for this batch in parallel threads
                with parallel_backend("threading", n_jobs=len(self.computation_methods)):
                    results = Parallel()(
                        delayed(run_method_on_batch)(method, batch_rows)
                        for method in self.computation_methods
                    )

                # Merge results back
                for method, batch_resps in results:
                    responses_by_method[method].extend(batch_resps)

        # ---- Write results into DataFrame, one pair of columns per judge ----
        for method in self.computation_methods:
            result_column_name = metric.name + "_" + method.name
            score_column_name = result_column_name + "_score"
            explanation_column_name = result_column_name + "_explanation"

            method_responses = responses_by_method[method]

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