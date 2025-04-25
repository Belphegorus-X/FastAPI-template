import asyncio

from apps.faker.src.core.database_session import get_session
from apps.faker.src.generator import Generator
from domain.repositories.chat import ChatEntry
from domain.repositories.messages import MessagesEntry


async def main() -> None:
    async with get_session() as session:
        generator = Generator()

        chat = generator.generate(MessagesEntry)
        chat = await MessagesEntry.insert(
            chat.name,
            chat.chat_type,
            chat.created_at,
            chat.updated_at,
            session,
        )
        geneator.foreign_key_map[MessagesEntry].append(chat.chat_id)


if __name__ == "__main__":
    asyncio.run(main())
