import discord
from discord.ext import commands
import chess
import chess.svg
import aspose.words as aw
class Chess(commands.Cog):
    config = {
        "name": "chess",
        "desc": "chơi cờ vua+)",
        "use": "<prefix>chess @mention",
        "author": "Anh Duc(aki team)"
    }
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name = "chess")
    async def chess(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send("@mention một người để chơi cùng bạn, hoặc tự đánh một mình bằng cách @mention chính bạn=))")
        else:    
            try:
                def save(svg_code):
                    f = open("file.svg", "w")
                    f.write(svg_code)
                    f.close()
                def convert_svg_to_png(list_image = ["file.svg"]):
                    fileNames = list_image
                    doc = aw.Document()
                    builder = aw.DocumentBuilder(doc)
                    shapes = [builder.insert_image(fileName) for fileName in fileNames]

                        # Calculate the maximum width and height and update page settings 
                        # to crop the document to fit the size of the pictures.
                    pageSetup = builder.page_setup
                    pageSetup.page_width = max(shape.width for shape in shapes)
                    pageSetup.page_height = sum(shape.height for shape in shapes)
                    pageSetup.top_margin = 0
                    pageSetup.left_margin = 0
                    pageSetup.bottom_margin = 0
                    pageSetup.right_margin = 0

                    doc.save("output.png")
                board = chess.Board()
                svg_code = chess.svg.board(board)
                f = open("file.svg", "w")
                f.write(svg_code)
                f.close()
                convert_svg_to_png(["file.svg"])
                send = await ctx.reply(f"ván cờ đã bắt đầu, quân trắng đi trước (lượt của <@{ctx.message.author.id}>), hãy di chuyển quân bằng cách gõ theo vị trí trên bàn cờ\nLưu ý: nếu muốn thoát ván cờ hãy gõ 'chess.out'",file=discord.File("output.png"))
                
                async def push_san(id, a):
                    board.push_san(str(a).lower())
                    save(chess.svg.board(board))
                    convert_svg_to_png()
                    await send.edit(content = f"lượt của <@{id}>",attachments=[discord.File("output.png")])
                turn = 1
                while not board.is_checkmate():
                    try:
                        if turn == 1:
                            def check(msg):
                                return msg.channel == ctx.channel and msg.author.id == ctx.author.id            
                            message = await self.bot.wait_for("message", check=check)
                            
                            if str(message.content) == "chess.out":
                                await ctx.reply("ván cờ đã kết thúc")
                                break
                            else:
                                await message.delete()
                                await push_san(id=str(member.id),a=str(message.content).lower().strip(" "))
                            turn = 2
                        elif turn == 2:
                            def check(msg):
                                return msg.channel == ctx.channel and msg.author.id == member.id
                            message = await self.bot.wait_for("message", check=check)
                            
                            if str(message.content) == "chess.out":
                                await ctx.reply("ván cờ đã kết thúc")
                                break
                            else:
                                await message.delete()
                                await push_san(id = str(ctx.message.author.id), a = str(message.content).lower().strip(" "))
                            turn = 1
                    except Exception as e:
                        print(e)
                        await ctx.reply("nước đi không hợp lệ, vui lòng thử lại", delete_after = 3.5)
                        continue
            except Exception as e:
                print(e)
async def setup(bot):
    await bot.add_cog(Chess(bot))
