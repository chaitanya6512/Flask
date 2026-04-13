# In Python, asynchronous functions are defined using the async def keyword.

import asyncio

async def my_async_function():
    print("Task started")
    await asyncio.sleep(2)
    print("Task completed")

# Running the async function
asyncio.run(my_async_function())
 