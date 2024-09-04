
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot,storage=MemoryStorage())

@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.')

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age_=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth_=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight_=message.text)
    data = await state.get_data()
    amount_calories = (10 * float(data['weight_'])) + (6.25 * float(data['growth_'])) - (5 * float(data['age_']) + 5)
    await message.answer(f'Ваша норма калорий {amount_calories}')
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)







