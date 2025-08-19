import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import APIRouter, Query, HTTPException
from app.schemas import ModelResponse, ModelLlamaRequest, ModelGemmaRequest
from app.models import LlamaVersionEnum, GemmaVersionEnum
from app.utils import generate_llama_response, generate_gemma_response

router = APIRouter()

# --------------------
# Thread pool + queue
# --------------------
MAX_WORKERS = 4          # number of inference threads
MAX_QUEUE_SIZE = 20      # max queued requests
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)
request_queue = asyncio.Queue(maxsize=MAX_QUEUE_SIZE)


# --------------------
# Worker loop
# --------------------
async def worker():
    loop = asyncio.get_event_loop()
    while True:
        func, args, future = await request_queue.get()
        try:
            result = await loop.run_in_executor(executor, func, *args)
            future.set_result(result)
        except Exception as e:
            future.set_exception(e)
        finally:
            request_queue.task_done()


# --------------------
# Start workers at startup
# --------------------
async def start_workers():
    for _ in range(MAX_WORKERS):
        asyncio.create_task(worker())

# Call this once at app startup (from main.py)
# e.g., app.add_event_handler("startup", start_workers)


# --------------------
# Endpoints
# --------------------
@router.post("/gemma", response_model=ModelResponse)
async def get_gemma_response(
    model_version: GemmaVersionEnum = Query(..., description="Choose a model version"),
    model_request: ModelGemmaRequest = None
):
    if request_queue.full():
        raise HTTPException(status_code=429, detail="Too many requests in queue")

    loop = asyncio.get_event_loop()
    future = loop.create_future()
    await request_queue.put((generate_gemma_response, (model_version, model_request), future))
    result = await future
    return {"message": result}


@router.post("/llama", response_model=ModelResponse)
async def get_llama_response(
    model_version: LlamaVersionEnum = Query(..., description="Choose a model version"),
    model_request: ModelLlamaRequest = None
):
    if request_queue.full():
        raise HTTPException(status_code=429, detail="Too many requests in queue")

    loop = asyncio.get_event_loop()
    future = loop.create_future()
    await request_queue.put((generate_llama_response, (model_version, model_request), future))
    result = await future
    return {"message": result}