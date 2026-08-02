import asyncio

from backend.drone.px4_connection import PX4Connection


async def main():

    connection = PX4Connection()

    await connection.connect()


if __name__ == "__main__":

    asyncio.run(main())