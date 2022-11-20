
from discord.ext.commands import *
from discord.ext import commands
from discord import *
import aiohttp
import sqlite3
import os
import time
import nest_asyncio
import asyncio
import json
import requests
from host.webdriver import server
#khai báo
#=============================================#
nest_asyncio.apply()
with open('config.json', 'r') as f:
    config = json.load(f)
bot=commands.Bot(command_prefix=config['prefix'],intents=Intents.all(),help_command=None)
bot.database = sqlite3.connect('data.db', timeout = 10)
bot.sql = bot.database.cursor()
#=============================================#

#treo bot
#=============================================#
server()
#=============================================#

#hàm chung
#=============================================#
async def update(user, change, mode):
    if mode == "win_wallet":
        bot.sql.execute(f'UPDATE user_data SET user_money = user_money + {change} WHERE user_id={user}')
    elif mode == "lose_wallet":
        bot.sql.execute(f'UPDATE user_data SET user_money = user_money - {change} WHERE user_id={user}')
    elif mode == "win_bank":
        bot.sql.execute(f'UPDATE user_data SET user_bank = user_bank + {change} WHERE user_id={user}')
    elif mode == "lose_bank":
        bot.sql.execute(f'UPDATE user_data SET user_bank = user_bank - {change} WHERE user_id={user}')
async def open_account(user):
    users = await get_bank_data()
    if str(user) in users:
        return False
    else:
        users[str(user)] = {}
    save_member_data(users)
    return True


async def get_bank_data():
    with open("command/data.json", 'r') as f:
        users = json.load(f)
    return users

def save_member_data(data):
    with open("command/data.json", 'w') as f:
        json.dump(data, f)
#=============================================#



#hàm chính chạy bot
#=============================================#
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.reply(f"Không tìm thấy lệnh `{ctx.invoked_with}`")

    elif isinstance(error, CommandOnCooldown):
        await ctx.reply(f"Xài lệnh chậm thôi bạn ơi. Hãy thử lại sau {error.retry_after :.3f}s")

@bot.event
async def on_ready():
  bot.session = await aiohttp.ClientSession()
  print("bot đã sẵn sàng")
  
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@bot.event
async def on_message(message):
    await bot.process_commands(message)
async def main():
    thong_bao = requests.get(url='https://api-iotran.tk/aki-bot/update').json()
    print(bcolors.WARNING+'                      MODULE'+bcolors.ENDC)
    print('═══════════════════════════════════════════════════')
    dem_lenh=0
    commands = os.listdir('command')
    for command in commands:
        if(command=='__pycache__' or command=='random_list' or command=="data.json" or command=="cache"):
            pass
        else:
            try:
                await bot.load_extension(f"command.{command[:-3]}")
                print(bcolors.OKBLUE+f'>> load thành công module {command[:-3]}'+bcolors.ENDC)
                dem_lenh=dem_lenh+1
                time.sleep(0.025)
            except:
                print(bcolors.FAIL+f'>> load thất bại module {command[:-3]}'+bcolors.ENDC)
    print('═════════════════════════════════════════════════════')
    print(bcolors.WARNING+'                      EVENT'+bcolors.ENDC)
    print('═════════════════════════════════════════════════════')
    for command in os.listdir("./event"):
        if(command=='__pycache__' or command=='random_list' or command=="data.json"):
            pass
        else:
            await bot.load_extension(f"event.{command[:-3]}")
            print(bcolors.OKBLUE+f'>> load thành công module {command[:-3]}'+bcolors.ENDC)
            time.sleep(0.025)
    print('═════════════════════════════════════════════════════')
    print(bcolors.OKGREEN+'''
 █████╗ ██╗  ██╗██╗    ██████╗  ██████╗ ████████╗
██╔══██╗██║ ██╔╝██║    ██╔══██╗██╔═══██╗╚══██╔══╝
███████║█████╔╝ ██║    ██████╔╝██║   ██║   ██║   
██╔══██║██╔═██╗ ██║    ██╔══██╗██║   ██║   ██║   
██║  ██║██║  ██╗██║    ██████╔╝╚██████╔╝   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝    ╚═════╝  ╚═════╝    ╚═╝   
                                                 
                                                                       
'''+bcolors.ENDC)
    print(f'''
        ══╦═════════════════════════════════╦══
╔═════════╩═════════════════════════════════╩═════════╗      
║ TÁC GIẢ:King.#4732 and Anh Duc#5954                 
║ CHỦ SỞ HỮU BOT: {config['admin_name']}({config['admin_id']})                          
║ TÊN BOT:{config['bot_name']}  
║ PREFIX:{config['prefix']}   
║ PHIÊN BẢN:{thong_bao['version']}                       
║ SỐ MODULE(LỆNH) HIỆN CÓ TRONG BOT: {dem_lenh}                   
╚═════════════════════════════════════════════════════╝
''')
    try:
        print(bcolors.WARNING+f">> Khởi động thành công {config['bot_name']} <<"+bcolors.ENDC)
        print(bcolors.OKBLUE+f'''Lời nhắn của aki team :{thong_bao['message']}'''+bcolors.ENDC)
        await bot.start(config['token'])
    except:
        print(bcolors.WARNING+'>> LỖI TOKEN BOT <<'+bcolors.ENDC)
try: 
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
except Exception as e:
  print(e)
  os.system("kill 1")
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  


#=============================================#