import time

from fastapi import Request


async def add_process_time_header(request: Request, call_next):
    """Add X-Process-Time header to response showing request processing time.

    Args:
        request: The incoming HTTP request.
        call_next: The next middleware or route handler in the chain.

    Returns:
        Response with X-Process-Time header added.
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response
