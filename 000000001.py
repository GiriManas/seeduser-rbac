async def enqueue_and_wait(model_key: ModelKey, fn: GenerateFn, *args) -> str:
    """
    Put a task in the model queue and await the result. Raises 429 if queue full.
    """
    q = QUEUES[model_key]
    loop = asyncio.get_running_loop()
    future: asyncio.Future = loop.create_future()
    
    try:
        q.put_nowait((fn, args, future))  # non-blocking enqueue
    except asyncio.QueueFull:
        raise HTTPException(status_code=429, detail=f"{model_key} queue full")
    
    return await future