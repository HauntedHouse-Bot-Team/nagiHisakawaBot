from discord.ext import commands  # Bot Commands Frameworkのインポート
import discord
import random
import re
import linecache
import csv
from discord.utils import get

# コグとして用いるクラスを定義。
class Idol(commands.Cog):


    def __init__(self, bot):
        self.bot = bot

    






    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot:
         return
      if re.search(r'肇ちゃん',message.content):
         dice = str(random.randint(1,48))  #出る目を指定
         await message.channel.send(file=discord.File(f"../pictures/hajime/{dice.zfill(3)}.jpg"))

      if re.search(r'ちえり',message.content):
         dice = str(random.randint(1,48)) #出る目を指定
         await message.channel.send(file=discord.File(f"../pictures/chery/{dice.zfill(3)}.jpg"))
# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):
    bot.add_cog(Idol(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
