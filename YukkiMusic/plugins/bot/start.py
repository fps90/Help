from YukkiMusic import app
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import SUPPORT_GROUP, SUPPORT_CHANNEL, OWNER, START_IMG_URL

# Dummy function add_served_user to avoid error
async def add_served_user(user_id: int):
    # You can add user storage logic here if necessary
    pass

# Command handlers
@app.on_message(filters.command(["start", "help"]) & filters.private)
async def start_(c: Client, message: Message):
    user_id = message.from_user.id
    await add_served_user(user_id)
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه . \n⎯ ⎯ ⎯ ⎯""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⦗ قائمة الأوامر ⦘", callback_data="command_list")
                ],
                [
                    InlineKeyboardButton(text="⦗ قناة السورس ⦘", url=SUPPORT_CHANNEL),
                    InlineKeyboardButton(text="⦗ قناة التحديثات ⦘", url=SUPPORT_GROUP),
                ],
                [
                    InlineKeyboardButton(text="⦗ مطور البوت ⦘", user_id=int(OWNER)),
                ],
            ]
        )
    )

# Callback query handlers
@app.on_callback_query(filters.regex("home_start"))
async def start_set(_, query: CallbackQuery):
    await query.answer("القائمة الرئيسية")
    await query.edit_message_text(
        f"""أَهلًا بك عزيزي في بوت تشغيل الميديا الصوتية في المجموعات والقنوات مع دعم مُميزات كثيرة يُمكنُك التحقُق منها عن طريق إِستخدام الازرار أدناه . \n⎯ ⎯ ⎯ ⎯""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="⦗ قائمة الأوامر ⦘", callback_data="command_list")
                ],
                [
                    InlineKeyboardButton(text="⦗ قناة السورس ⦘", url=SUPPORT_CHANNEL),
                    InlineKeyboardButton(text="⦗ قناة التحديثات ⦘", url=SUPPORT_GROUP),
                ],
                [
                    InlineKeyboardButton(text="⦗ مطور البوت ⦘", user_id=int(OWNER)),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("command_list"))
async def commands_set(_, query: CallbackQuery):
    await query.answer("👍🏻قائمة الاوامر")
    await query.edit_message_text(
        f"""- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ أوامر التشغيل ⦘", callback_data="user_command"),
                ],
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="home_start"),
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("next"))
async def next_set(_, query: CallbackQuery):
    await query.answer("تم فتح لوحة التحكم")
    await query.edit_message_text(
        """- تم فتح لوحة التحكم ↓
 – – – – – – 
⦗ تستطيع التحكم عن طريق الأزرار أدناه ⦘""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ أوامر المطورين ⦘", callback_data="developer_commands"),
                ],
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="command_list"),
                    InlineKeyboardButton("⦗ أوامر المالك ⦘", callback_data="owner_commands"),
                ],
            ]
        )
    )

@app.on_callback_query(filters.regex("user_command"))
async def user_commands_set(_, query: CallbackQuery):
    await query.answer("أوامر التشغيل")
    await query.edit_message_text(
        f"""هذا هي أوامر التشغيل""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ التالي ⦘", callback_data="next")
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("developer_commands"))
async def developer_commands_set(_, query: CallbackQuery):
    await query.answer("أوامر المطورين")
    await query.edit_message_text(
        f"""هذا هي أوامر المطورين""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="next")
                ],
            ]
        ),
    )

@app.on_callback_query(filters.regex("owner_commands"))
async def owner_commands_set(_, query: CallbackQuery):
    await query.answer("أوامر المالك")
    await query.edit_message_text(
        f"""هذا هي أوامر المالك""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⦗ الرجوع ⦘", callback_data="next")
                ],
            ]
        ),
    )
