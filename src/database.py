from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, LargeBinary, func, ForeignKey, Boolean
from dotenv import load_dotenv
import datetime
import asyncio
import os


load_dotenv()
database_url = os.getenv("DATABASE_URL")

engine = create_async_engine(database_url, echo=True)

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session


class Base(DeclarativeBase):
    pass


# Таблица пользователей
class UsersModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_name: Mapped[str] = mapped_column(String, nullable=False)
    display_name: Mapped[str] = mapped_column(String, nullable=False)
    profile_pic: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    profile_status_text: Mapped[str] = mapped_column(String, nullable=True)
    profile_status_media: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    profile_status_audio: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    registred_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


# Таблица постов
class PostModel(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    media_file: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    sound_file: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

    watches: Mapped[int] = mapped_column(Integer, nullable=True)
    likes: Mapped[int] = mapped_column(Integer, nullable=True)
    dislikes: Mapped[int] = mapped_column(Integer, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


# Таблицы чатов


class ChatModel(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)  # private or group
    group_pic: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ChatMemberModel(Base):
    __tablename__ = "chat_members"

    chat_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("chats.id"), primary_key=True
    )
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    role: Mapped[str] = mapped_column(String, nullable=False)  # owner, member, admin
    joined: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class MessageModel(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id"))
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    text: Mapped[str] = mapped_column(String, nullable=True)
    file_id: Mapped[int] = mapped_column(Integer, nullable=True)
    reply_to: Mapped[int] = mapped_column(
        Integer, ForeignKey("messages.id"), nullable=True
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_edited: Mapped[bool] = mapped_column(Boolean, nullable=True)


class ChatFileModel(Base):
    __tablename__ = "chat_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    file: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    uploaded_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    uploaded_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    # Запуск для создания основаной базы данных
    asyncio.run(setup_database())
