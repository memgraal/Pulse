from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.sql import func
from dotenv import load_dotenv
import datetime
import asyncio
import os 


load_dotenv()


engine = create_async_engine(os.getenv("DATABASE_URL"))

new_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_session() as session:
        yield session
        
        
class Base(DeclarativeBase):
    pass

        
class UsersModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    date_of_registration: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    

async def setup_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    # Запуск для создания основаной базы данных
    asyncio.run(setup_database())