import aiosqlite
import datetime
import asyncio
from loguru import logger

async def create_tables():
    async with aiosqlite.connect("expenses.db") as db:
        await db.execute("CREATE TABLE IF NOT EXISTS Users (userid INTEGER PRIMARY KEY, tg_id TEXT UNIQUE, amount_left REAL)")
        await db.execute("CREATE TABLE IF NOT EXISTS Expenses (expenseid INTEGER PRIMARY KEY, tg_id TEXT, date DATE, expense_amount INT, category TEXT)")
        await db.commit()

async def add_user(tg_id, amount_left):
    async with aiosqlite.connect("expenses.db") as db:
        await db.execute("INSERT INTO Users (tg_id, amount_left) VALUES (?, ?)", (tg_id, amount_left))
        await db.commit()

async def check_user_exists(tg_id:str):
    async with aiosqlite.connect('expenses.db') as conn:
        result = await conn.execute("SELECT * FROM Users WHERE tg_id = ?", (tg_id,))
        try:
            if await result.fetchone(): return True
            else: return False
        except Exception as e:
            logger.error(f"Error checking user existence: {e}")           
            return False

async def add_income(tg_id, expense_amount):
    async with aiosqlite.connect("expenses.db") as db:
        await db.execute("UPDATE Users SET amount_left = amount_left + ? WHERE tg_id = ?", (expense_amount, tg_id))
        await db.commit()

async def add_expense(tg_id, expense_date, expense_amount, category):
    async with aiosqlite.connect("expenses.db") as db:
        await db.execute("UPDATE Users SET amount_left = amount_left - ? WHERE tg_id = ?", (expense_amount, tg_id))
        await db.execute("INSERT INTO Expenses (tg_id, date, expense_amount, category) VALUES (?, ?, ?, ?)", (tg_id, expense_date, expense_amount, category))
        await db.commit()

async def delete_expense(tg_id, expense_date, expense_amount, category):
    async with aiosqlite.connect("expenses.db") as db:
        await db.execute("DELETE FROM Expenses WHERE tg_id= ? AND date=? AND expense_amount = ? AND  category = ?", (tg_id, expense_date, expense_amount, category))
        await db.execute("UPDATE Users SET amount_left = amount_left + ? WHERE tg_id = ?", (expense_amount, tg_id))
        await db.commit()


async def get_expenses_for_period(tg_id, start_date, end_date):
    async with aiosqlite.connect('expenses.db') as db:
        async with db.execute(f"SELECT * FROM Expenses WHERE tg_id = ? AND date BETWEEN ? AND ?", (tg_id, start_date, end_date)) as cursor:
            rows = await cursor.fetchall()
            transactions = [row for row in rows]
            return transactions