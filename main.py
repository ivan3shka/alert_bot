import asyncio
from gorodufa import main_gorodufa
from nash_dom import main_nashdom


async def main():
    #nashdom = asyncio.create_task(main_nashdom())
    gorodufa = asyncio.create_task(main_gorodufa())

    await asyncio.gather(gorodufa)


if __name__ == "__main__":
    asyncio.run(main())
