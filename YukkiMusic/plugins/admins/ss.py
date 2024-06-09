from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import platform
import socket
import psutil
import requests
import speedtest
import datetime
import os
import uuid
from strings.filters import command
from config import OWNER
from YukkiMusic import app

def humanbytes(B):
    """تحويل بايتات إلى قراءة بشرية"""
    B = float(B)
    KB = float(1024)
    MB = float(KB ** 2) 
    GB = float(KB ** 3) 
    TB = float(KB ** 4) 

    if B < KB:
        return "{0} {1}".format(B, "Bytes" if 0 == B > 1 else "Byte")
    elif KB <= B < MB:
        return "{0:.2f} KB".format(B / KB)
    elif MB <= B < GB:
        return "{0:.2f} MB".format(B / MB)
    elif GB <= B < TB:
        return "{0:.2f} GB".format(B / GB)
    elif TB <= B:
        return "{0:.2f} TB".format(B / TB)

def get_hosting_type():
    if "DYNO" in os.environ:
        return "Heroku"
    elif "PYTHONHOME" in os.environ:
        return "PythonAnywhere"
    elif "LD_LIBRARY_PATH" in os.environ:
        return "Linux VPS"
    else:
        return "غير معروف"

def check_internet_connection():
    try:
        requests.get("https://www.google.com/", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def get_network_status():
    if check_internet_connection():
        return "متصل بالإنترنت"
    else:
        return "غير متصل بالإنترنت"

def get_network_information():
    try:
        public_ip = requests.get("https://api64.ipify.org").text.strip()
    except Exception as e:
        public_ip = "غير متاح"

    try:
        isp_name = requests.get("https://ipinfo.io/org").text.strip()
    except Exception as e:
        isp_name = "غير متاح"

    try:
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        speed_info = st.results.dict()
    except Exception as e:
        speed_info = "غير متاح"

    return public_ip, isp_name, speed_info

start_time = datetime.datetime.now()

def get_uptime():
    uptime = datetime.datetime.now() - start_time
    return str(uptime).split(".")[0]

def get_actual_used_memory():
    used_memory = psutil.virtual_memory().used
    return humanbytes(used_memory)

def get_cpu_load():
    cpu_load = psutil.cpu_percent(interval=1)
    return f"{cpu_load}%"

def get_system_info():
    virtual_memory = psutil.virtual_memory()
    total_memory = humanbytes(virtual_memory.total)
    available_memory = humanbytes(virtual_memory.available)
    used_memory = humanbytes(virtual_memory.used)
    percent_memory = virtual_memory.percent

    cpu_percent = psutil.cpu_percent(interval=1)

    return total_memory, available_memory, used_memory, percent_memory, cpu_percent

def get_bot_speed():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        st.download()
        st.upload()
        speed = st.results.dict()
        download_speed = humanbytes(speed["download"])
        upload_speed = humanbytes(speed["upload"])
        return f"سرعة التحميل: {download_speed}\nسرعة الرفع: {upload_speed}"
    except Exception as e:
        return "غير متاح"

@app.on_message(command(["معلومات التشغيل", "السيرفر"]) & (filters.private | filters.group))
async def fetch_system_information(client, message):
    if message.from_user.id == int(OWNER):       
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("نظام التشغيل", callback_data="system_os"),
                    InlineKeyboardButton("إصدار نظام التشغيل", callback_data="system_release"),
                ],
                [
                    InlineKeyboardButton("عنوان IP", callback_data="system_ip"),
                    InlineKeyboardButton("عنوان MAC", callback_data="system_mac"),
                ],
                [
                    InlineKeyboardButton("المعالج", callback_data="system_processor"),
                    InlineKeyboardButton("استخدام وحدة المعالجة المركزية", callback_data="system_cpu"),
                ],
                [
                    InlineKeyboardButton("معلومات الذاكرة", callback_data="system_memory"),
                    InlineKeyboardButton("الشبكة", callback_data="system_network"),
                ],
                [
                    InlineKeyboardButton("IP العام", callback_data="system_public_ip"),
                    InlineKeyboardButton("مقدم الخدمة", callback_data="system_isp"),
                ],
                [
                    InlineKeyboardButton("وقت التشغيل", callback_data="system_uptime"),
                ],
                [
                    InlineKeyboardButton("اجمالي الذاكرة", callback_data="total_memory"),
                    InlineKeyboardButton("المستخدم", callback_data="used_memory"),
                ],
                [
                    InlineKeyboardButton("المتاح", callback_data="available_memory"),
                    InlineKeyboardButton("حالة الشبكة", callback_data="network_status"),
                ],
                [
                    InlineKeyboardButton("سرعة البوت", callback_data="bot_speed"),
                ],
            ]
        )

        await message.reply_text(
            text="اختر ما تريد معرفته عن النظام عزيزي المطور :",
            reply_markup=keyboard
        )
    
@app.on_callback_query()
async def callback_query_handler(client, query):
    if query.from_user.id != int(OWNER):
        await query.answer("# هذا الزر خاص بمطور البوت .", show_alert=True)
        return
      
    splatform = platform.system()
    platform_release = platform.release()
    platform_version = platform.version()
    architecture = platform.machine()
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(socket.gethostname())
    mac_address = ":".join(re.findall("..", "%012x" % uuid.getnode()))
    processor = platform.processor()
    cpu_len = len(psutil.Process().cpu_affinity())

    hosting_type = get_hosting_type()

    public_ip, isp_name, speed_info = get_network_information()

    uptime = get_uptime()

    total_memory, available_memory, used_memory, percent_memory, cpu_percent = get_system_info()

    actual_used_memory = get_actual_used_memory()

    cpu_load = get_cpu_load()

    network_status = get_network_status()

    bot_speed = get_bot_speed()

    if query.data == "system_os":
        await query.answer(text=f"نظام التشغيل: {splatform}", show_alert=True)
    
    elif query.data == "system_release":
        await query.answer(text=f"إصدار نظام التشغيل: {platform_release}", show_alert=True)
    
    elif query.data == "system_ip":
        await query.answer(text=f"عنوان IP: {ip_address}", show_alert=True)
    
    elif query.data == "system_mac":
        await query.answer(text=f"عنوان MAC: {mac_address}", show_alert=True)
    
    elif query.data == "system_processor":
        await query.answer(text=f"المعالج: {processor}", show_alert=True)
    
    elif query.data == "system_cpu":
        await query.answer(text=f"استخدام وحدة المعالجة المركزية: {cpu_load}", show_alert=True)
    
    elif query.data == "system_memory":
        await query.answer(text=f"""
- اجمالي الذاكرة : {total_memory}
- الذاكرة الفعلية المستخدمة : {actual_used_memory}
""", show_alert=True)
    
    elif query.data == "system_network":
        await query.answer(text=f"""
- العنوان IP العام: {public_ip}
- اسم مزود خدمة الإنترنت: {isp_name}
""", show_alert=True)
    
    elif query.data == "system_public_ip":
        await query.answer(text=f"العنوان IP العام: {public_ip}", show_alert=True)
    
    elif query.data == "system_isp":
        await query.answer(text=f"مقدم الخدمة: {isp_name}", show_alert=True)
    
    elif query.data == "system_uptime":
        await query.answer(text=f"وقت التشغيل: {uptime}", show_alert=True)
    
    elif query.data == "total_memory":
        await query.answer(text=f"اجمالي الذاكرة: {total_memory}", show_alert=True)
    
    elif query.data == "used_memory":
        await query.answer(text=f"الذاكرة المستخدمة: {used_memory} ({percent_memory}%)", show_alert=True)
    
    elif query.data == "available_memory":
        await query.answer(text=f"الذاكرة المتاحة: {available_memory} ({100 - percent_memory}%)", show_alert=True)
    
    elif query.data == "network_status":
        await query.answer(text=f"حالة الشبكة: {network_status}", show_alert=True)
    
    elif query.data == "bot_speed":
        await query.answer(text=f"سرعة البوت: {bot_speed}", show_alert=True)
