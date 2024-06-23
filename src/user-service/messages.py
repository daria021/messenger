import json

import aio_pika

from api.dependencies.repositories import user_repo_context

RABBITMQ_URL = "amqp://user:password@rabbitmq/"
REQUEST_QUEUE = "user_check_queue"
RESPONSE_QUEUE = "user_response_queue"


async def user_request_handler():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()

    request_queue = await channel.declare_queue(REQUEST_QUEUE, durable=True)

    async with request_queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                request = json.loads(message.body)
                user_id = request["user_id"]

                async with user_repo_context() as repo:
                    response = await repo.get(user_id)

                response_message = {
                    "user_id": user_id,
                    "status_code": 200
                }

                await channel.default_exchange.publish(
                    aio_pika.Message(
                        body=json.dumps(response_message).encode(),
                        correlation_id=message.correlation_id
                    ),
                    routing_key=RESPONSE_QUEUE
                )





