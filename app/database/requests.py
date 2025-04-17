from app.database.models import get_session
from app.database.models import User, Account
from sqlalchemy import select


async def set_user(tg_id: int, username: str, user_role: str):
    async with get_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, username=username, user_role=user_role))
            await session.commit()
            return True
        return False
        
async def get_user(tg_id: int):
    async with get_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user

async def add_account(name, account_id, token, time_check_statistic, user_id):
    print("Добавление аккаунта:", name, account_id, token, time_check_statistic, user_id)
    try:
        async with get_session() as session:
            new_account = Account(
                name=name,
                account_id=account_id,
                token=token,
                time_check_statistic=time_check_statistic,
                user_id=user_id
            )
            session.add(new_account)
            await session.commit()
            print("Аккаунт успешно добавлен")
    except Exception as e:
        print(f"Ошибка при добавлении аккаунта: {e}")

async def get_accounts(user_id: int):
    async with get_session() as session:
        result = await session.execute(select(Account).where(Account.user_id == user_id))
        accounts = result.scalars().all()
        return accounts

async def get_user_id_by_tg_id(tg_id: int):
    async with get_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        return user.id

async def get_account_by_id(account_id: int):
    async with get_session() as session:
        result = await session.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()
        return account.name if account else None

async def get_info_account_by_id(account_id: int):
    async with get_session() as session:
        result = await session.execute(select(Account).where(Account.id == account_id))
        account = result.scalar_one_or_none()
        return account

async def update_account_token(account_id: int, new_token: str):
    async with get_session() as session:
        account = await session.scalar(select(Account).where(Account.id == account_id))
        if account:
            account.token = new_token
            await session.commit()
            return True
        return False
    
async def update_account_time_check_statistic(account_id: int, new_time_check_statistic: int):
    async with get_session() as session:
        account = await session.scalar(select(Account).where(Account.id == account_id))
        if account:
            account.time_check_statistic = new_time_check_statistic
            await session.commit()
            return True
        return False
    
async def delete_account(account_id: int):
    async with get_session() as session:
        account = await session.scalar(select(Account).where(Account.id == account_id))
        if account:
            await session.delete(account)
            await session.commit()
            return True
