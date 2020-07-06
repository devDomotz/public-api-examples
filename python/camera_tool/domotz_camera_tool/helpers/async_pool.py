__author__ = 'Iacopo Papalini <iacopo@domotz.com>'

import asyncio
import logging

_logger = logging.getLogger(__name__)

MAX_POOL_SIZE = 10


# https://stackoverflow.com/questions/48483348/how-to-limit-concurrency-with-python-asyncio
async def gather_max_parallelism(futures, max_parallelism=MAX_POOL_SIZE):
    max_parallelism = min(max_parallelism, MAX_POOL_SIZE)
    tasks = set()
    results = [None] * len(futures)
    loop = asyncio.get_running_loop()

    async def call_and_store_return(future_, index_):
        _logger.debug("Awaiting future #%s", index_)
        result = await future_
        _logger.debug("Future #%s returned", index_)
        results[index_] = result

    for index, future in enumerate(futures):
        if len(tasks) >= max_parallelism:
            _logger.debug("Max parallelism of %s reached, waiting one future to return", max_parallelism)
            _done, tasks = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            _logger.debug("%s future returned, others can be added", len(_done))
        tasks.add(loop.create_task(call_and_store_return(future, index)))
    if tasks:
        await asyncio.wait(tasks)

    return results
