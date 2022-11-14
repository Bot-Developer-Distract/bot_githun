from main import open_account, save_member_data, get_bank_data
import random
import discord
from discord.ext import commands
import json
import pymailtm
import requests
import base64
class Mail10p(commands.Cog):
    config = {
        "author":"Anh Duc(aki-team)",
        "name": "mail10p",
        "desc": "tạo gmail ảo",
        "use": "<prefix>mail10p [message/account/create]\n- message (xem các mail gửi đến)\n- account (xem thông tin gmail ảo của bạn)\n- create (tạo gmail ảo)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command()
    async def mail10p(self, ctx, arg = None):
        try:
            await open_account(ctx.message.author.id)
            member_data = await get_bank_data()
            if arg == None:
                await ctx.send('error: sai cú pháp')
            elif arg == 'create':
                if "email" in member_data[str(ctx.message.author.id)]:
                    await ctx.send(f"bạn đã tạo một tài khoản trước đó rồi, không thể tạo thêm. Sử Dụng {member_data[str(ctx.message.guild.id)]['prefix']}mail10p load_account")
                else:
                    await ctx.send('đang tạo tài khoản vui lòng đợi,...')
                    p = pymailtm.MailTm()
                    password = p._generate_password(8)
                    domain = str(random.choice(p._get_domains_list()))
                    create = p._make_account_request("accounts",p._generate_password(12).lower() + '@' + domain, password)
                    print(create)
                    address = create["address"]
                    _id = create["id"]
                    member_data[str(ctx.message.author.id)]['email'] = {}
                    member_data[str(ctx.message.author.id)]['email']["address"] = str(address)
                    member_data[str(ctx.message.author.id)]['email']['password'] = str(password)
                    member_data[str(ctx.message.author.id)]['email']['id'] = str(_id)
                    save_member_data(member_data) 
                    user = await self.bot.fetch_user(ctx.message.author.id)
                    await user.send(f"Tạo tài khoản thành công\nEmail: {address}\npassword: {password}\nid: {_id}")
            elif arg == 'message':
                if "email" not in member_data[str(ctx.message.author.id)]:
                    await ctx.send(f"bạn chưa tạo tài khoản email để xem tin nhắn gửi đến, sử dụng: {member_data[str(ctx.message.guild.id)]['prefix']}mail10p create để tạo tài khoản")
                else:
                    p = pymailtm.MailTm()
                    await ctx.send("đang thu thập các mail gửi đến...")
                    path = member_data[str(ctx.message.author.id)]['email']
                    x = pymailtm.Account(path['id'], path["address"], path["password"])
                    r = requests.get("{}/messages?page={}".format(p.api_address, "1"),headers=x.auth_headers)
                    user = await self.bot.fetch_user(ctx.message.author.id)
                    await user.send(f"Đã nhận được {len(r.json()['hydra:member'])} mail gửi đến tài khoản")
                    message = {}
                    num_email = 1
                    for i in r.json()['hydra:member']:
                        get = requests.get(f"{p.api_address}/messages/{i['id']}", headers=x.auth_headers)
                        data = json.loads(get.text)
                        message['from'] = data['from']['address']
                        for k in data['to']:
                            message['to'] = []
                            message['to'].append(k['address'])
                            message['subject'] = data['subject']
                            message['body'] = data['text']
                            if data['hasAttachments'] == True:
                                num_attachments = []
                                backslash = r'\"'
                                for i in data['attachments']:
                                    get_attachment = requests.get(str(p.api_address) + str(i['downloadUrl']).strip(backslash), headers = x.auth_headers)
                                    file = open("mail10p.png", "wb")
                                    file.write(get_attachment.content)
                                    file.close()
                                    with open("mail10p.png", "rb") as file:
                                        link = []
                                        url = "https://api.imgbb.com/1/upload"
                                        payload = { "key": "a631a9c1fceb926d62f8108aa6580e2a", "image": base64.b64encode(file.read()), }
                                        up_image = requests.post(url, payload).json()
                                        link.append(up_image["data"]["image"]["url"])
                                message_send = f"email thứ {num_email}:\nGửi từ: {str(message['from'])}\nGửi đến: {str(message['to']).replace('[', '').replace(']', '')}\nTiêu đề: {str(message['subject'])}\nNội dung: {str(message['body'])}\nTệp đính kèm trong mail\n"
                                for ls in link:
                                    message_send += f"{ls}\n"
                                await user.send(f"{message_send}")
                            else:
                                await user.send(f"email thứ {num_email}:\nGửi từ: {str(message['from'])}\nGửi đến: {str(message['to']).replace('[', '').replace(']', '')}\nTiêu đề: {str(message['subject'])}\nNội dung: {str(message['body'])}")
                            num_email += 1
            elif arg == 'account':
                if "email" not in member_data[str(ctx.message.author.id)]:
                    await ctx.send('bạn chưa tạo tài khoản mail10p để lấy thông tin account')
                else:
                    await ctx.send(f"đã thu thập thành công thông tin tài khoản của {ctx.author.name}")
                    user = await self.bot.fetch_user(ctx.message.author.id)
                    id_account = member_data[str(ctx.message.author.id)]['email']['id']
                    password_account = member_data[str(ctx.message.author.id)]['email']['password']
                    address_account = member_data[str(ctx.message.author.id)]['email']['address']
                    user.send(f'thông tin về tài khoản của bạn như sau\nid: {id_account}\naddress: {address_account}\npassword: {password_account}')
            elif arg == "delete":
                if "email" not in member_data[str(ctx.message.author.id)]:
                    await ctx.send("bạn chưa sở hữu tài khoản mail để xóa")
                else:
                    member_data = member_data[str(ctx.message.author.id)]
                    account = pymailtm.Account(id = member_data['email']['id'], address=member_data['email']['address'], password=member_data['email']['password'])
                    result = account.delete_account()
                    if result:
                        del member_data['email']
                        save_member_data(member_data)
                        await ctx.send(f'xóa tài khoản thành công')
                        return
                    del member_data['email']
                    save_member_data(member_data)
                    await ctx.send("xóa tài khoản thất bại")
            else:
                await ctx.send(f"sai cú pháp")
        except Exception as e:
                print(e)
                await ctx.send(f"đã xảy ra lỗi: {e}\nVui lòng thử lại sau")
async def setup(bot):
    await bot.add_cog(Mail10p(bot))
