import asyncio
from fastapi.concurrency import run_in_threadpool




try:
    # Offload CPU/blocking work to threadpool & enforce timeout
    result = await asyncio.wait_for(
        run_in_threadpool(lambda: response),
        timeout=120   # 2-minute timeout
    )
    log.info("Response Sent Successfully")
    return result

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