import asyncio

from apps.faker.src.core.database_session import get_session
from apps.faker.src.generator import Generator
from domain.repositories.chat import ChatEntry


async def main() -> None:
    async with get_session() as session:
        generator = Generator()

        chat = generator.generate(ChatEntry)
        chat = await ChatEntry.insert(
            chat.name,
            chat.chat_type,
            chat.created_at,
            chat.updated_at,
            session,
        )
        print(chat.chat_id, chat.chat_type, chat.name, chat.created_at, chat.updated_at)


if __name__ == "__main__":
    asyncio.run(main())
