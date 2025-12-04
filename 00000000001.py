import asyncio
from fastapi import APIRouter, HTTPException
from fastapi.concurrency import run_in_threadpool

router = APIRouter()

@router.post("/evaluate", response_model=dict)
async def get_evaluate_score(model_request: JuryRequest = None):

    if model_request is None:
        raise HTTPException(status_code=400, detail="Empty request")

    log.info("Incoming Request")

    # Select evaluation metric
    if model_request.evaluation_config.upper() in ["RAG", "Q&A"]:
        evaluation_metric = (
            Metric.GROUNDEDNESS if model_request.evaluation_metrics == "GROUNDEDNESS"
            else Metric.COMPLETENESS if model_request.evaluation_metrics == "COMPLETENESS"
            else Metric.RELEVANCE
        )

        async def task():
            return generate_score_response(
                evaluation_config=UseCase.RAG,
                question=model_request.question,
                context=model_request.context,
                answer=model_request.answer,
                evaluation_metric=evaluation_metric
            )

    elif model_request.evaluation_config.upper() == "SUMMARIZATION":
        evaluation_metric = (
            Metric.GROUNDEDNESS if model_request.evaluation_metrics == "GROUNDEDNESS"
            else Metric.COMPLETENESS if model_request.evaluation_metrics == "COMPLETENESS"
            else Metric.RELEVANCE
        )

        async def task():
            return generate_score_response(
                evaluation_config=UseCase.SUMMARIZATION,
                source_document=model_request.source_document,
                generated_summary=model_request.generated_summary,
                evaluation_metric=evaluation_metric
            )
    else:
        raise HTTPException(status_code=400, detail="Bad Request")

    try:
        # 🚀 Offload heavy sync task to threadpool
        # timeout = 120 seconds (2 mins)
        response = await asyncio.wait_for(
            run_in_threadpool(task), timeout=120
        )
        log.info("Response sent successfully")
        return response

    except asyncio.TimeoutError:
        log.error("Timeout occurred while processing request")
        raise HTTPException(
            status_code=504,
            detail="Processing exceeded time limit (2 minutes)"
        )

    except Exception as e:
        log.error(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )