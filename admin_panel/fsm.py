from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from keyboards.inline_keyboards import admin_panel_main_menu
from config.bot_config import dp, bot


class FSM_UserRole(StatesGroup):
    user_id = State()


@dp.message_handler(state='*',
                    commands='cancel')
async def cancel_command(message: types.Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state is None:
        return
    await state.finish()
    await bot.delete_message(chat_id=message.from_user.id,
                             message_id=message.message_id)
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'{message.from_user.first_name} операция отменена',
                           reply_markup=admin_panel_main_menu)


@dp.callback_query_handler(text='make_user_role')
async def create_user_role(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Кого вы хотите добавить?',
                           reply_markup=admin_panel_main_menu)


@dp.callback_query_handler(text='take_user_role', state=None)
async def load_user_role(callback_query: types.CallbackQuery):
    await FSM_UserRole.user_id.set()
    await bot.delete_message(chat_id=callback_query.from_user.id,
                             message_id=callback_query.message.message_id)
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text='Роль успешна выбрана!\n\n Введите номер пользователя',
                           reply_markup=admin_panel_main_menu)


@dp.message_handler(state=FSM_UserRole.user_id)
async def load_user_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text
        await state.finish()
        await bot.delete_message(chat_id=message.from_user.id,
                                 message_id=message.message_id)
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Администратор \n\n ID пользователя {data["user_id"]}\n'
                               f'Успешно создан',
                               reply_markup=admin_panel_main_menu)
