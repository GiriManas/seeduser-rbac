# app/routers/LLMServerModels.py

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, Tuple

from fastapi import APIRouter, Query, HTTPException

# ---- your models & enums (unchanged) ----
from app.schemas import (
    ModelResponse,
    ModelMistralRequest, ModelQwenRequest, ModelDeepseekRequest, ModelGemmaRequest, ModelLlamaRequest,
)
from enums import (
    MistralVersionEnum, QwenVersionEnum, DeepseekVersionEnum, GemmaVersionEnum, LlamaVersionEnum,
)
from utils.text_gen_utils import (
    generate_mistral_response, generate_qwen_response, generate_deepseek_response,
    generate_gemma_response, generate_llama_response,
)

log = logging.getLogger(__name__)

router = APIRouter(
    prefix="/llm-pipeline-server",
    tags=["LLM PIPELINE MODELS"],
    responses={404: {"description": "Not found"}},
)

# =========================
# Config (tune per model)
# =========================
MAX_WORKERS_PER_MODEL = 3     # safe start for 32GB V100s
MAX_QUEUE_SIZE_PER_MODEL = 25 # backlog per model

# =========================
# Executors & Queues
# =========================
# Map model key -> executor / queue / generate_fn
ModelKey = str
GenerateFn = Callable[..., str]

EXECUTORS: Dict[ModelKey, ThreadPoolExecutor] = {}
QUEUES: Dict[ModelKey, asyncio.Queue] = {}
GENERATE: Dict[ModelKey, GenerateFn] = {
    "mistral": generate_mistral_response,
    "qwen":    generate_qwen_response,
    "deepseek":generate_deepseek_response,
    "gemma":   generate_gemma_response,
    "llama":   generate_llama_response,
}

# =========================
# Worker
# =========================
async def worker(model_key: ModelKey):
    """
    Pull (fn, args, future) from the queue and execute in that model's thread pool.
    """
    loop = asyncio.get_running_loop()
    queue = QUEUES[model_key]
    executor = EXECUTORS[model_key]

    while True:
        fn, args, future = await queue.get()  # type: ignore[assignment]
        try:
            # run the blocking generation on the executor
            result = await loop.run_in_executor(executor, fn, *args)
            if not future.done():
                future.set_result(result)
        except Exception as e:
            if not future.done():
                future.set_exception(e)
        finally:
            queue.task_done()

# =========================
# Startup / Shutdown hooks
# =========================
@router.on_event("startup")
async def start_workers():
    # one executor & queue per model
    for key in GENERATE.keys():
        EXECUTORS[key] = ThreadPoolExecutor(max_workers=MAX_WORKERS_PER_MODEL, thread_name_prefix=f"{key}-infer")
        QUEUES[key] = asyncio.Queue(maxsize=MAX_QUEUE_SIZE_PER_MODEL)
        # spin up one worker per max_worker (nice balance)
        for _ in range(MAX_WORKERS_PER_MODEL):
            asyncio.create_task(worker(key))
    log.info("Per-model executors & workers started.")

@router.on_event("shutdown")
async def stop_workers():
    for ex in EXECUTORS.values():
        ex.shutdown(wait=False, cancel_futures=True)
    log.info("Executors shut down.")

# =========================
# Helper: enqueue & await
# =========================
async def enqueue_and_wait(model_key: ModelKey, fn: GenerateFn, *args) -> str:
    """
    Put a task in the model queue and await the result. Raises 429 if queue full.
    """
    q = QUEUES[model_key]
    if q.full():
        raise HTTPException(status_code=429, detail=f"{model_key} queue full")

    loop = asyncio.get_running_loop()
    future: asyncio.Future = loop.create_future()
    await q.put((fn, args, future))
    return await future

# =========================
# Endpoints (one per model)
# =========================

@router.post("/mistral", response_model=ModelResponse)
async def mistral_endpoint(
    model_version: MistralVersionEnum = Query(..., description="Choose a model version"),
    model_request: ModelMistralRequest | None = None,
):
    msg = await enqueue_and_wait("mistral", generate_mistral_response, model_version, model_request)
    return {"message": msg}

@router.post("/qwen", response_model=ModelResponse)
async def qwen_endpoint(
    model_version: QwenVersionEnum = Query(..., description="Choose a model version"),
    model_request: ModelQwenRequest | None = None,
):
    msg = await enqueue_and_wait("qwen", generate_qwen_response, model_version, model_request)
    return {"message": msg}

@router.post("/deepseek", response_model=ModelResponse)
async def deepseek_endpoint(
    model_version: DeepseekVersionEnum = Query(..., description="Choose a model version"),
    model_request: ModelDeepseekRequest | None = None,
):
    msg = await enqueue_and_wait("deepseek", generate_deepseek_response, model_version, model_request)
    return {"message": msg}

@router.post("/gemma", response_model=ModelResponse)
async def gemma_endpoint(
    model_version: GemmaVersionEnum = Query(..., description="Choose a model version"),
    model_request: ModelGemmaRequest | None = None,
):
    msg = await enqueue_and_wait("gemma", generate_gemma_response, model_version, model_request)
    return {"message": msg}

@router.post("/llama", response_model=ModelResponse)
async def llama_endpoint(
    model_version: LlamaVersionEnum = Query(..., description="Choose a model version"),
    model_request: ModelLlamaRequest | None = None,
):
    msg = await enqueue_and_wait("llama", generate_llama_response, model_version, model_request)
    return {"message": msg}