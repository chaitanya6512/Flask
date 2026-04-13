# Running Multiple async Tasks.
# asyncio.gather() - To run multiple async functions concurrently used.

import asyncio

async def task_1():
    await asyncio.sleep(2)
    return "Task 1 Completed"

async def task_2():
    await asyncio.sleep(3)
    return "Task 2 Completed"

async def main():
    results = await asyncio.gather(task_1(), task_2())  # Runs both tasks simulatonously
    print(results)

asyncio.run(main())