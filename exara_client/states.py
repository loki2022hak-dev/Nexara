from aiogram.fsm.state import State, StatesGroup

class ExportStates(StatesGroup):
    choosing_format = State()
    confirming_id = State()
