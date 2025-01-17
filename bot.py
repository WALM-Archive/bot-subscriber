import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ChatJoinRequest
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import config, info
from importlib import reload
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command, StateFilter

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_API)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

dp.chat_join_request.filter(F.chat.id == config.channel_id)

class FSMFillForm(StatesGroup):
    extended_channels_sfm = State()
    id_base_channel_sfm = State()
    extended_channels_id_sfm = State()
    tgk_sfm = State()
    hello_user_start_sfm = State()

@dp.message(Command("start"), StateFilter(default_state))
async def cmd_start(message: types.Message):
    
    if message.from_user.username == config.admin:
        
        builder = ReplyKeyboardBuilder()
        
        builder.row(
            types.KeyboardButton(text="ID телеграм канала для сбора заявок"),
            types.KeyboardButton(text="Список юзернеймов доп. телеграмм каналов"),
            types.KeyboardButton(text="Список ID доп. телеграмм каналов"),
        )
        builder.row(
            types.KeyboardButton(text="Добавить ID телеграм канала для сбора заявок"),
            types.KeyboardButton(text="Добавить юзернеймы доп. телеграмм каналов"),
            types.KeyboardButton(text="Добавить ID доп. телеграмм каналов"),
        )
        builder.row(
            types.KeyboardButton(text="Приветствие для подавшего заявку"),
            types.KeyboardButton(text="Название основного телеграмм канала"), 
        )
        builder.row(
            types.KeyboardButton(text="Добавить приветствие для подавшего заявку"),
            types.KeyboardButton(text="Добавить название основного телеграмм канала"),
        )

        await message.answer("Добро пожаловать в панель администрирования бота по принятию заявок телеграмм канала", reply_markup=builder.as_markup(resize_keyboard=True))


@dp.message(Command('edit_id_base_channel'))
async def edit_base_id(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введите ID телеграм канала для сбора заявок. ')
    await state.set_state(FSMFillForm.id_base_channel_sfm)
@dp.message(StateFilter(FSMFillForm.id_base_channel_sfm))
async def process_name_sent(message: types.Message, state: FSMContext):
    await message.answer('ID телеграм канала для сбора заявок принят и записан в конфиги. Требуется перезагрузка бота')

    configer = open('config.py', 'w+')
    configer.write(f'BOT_API = "{config.BOT_API}"')
    configer.write(f'\nadmin = "{config.admin}"')
    configer.write(f'\nchannel_id = {message.text}')
    configer.write(f'\nextended_channels_usernames = {config.extended_channels_usernames}')
    configer.write(f'\nextended_channels_id = {config.extended_channels_id}')
    configer.close()
    reload(config)
    
    await state.clear()

@dp.message(Command('edit_extended_chanels_usernames'))
async def edit_base_id(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введите юзернеймы доп. телеграмм каналов. Это нужно, чтобы пользователь переходил на эти каналы. Формат ответа такой - ["example", "example2"]. ')
    await state.set_state(FSMFillForm.extended_channels_sfm)
@dp.message(StateFilter(FSMFillForm.extended_channels_sfm))
async def process_name_sent(message: types.Message, state: FSMContext):
    await message.answer('юзернеймы доп. телеграмм каналов принят и записан в конфиги')

    configer = open('config.py', 'w+')
    configer.write(f'BOT_API = "{config.BOT_API}"')
    configer.write(f'\nadmin = "{config.admin}"')
    configer.write(f'\nchannel_id = {config.channel_id}')
    configer.write(f'\nextended_channels_usernames = {message.text}')
    configer.write(f'\nextended_channels_id = {config.extended_channels_id}')
    configer.close()
    reload(config)
    
    await state.clear()    

@dp.message(Command('edit_extended_chanels_id'))
async def edit_base_id(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введите ID доп. телеграмм каналов. Это нужно для того, чтобы можно было проверить, подписан ли пользователь на доп. телеграмм каналы. Формат ответа такой - ["-100456456", "-100546546"].')
    await state.set_state(FSMFillForm.extended_channels_id_sfm)
@dp.message(StateFilter(FSMFillForm.extended_channels_id_sfm))
async def process_name_sent(message: types.Message, state: FSMContext):
    await message.answer('ID доп. телеграмм каналов принят и записан в конфиги')

    configer = open('config.py', 'w+')
    configer.write(f'BOT_API = "{config.BOT_API}"')
    configer.write(f'\nadmin = "{config.admin}"')
    configer.write(f'\nchannel_id = {config.channel_id}')
    configer.write(f'\nextended_channels_usernames = {config.extended_channels_usernames}')
    configer.write(f'\nextended_channels_id = {message.text}')
    configer.close()
    reload(config)
    
    await state.clear()  


@dp.message(Command('edit_tgk'))
async def edit_base_id(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введите название своего основного телеграмм канала. Это нужно, чтобы тот, кто подал заявку, знал, откуда пришло сообщение')
    await state.set_state(FSMFillForm.tgk_sfm)
@dp.message(StateFilter(FSMFillForm.tgk_sfm))
async def process_name_sent(message: types.Message, state: FSMContext):
    await message.answer('Название основного телеграмм канала принято и записано в конфиги')

    configer = open('info.py', 'w+')
    configer.write(f'tgk = "{message.text}"')
    configer.write(f'\nhello_user_start = "{info.hello_user_start}"')
    configer.close()
    reload(info)

    await state.clear() 

@dp.message(Command('edit_hello_user_start'))
async def edit_base_id(message: types.Message, state: FSMContext):
    await message.answer('Пожалуйста, введите привествие. Это нужно, чтобы после подачи заявки приходило приветствие и мотивировало к выполнениям условий.')
    await state.set_state(FSMFillForm.hello_user_start_sfm)
@dp.message(StateFilter(FSMFillForm.hello_user_start_sfm))
async def process_name_sent(message: types.Message, state: FSMContext):
    await message.answer('Приветствие принято и записано в конфиги')

    configer = open('info.py', 'w+')
    configer.write(f'tgk = "{info.tgk}"')
    configer.write(f'\nhello_user_start = "{message.text}"')
    configer.close()
    reload(info)
    
    await state.clear()


@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.answer(
        text=f"Вы получили это сообщение, потому что вы подали заявку в {info.tgk} и на данный момент она рассматривается ",
        show_alert=True
    )  

@dp.message(F.text, StateFilter(default_state))
async def message(message: types.Message):

    if message.from_user.username == config.admin:
        if message.text == 'ID телеграм канала для сбора заявок':
            await message.answer(f"ID телеграмм канала для сбора заявок - {config.channel_id}")
        if message.text == 'Список ID доп. телеграмм каналов':
            await message.answer(f"Список ID доп. телеграмм каналов - {config.extended_channels_id}")
        if message.text == 'Список юзернеймов доп. телеграмм каналов':
            await message.answer(f"Список юзернеймов доп. телеграмм каналов - {config.extended_channels_usernames}")
        if message.text == 'Добавить ID телеграм канала для сбора заявок':
            await message.answer("Чтобы добавить ID телеграм канала для сбора заявок, активируйте комманду /edit_id_base_channel")
        if message.text == 'Добавить юзернеймы доп. телеграмм каналов':
            await message.answer("Чтобы добавить юзернеймы доп. телеграмм каналов, активируйте комманду /edit_extended_chanels_usernames")
        if message.text == 'Добавить ID доп. телеграмм каналов':
            await message.answer("Чтобы добавить ID доп. телеграмм каналов, активируйте комманду /edit_extended_chanels_id")
        if message.text == 'Приветствие для подавшего заявку':
            await message.answer(f"Приветствие для подавшего заявку - {info.hello_user_start}")
        if message.text == 'Название основного телеграмм канала':
            await message.answer(f"Название основного телеграмм канала - {info.tgk}") 
        if message.text == 'Добавить приветствие для подавшего заявку':
            await message.answer("Чтобы добавить приветствие для подавшего заявку, активируйте команду /edit_hello_user_start")
        if message.text == 'Добавить название основного телеграмм канала':
            await message.answer("Чтобы добавить название основного телеграмм канала, активируйте команду /edit_tgk")

@dp.chat_join_request() 
async def test(update: ChatJoinRequest):
    global join_error

    builder1 = InlineKeyboardBuilder()

    builder1.add(types.InlineKeyboardButton(text="подробнее", callback_data="random_value"))

    to_pin = await update.bot.send_message(update.from_user.id, f"Администраторы {info.tgk}, в которую вы подали заявку, рассматривают", reply_markup=builder1.as_markup())

    await bot.pin_chat_message(chat_id = update.from_user.id, message_id = to_pin.message_id)

    for i in config.extended_channels_id:

        user_channel_status = await update.bot.get_chat_member(chat_id=i, user_id=update.from_user.id)
        if user_channel_status.status == 'left':
            builder = InlineKeyboardBuilder()

            for i in config.extended_channels_usernames:
                builder.add(types.InlineKeyboardButton(
                    text="✅ТГ канал✅",
                    url=f"https://t.me/{i}")
                )
            join_error =0
            await update.bot.send_message(update.from_user.id, info.hello_user_start, reply_markup=builder.as_markup())
            await update.decline()  

            return False
          
    await update.approve()

    return True

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
