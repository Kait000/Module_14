import asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import get_all_products, is_included, add_user

API = ''
bot = Bot(token=API)
dp = Dispatcher(bot, storage=MemoryStorage())

rus_key = ('а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о',
           'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я')


"""Описание нижней клавиатуры"""
kb_reply = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Рассчитать'), KeyboardButton(text='Информация')
        ], [
            KeyboardButton(text='Купить')
        ], [
            KeyboardButton(text='Регистрация')
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
            InlineKeyboardButton(text='Продукт 1', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт 2', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт 3', callback_data='product_buying'),
            InlineKeyboardButton(text='Продукт 4', callback_data='product_buying')
        ]
    ]
)


class UserState(StatesGroup):
    """Состояние КАЛОРИИ"""
    age = State()  # возраст
    growth = State()  # рост
    weight = State()  # вес


class RegistrationState(StatesGroup):
    """Состояние РЕГИСТРАЦИЯ"""
    username = State()
    email = State()
    age = State()
    balance = State()


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
    """Состояние КАЛОРИИ 1.1"""
    await call.answer()
    await call.message.answer('Введите свой возраст: ')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    """Состояние КАЛОРИИ 1.2"""
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост: ')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    """Состояние КАЛОРИИ 1.3"""
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес: ')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    """Состояние КАЛОРИИ 1.4 end"""
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


@dp.message_handler(text='Регистрация')
async def sing_up(message):
    """Состояние РЕГИСТРАЦИЯ 1.1"""
    await message.answer('Введите имя пользователя (только латинский алфавит): ')
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_growth(message, state):
    """Состояние РЕГИСТРАЦИЯ 1.2"""
    key = True
    for i in range(len(message.text)):
        if message.text[i].lower() in rus_key:
            key = False
            await message.answer('Вы ввели недопустимые символы, повторите ввод')
            break
    if key:
        if is_included(message.text):
            await message.answer('Пользователь существует, введите другое имя')
        else:
            await state.update_data(username=message.text)
            await message.answer('Введите свой email: ')
            await RegistrationState.email.set()


@dp.message_handler(state=RegistrationState.email)
async def set_growth(message, state):
    """Состояние РЕГИСТРАЦИЯ 1.3"""
    await state.update_data(email=message.text)
    await message.answer('Введите свой возраст: ')
    await RegistrationState.age.set()


@dp.message_handler(state=RegistrationState.age)
async def set_growth(message, state):
    """Состояние РЕГИСТРАЦИЯ 1.4 end"""
    try:
        if int(message.text) <= 0:
            raise ValueError
        await state.update_data(age=int(message.text))
        data = await state.get_data()
        add_user(data['username'], data['email'], data['age'])
        await message.answer('Регистрация прошла успешно!')
        await state.finish()
    except ValueError:
        await message.answer('Возраст должен быть положительным числом!')


@dp.message_handler(text='Купить')
async def get_buying_list(message):
    """Выводим список товаров по кнопке Купить"""
    for item in get_all_products():
        await message.answer(f'Название: {item[1]} | '
                             f'Описание: {item[2]} | '
                             f'Цена: {item[3]}')
        with open(f'img/{item[1]}.png', 'rb') as img:
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
