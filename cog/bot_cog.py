import asyncio
import json
import os
import random
import re

import discord
import MeCab
from discord.ext import commands  # Bot Commands Frameworkのインポート
from googletrans import Translator
from pykakasi import kakasi

import colla
from language_judge import isalnum
from roma_judge import judge
import wiki_search
from picture_download import download_img

kakasi = kakasi()
num=1
# コグとして用いるクラスを定義。
class Main(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        with open("json/bot_id.json","r")as f:
            self.user_data=json.load(f)


    @commands.group()
    async def role(self, ctx):
        """サブコマンドで数字を選択"""
        # サブコマンドが指定されていない場合、メッセージを送信する。
        if ctx.invoked_subcommand is None:
            await ctx.send('このコマンドにはサブコマンドが必要です。')

    # roleコマンドのサブコマンド
    # 指定したユーザーに指定した役職を付与する。
    @role.command()
    async def add(self, ctx, num1:int, num2:int):
        await ctx.send(num1+num2)

    @commands.command("goodbye")
    async def disconnect(self, ctx):
       await ctx.send("また会いましょう")
       await self.bot.logout()

    @commands.command()
    async def birthday(self, ctx, idol: str):
       """アイドル名を入れると誕生日を出力します"""
       with open("text/birthday.txt","r")as f:
            target=f.readline()
            while target:
                if idol in target:
                    answer=target.split(" - ")
                    break
                else:
                    target=f.readline()

            await ctx.send(answer[0])

    @commands.command()
    async def repeat(self, ctx,word:str,num:int):
        send_word=""
        if(len(word)*num>2000):
            ctx.send("文字数が多いですね。欲張りはダメ、絶対")
        for i in range(num):
            send_word+=word
        await ctx.message.delete()
        ch_webhooks = await ctx.channel.webhooks()
        webhook = discord.utils.get(ch_webhooks, name="久川颯")
        await webhook.send(content=send_word,
                username=ctx.author.display_name,
                avatar_url=ctx.author.avatar_url_as(format="png"))

    @commands.command()
    async def ero(self, ctx):
       with open("text/ero_block.txt","r")as f:
            text=f.read()
            await ctx.send(text)

    @commands.command("リアリティストーン")
    async def reality(self, ctx):
       for member in ctx.guild.members:
           try:
               await member.edit(nick=member.name)
           except discord.Forbidden:
              pass

    @commands.command("パワーストーン")
    async def power(self, ctx,name:str):
       for member in ctx.guild.members:
           try:
               await member.edit(nick=name)
           except discord.Forbidden:
               pass

    @commands.command("俺の誕生日")
    async def my_birthday(self,ctx,text:str):
       with open("../text/mybirthday.txt","a")as f:
            f.write(text+"by"+ctx.author.display_name+"\n")
       await ctx.send(message.author.mention + "覚えました")

    @commands.command("エクスチェンジ")
    async def exchange(self,ctx):
       global num
       ch_webhooks = await ctx.channel.webhooks()
       webhook = discord.utils.get(ch_webhooks, name="久川颯")
       if num==1:
           await webhook.send(content="ど゛う゛し゛て゛な゛ん゛だ゛よ゛お゛お゛ぉ゛お゛！゛！゛！゛ん゛あ゛あ゛あ゛あ゛あ゛ぁ゛ぁ゛あ゛あ゛！゛！゛！゛！゛",
                 username="藤原竜也",
                 avatar_url="https://stat.ameba.jp/user_images/20150306/19/tamagochan-deddosusi/3f/05/j/t02200220_0354035413237066758.jpg?caw=800")
           num=2
       elif num==2:
           await webhook.send(content="凪です",
                 username="久川凪",
                 avatar_url="https://imas.gamedbs.jp/cg/image_sp/card/quest/d30a16b66031de8bce07de107afbd190.png")
           num=3
       elif num==3:
           await webhook.send(content="I am...inevitable",
                 username="サノス",
                 avatar_url="https://contents.newspicks.com/images/news/4210549?updatedAt=20190909142641")
           num=1

    @commands.command()
    async def tf(self, ctx, text: str):

       kakasi.setMode('J', 'H')  # J(Kanji) to H(Hiragana)
       conv = kakasi.getConverter()
       text=conv.do(text)
       fujiwara="゛".join(text)+"゛"
       ch_webhooks = await ctx.channel.webhooks()
       webhook = discord.utils.get(ch_webhooks, name="久川颯")
       await webhook.send(content=fujiwara,
             username="藤原竜也",
             avatar_url="https://stat.ameba.jp/user_images/20150306/19/tamagochan-deddosusi/3f/05/j/t02200220_0354035413237066758.jpg?caw=800")


    @commands.command("分割")
    async def wakati(self, ctx, url: str):
       m = MeCab.Tagger ("-Ochasen ")
       await ctx.send(m.parse(url))

    @commands.command("英語縛り")
    async def funny(self, ctx,id:str):
       with open("json/bot_id.json","r")as f:
           dic=json.load(f)
       if dic[id]["english_switch"]==False:
           await ctx.send(f"いまから<@{id}>は英語しか使えません")
           dic[id]["english_switch"]=True
       else:
           await ctx.send(f"<@{id}>は日本語が使えます")
           dic[id]["english_switch"]=False
       with open("json/bot_id.json","w")as f:
           json.dump(dic,f,indent=3)
       self.user_data=dic

    @commands.command()
    async def funny(self, ctx):
       with open("../text/funny.txt","a")as f:
          f.write(text+"\n")
       await message.channel.send(text+"を追加しました")

    @commands.command()
    async def wiki(self,ctx,word:str):
        await ctx.send(wiki_search.wikipediaSearch(word))

    @commands.command()
    async def gold(self,ctx):
        with open("json/bot_id.json","r")as f:
            gold= json.load(f)
        await ctx.send(str(gold[str(ctx.author.id)]["gold"])+"みつは")



    @commands.command("占い")
    async def fortune(self, ctx):
       with open("json/bot_id.json","r")as f:
           fortune_judge= json.load(f)
       if fortune_judge[str(ctx.author.id)]["fortune"]==True:
           await ctx.send("占いは1日1回までです。欲張ってはいけません")
           return

       dice = random.randint(1, 101) #出る目を指定
       if dice==1:
           fortune_print=["超大吉","daidaikiti"]


       elif dice>1 and dice<11:
           fortune_print=["大吉","daikiti"]
       elif dice>10 and dice<25:
           fortune_print=["中吉","tyukiti"]
       elif dice>24 and dice<50:
           fortune_print=["小吉","syokiti"]
       elif dice>49 and dice<75:
           fortune_print=["吉","kiti"]
       elif dice>74 and dice<93 :
           fortune_print=["凶","kyo"]
       elif dice>92 and dice<100:
           fortune_print=["大凶","daikyo"]
       else:
           fortune_print=["まゆ吉","daidaidaidaikiti"]
       fortune_list=[]
       directory = os.listdir('picture/fortune')
       directory=sorted(directory)
       for i in directory:
           if i.startswith(fortune_print[1]):
               fortune_list.append(i)
       text=random.choice(fortune_list)

       await ctx.send(fortune_print[0])
       await ctx.send(file=discord.File(f"picture/fortune/{text}"))
       fortune_judge[str(ctx.author.id)]["fortune"]=True
       with open("json/bot_id.json","w")as f:
           json.dump(fortune_judge, f, indent=3)
       self.user_data=fortune_judge



    @commands.command()
    async def slot(self, ctx):
        with open("json/bot_id.json","r")as f:
            gold= json.load(f)
        emoji=""
        judge=[]
        ei=[688263713228455942,688264142360281145,688263965926883356]
        if gold[str(ctx.author.id)]["gold"]<100:
            await ctx.send("みつはが足りません")
            return
        else:
            gold[str(ctx.author.id)]["gold"]-=100
            await ctx.send("100みつはを使いました")

        for i in range(3):
            emoji += str(self.bot.get_emoji(692396383000592384))
        msg=await ctx.send(emoji)
        await asyncio.sleep(2)
        await msg.delete()
        emoji=""

        for i in range(3):
            ran=random.choice(ei)
            judge.append(ran)
            emoji += str(self.bot.get_emoji(ran))
        await ctx.send(emoji)
        if judge[0]==judge[1] and judge[1]==judge[2]:
            await ctx.send("あたり！300みつはゲット！")
            gold[str(ctx.author.id)]["gold"]+=300
        with open("json/bot_id.json","w")as f:
            json.dump(gold, f, indent=3)
        self.user_data=gold

    @commands.command("送金")
    async def send_money(self, ctx,user_id:int,money:int):
        with open("json/bot_id.json","r")as f:
            gold= json.load(f)
        if gold[str(ctx.author.id)]["gold"]<money:
            await ctx.send("お金が足りません。しくしく")
            return
        else:
            gold[str(ctx.author.id)]["gold"]-=money
            gold[str(user_id)]["gold"]+=money
        with open("json/bot_id.json","w")as f:
            json.dump(gold, f, indent=3)
        me=self.bot.get_user(user_id)
        await ctx.send(me.mention+f"に{money}みつは送金しました")
        self.user_data=gold


    @commands.Cog.listener()
    async def on_member_join(self,member):
         channel = discord.utils.get (member.guild.text_channels, name="玄関")
         server=member.guild
         e=discord.Embed (description="ようこそ！")
         e.add_field (name="参加ありがとうございます。", value=f"{member.mention}", inline=False)
         await channel.send (embed=e)

    @commands.command()#メンバー登録
    async def member(self, ctx):
       with open("json/bot_id.json","r")as f:
           dic=json.load(f)
       for member in ctx.guild.members:
           if member.bot :
               pass
           else:

               dic[str(member.id)]["fortune"]=False
               # dic[member.id]={"gold":10000,"english_switch":False,"fortune":False,"birthday":None}

       with open("json/bot_id.json","w")as f:
           json.dump(dic, f, indent=3)

    @commands.Cog.listener()
    async def on_member_update(self,before,after):
        channel = self.bot.get_channel(658856327019495475)
        if before.display_name!= after.display_name:
            if after.display_name=="ランダム":
                res = gt.main()
                await after.edit(nick=res[0:20])
            else:
                msg = before.display_name+"が"+after.display_name+"に名前を変えたようですよ、ご主人様"
                await channel.send(msg)

    @commands.Cog.listener()
    async def on_reaction_add(self,reaction,user):
        if reaction.count==1:
           if reaction.emoji =="🇺🇸":
                translator = Translator()
                trans_en = translator.translate(reaction.message.content, src='ja', dest='en')
                await reaction.message.channel.send(trans_en.text)
           elif reaction.emoji =="🇯🇵":
               translator = Translator()
               lang=translator.detect(reaction.message.content)
               trans_en = translator.translate(reaction.message.content, src=lang.lang, dest='ja')
               await reaction.message.channel.send(trans_en.text)

           elif reaction.emoji =="🇮🇹":
               translator = Translator()
               trans_en = translator.translate(reaction.message.content, src='ja', dest='it')
               await reaction.message.channel.send(trans_en.text)

    @commands.Cog.listener()
    async def on_message(self, message):
      if message.author.bot:
         return

      print(message.content+"by"+message.author.display_name)

      if (isalnum(message.content)!=True or judge(message.content)!=True) and self.user_data[str(message.author.id)]["english_switch"]==True:
         await message.delete()


      if message.attachments:
          if message.content=="ミリシタコラ":
              download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.mirikora2()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))
          elif message.content=="バジリスク":

              download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.bazirisuku()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))
          elif message.content=="デレステコラ":

              download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.deresute_kora()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))
          elif message.content=="優しい世界観":

              download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.ppp()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))
          elif message.content=="全員アウト":

              download_img(message.attachments[0].url, "picture/colla/image.png")
              colla.out()
              await message.delete()
              await message.channel.send(file=discord.File("picture/colla/new.png"))

      if "肇ちゃん" in message.content:
         dice = str(random.randint(1,48))  #出る目を指定
         await message.channel.send(file=discord.File(f"picture/hajime/{dice.zfill(3)}.jpg"))

      if "ちえり" in message.content:
         dice = str(random.randint(1,48)) #出る目を指定
         await message.channel.send(file=discord.File(f"picture/chery/{dice.zfill(3)}.jpg"))

      if "!random" in message.content:
          text=message.content.split("!random")
          num=random.randint(0,100)
          await message.channel.send(text[0]+str(num)+text[1])



def setup(bot):
    bot.add_cog(Main(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
