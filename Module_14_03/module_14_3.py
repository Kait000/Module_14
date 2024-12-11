import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API = ''
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())


"""Описание нижней клавиатуры"""
kb_reply = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')
        ], [
            KeyboardButton(text='Купить')
        ]
    ], resize_keyboard=True
)

"""Описание инлайн клавиатуры калории"""
kb_inline = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
            InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
        ]
    ]
)

"""Описание инлайн клавиатуры продажи"""
kb_inline_2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Product1', callback_data='product_buying'),
            InlineKeyboardButton(text='Product2', callback_data='product_buying'),
            InlineKeyboardButton(text='Product3', callback_data='product_buying'),
            InlineKeyboardButton(text='Product4', callback_data='product_buying')
        ]
    ]
)


class UserState(StatesGroup):
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_reply)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию: ', reply_markup=kb_inline)


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.answer()
    await call.message.answer('10 х вес(кг) + 6,25 х рост(см) - 5 х возраст(г) + 5')


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.answer()
    await call.message.answer('Введите свой возраст: ')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    try:
        calories = ((10 * float(data['weight'])) +
                    (6.25 * float(data['growth'])) -
                    (5 * float(data['age'])) + 5)
        await message.answer(f'Ваша норма калорий: {calories}')
    except ValueError:
        await message.answer('Вы ввели не верные данные, попробуйте еще раз.')
    await state.finish()


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for item in range(1, 5):
        await message.answer(f'Название: Product{item} | '
                             f'Описание: Описание{item} | '
                             f'Цена: {item*100}')
        with open(f'img/Product{item}.png', 'rb') as img:
            await message.answer_photo(img)
    await message.answer('Выберите продукт для покупки: ', reply_markup=kb_inline_2)


@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.answer()
    await call.message.answer(f'Вы успешно приобрели продукт!')


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
