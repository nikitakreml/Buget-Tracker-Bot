from aiogram import Bot, types, F
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Text
from aiogram.filters import Command
from datetime import datetime
from loguru import logger
from config import TOKEN
import asyncio
from keyboards import *
from db import *
from states import *
logger.add("logs.log", rotation="1 week")
bot = Bot(token=TOKEN, parse_mode="HTML", disable_web_page_preview=False)
dp = Dispatcher()



@dp.message(Command('start'))
async def command_start_handler(message: types.Message, state: FSMContext) -> None:
    logger.info(f"Бот приступил к работе у пользователя {str(message.from_user.id)}")
    if not await check_user_exists(str(message.from_user.id)):
        await add_user(tg_id=str(message.from_user.id), amount_left=0)
    await message.answer(f"👋Привет, {message.from_user.full_name}!\n", reply_markup=start_keyboard())


@dp.message(F.text=="↩️Отмена")
async def get_back(message: types.Message, state: FSMContext):
    await state.clear()
    logger.info(f"Пользователь {str(message.from_user.id)} вернулся в главное меню")
    await message.answer(f"😊Что теперь, {message.from_user.full_name}?\nТы можешь посмотреть свои доходы и расходы, а также добавить новые!", reply_markup=start_keyboard())
#INCOME HANDLE

@dp.message(F.text=="➕Добавить доход")
async def add_income_handler(message: types.Message, state: FSMContext):
    await state.set_state(IncomeForm.pass_income_amount)
    await message.answer(f"➡️Введи сумму дохода в рублях без пробелов и запятых:\n😔К сожалению, копейки пока тоже нельзя, но мы обязательно это исправим:", reply_markup=cancel_keyboard())

@dp.message(IncomeForm.pass_income_amount, F.text.isdigit())
async def input_income_handler(message: types.Message, state: FSMContext):
    data = await state.update_data(income = message.text)
    await state.clear()
    await add_income(message.from_user.id, float(data["income"]))
    await message.answer(f"✅ Доход добавлен\n💵 Сумма: {data['income']}", reply_markup=start_keyboard())

#EXPENSE HANDLE

@dp.message(F.text=="➖Добавить расход")
async def get_back_handler(message: types.Message, state: FSMContext):
    await state.set_state(ExpenseForm.pass_expense_category)
    await message.answer(f"😉 Выбери категорию расхода или введи свою!", reply_markup=categories_keyboard())

@dp.message(ExpenseForm.pass_expense_category)
async def input_category_handler(message: types.Message, state: FSMContext):
    await state.update_data(expense_category = message.text)
    await state.set_state(ExpenseForm.pass_expense_amount)
    await message.answer(f"➡️Теперь введи сумму в рублях без пробелов и запятых:", reply_markup=cancel_keyboard())

@dp.message(ExpenseForm.pass_expense_amount, F.text.isdigit())
async def input_income_handler(message: types.Message, state: FSMContext):
    data = await state.update_data(expense_amount = message.text)
    await state.clear()
    await add_expense(tg_id=message.from_user.id, expense_date=str(datetime.datetime.today().strftime('%Y-%m-%d')), expense_amount=int(data["expense_amount"]), category=data["expense_category"])
    await message.answer(f"Расход был записан!\n🗃️ Категория: {data['expense_category']}\n💲 Сумма: {int(data['expense_amount'])}", reply_markup=start_keyboard())




@dp.message(F.text=="📊Посмотреть расходы за временной период")
async def get_by_time_handler(message: types.Message, state: FSMContext):
    await state.set_state(DateForm.pass_start_date)
    await message.answer(f"📅 Введите дату начала периода в формате 'ГГГГ-ММ-ДД'", reply_markup=categories_keyboard())

@dp.message(DateForm.pass_start_date)
async def time_start_handler(message: types.Message, state: FSMContext):
    await state.update_data(start_time = message.text)
    await state.set_state(DateForm.pass_end_date)
    await message.answer(f"📅 Введите дату конца периода в формате 'ГГГГ-ММ-ДД'", reply_markup=cancel_keyboard())

@dp.message(DateForm.pass_end_date)
async def time_end_handler(message: types.Message, state: FSMContext):
    data = await state.update_data(end_time = message.text)
    await state.clear()
    query = await get_expenses_for_period(start_date=data["start_time"], end_date=data["end_time"], tg_id=str(message.from_user.id))
    ans_query = []
    for i in query:
        ans_query.append(f"{i[2]} - {i[3]} - {i[4]}")
    for i in ans_query:
        await message.answer(f"{i}", reply_markup=remove_expense_keyboard())

@dp.callback_query(F.data == "delete_expense_btn")
async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    parameters = list(map(str, callback_query.message.text.split(sep = " - ")))
    print(callback_query.from_user.id, parameters[0], parameters[1], parameters[2], sep=",")
    await delete_expense(tg_id = callback_query.from_user.id, expense_date=parameters[0], expense_amount=f"{int(parameters[1])}", category=parameters[2])
    await callback_query.message.delete()
    await callback_query.answer(f"{callback_query.message.text}", reply_markup=start_keyboard())



async def main() -> None:
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger.success("Бот приступил к работе")
    asyncio.run(create_tables())
    asyncio.run(main())
