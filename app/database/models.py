from sqlalchemy import BigInteger, String, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.engine.url import URL
import os
import contextlib
import asyncio
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()

@contextlib.asynccontextmanager
async def get_session():
    """Создает новую сессию и автоматически закрывает ее после использования"""
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            async with session_factory() as session:
                try:
                    yield session
                    await session.commit()
                except Exception as e:
                    await session.rollback()
                    print(f"Session error: {str(e)}")
                    raise e
                finally:
                    await session.close()
            break
        except SQLAlchemyError as e:
            print(f"Database error (attempt {attempt + 1}/{max_retries}): {str(e)}")
            if attempt == max_retries - 1:
                raise e
            await asyncio.sleep(retry_delay * (attempt + 1))

engine = create_async_engine(url=os.getenv("DB_URL"))
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    user_role: Mapped[str] = mapped_column(String(length=255), nullable=False)
    
    accounts: Mapped[list["Account"]] = relationship("Account", back_populates="user")
    
class Account(Base):
    __tablename__ = "accounts"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    account_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    token: Mapped[str] = mapped_column(String(length=255), nullable=False)
    time_check_statistic: Mapped[int] = mapped_column(Integer, nullable=True)
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship("User", back_populates="accounts")
    
    __table_args__ = (
        CheckConstraint('time_check_statistic IS NULL OR time_check_statistic IN (30, 60)', 
                        name='check_time_check_statistic'),
    )

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
