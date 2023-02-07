# https://stackoverflow.com/questions/35196974/aiohttp-set-maximum-number-of-requests-per-second
# As a precaution, add a limit to the number of requests can be sent per second.
# As a rule of thumb, use 100 requests per second.
import asyncio
import time

class Limiter:
    def __init__(self, calls_limit: int = 100, period: int = 1):
        self.calls_limit = calls_limit
        self.period = period
        self.semaphore = asyncio.Semaphore(calls_limit)
        self.requests_finish_time = []

    async def sleep(self):
        if len(self.requests_finish_time) >= self.calls_limit:
            sleep_before = self.requests_finish_time.pop(0)
            if sleep_before >= time.monotonic():
                await asyncio.sleep(sleep_before - time.monotonic())

    def __call__(self, func):
        async def wrapper(*args, **kwargs):
            async with self.semaphore:
                await self.sleep()
                res = await func(*args, **kwargs)
                self.requests_finish_time.append(time.monotonic() + self.period)

            return res

        return wrapper