from aiogram.fsm.state import StatesGroup, State

class PaymentStates(StatesGroup):
    selecting_currency = State()
    awaiting_screenshot = State()