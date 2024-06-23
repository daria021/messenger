import aio_pika
import json
from users.exception import ServerError

class UserService:
    RABBITMQ_URL = "amqp://user:password@rabbitmq/"
    REQUEST_QUEUE = "user_check_queue"
    RESPONSE_QUEUE = "user_response_queue"

    @staticmethod
    async def check_user(user_id: int) -> bool:
        connection = await aio_pika.connect_robust(UserService.RABBITMQ_URL)
        channel = await connection.channel()

        request_message = {
            "user_id": user_id
        }

        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(request_message).encode(),
                reply_to=UserService.RESPONSE_QUEUE,
                correlation_id=str(user_id)
            ),
            routing_key=UserService.REQUEST_QUEUE
        )

        await channel.close()
        await connection.close()

        return await UserService._await_response(user_id)

    @staticmethod
    async def _await_response(user_id: int) -> bool:
        connection = await aio_pika.connect_robust(UserService.RABBITMQ_URL)
        channel = await connection.channel()

        response_queue = await channel.declare_queue(UserService.RESPONSE_QUEUE, durable=True)

        async with response_queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    response = json.loads(message.body)
                    if response["user_id"] == user_id:
                        if response["status_code"] == 200:
                            return True
                        elif response["status_code"] == 404:
                            return False
                        else:
                            raise ServerError

        await channel.close()
        await connection.close()
