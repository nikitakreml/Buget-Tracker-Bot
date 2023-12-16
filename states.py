from aiogram.fsm.state import State, StatesGroup


class IncomeForm(StatesGroup):
    pass_income_amount = State()


class ExpenseForm(StatesGroup):
    pass_expense_category = State()
    pass_expense_amount = State()

class DateForm(StatesGroup):
    pass_start_date = State()
    pass_end_date = State()