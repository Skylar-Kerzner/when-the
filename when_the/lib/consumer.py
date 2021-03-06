import asyncio
import aio_pika

async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=loop
    )

    async with connection:
        channel = await connection.channel()

        queue = await channel.declare_queue("queue1", auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

                    if queue.name in message.body.decode():
                        break

if __name__ = "__main__":
    loop = asyncio.get_event_loop()
    coro = main(loop)
    loop.run_until_complete(coro)
    loop.close()