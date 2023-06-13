from aiogram import types, executor
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext

from config.bot_config import bot, dp, ADMIN
from keyboards.inline_keyboards import admin_panel_main_menu


class FSM_StatesUser(StatesGroup):
    name = State()
    last_name = State()
    position = State()


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_cmd(message: types.Message, state: FSMContext):
    if state is None:
        return
    await state.finish()
    await message.reply('Вы прервали операцию',
                        reply_markup=admin_panel_main_menu)


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.answer('Привет!', reply_markup=admin_panel_main_menu)


@dp.message_handler(commands=['create_user'])
async def create_cmd(message: types.Message, state: FSMContext):
    await message.reply('Создать нового пользователя\n\nВведи Имя:')
    await state.set_state(FSM_StatesUser.name)


@dp.message_handler(content_types=['name'], state=FSM_StatesUser.name)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        print(data)
        data['name'] = message.photo[0].file_id
        print(data['name'])

    await message.reply('Теперь отправь своё имя!')
    await FSM_StatesUser.next()


@dp.message_handler(state=FSM_StatesUser.last_name)
async def load_last_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.message_id

    await message.answer('Введите должность')
    await FSM_StatesUser.next()


@dp.message_handler(state=FSM_StatesUser.position)
async def load_position(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['position'] = message.text

    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Сотрудник {data["first_name"]}{data["last_name"]}-{data["position"]} создан')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
