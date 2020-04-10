import linecache
import os
import random
import asyncio
import discord
from discord.ext import commands  # Bot Commands Frameworkのインポート
from discord.ext import tasks
import json


class MusicBot():
    volume=0.2
    voich=None
    music_queue=[]

# コグとして用いるクラスを定義。
class Idol(commands.Cog,MusicBot):


    def __init__(self, bot):
        self.bot = bot


    def cog_unload(self):
        self.queue_check.cancel()


    @tasks.loop(seconds=3)
    async def queue_check(self):
        if self.voich.is_paused()!=True and len(self.music_queue)>0 and self.voich.is_playing()!=True:
            print("中身あり")
            se=self.music_queue.pop(0)
            if os.path.exists("music/"+se+".mp3"):
                self.voich.play(discord.FFmpegPCMAudio(f'music/{se}.mp3'))
            else:
                self.voich.play(discord.FFmpegPCMAudio(f'music/{se}.m4a'))
            self.voich.source=discord.PCMVolumeTransformer(self.voich.source)
            self.voich.source.volume=self.volume





    @commands.command("カモン")
    async def voice_connect(self, ctx):

       self.voich = await discord.VoiceChannel.connect(ctx.author.voice.channel)

       if random.randint(1,3)==1:
           self.voich.play(discord.FFmpegPCMAudio('music/hayate_desu.m4a'))
       else:
           self.voich.play(discord.FFmpegPCMAudio('music/nagi_aisatsu.m4a'))
       await asyncio.sleep(2)
       self.queue_check.start()


    @commands.command("グッバイ")
    async def voice_disconnect(self, ctx):
       if self.voich.is_playing():
           self.voich.stop()
       self.voich.play(discord.FFmpegPCMAudio("music/hayate_tanosikatta.m4a"))
       await asyncio.sleep(2)
       await self.voich.disconnect()
       self.voich=None
       self.cog_unload()



    @commands.command()
    async def se(self, ctx, se:str):
        if self.voich.is_playing():
            self.voich.stop()
        if os.path.exists("music/"+se+".mp3"):
            self.voich.play(discord.FFmpegPCMAudio(f'music/{se}.mp3'))
        else:
            self.voich.play(discord.FFmpegPCMAudio(f'music/{se}.m4a'))
        self.voich.source=discord.PCMVolumeTransformer(self.voich.source)
        self.voich.source.volume=self.volume

    @commands.command()
    async def skip(self, ctx):
        if self.voich.is_playing():
            self.voich.stop()
            se=self.music_queue.pop(0)
            if os.path.exists("music/"+se+".mp3"):
                self.voich.play(discord.FFmpegPCMAudio(f'music/{se}.mp3'))
            else:
                self.voich.play(discord.FFmpegPCMAudio(f'music/{se}.m4a'))
            self.voich.source=discord.PCMVolumeTransformer(self.voich.source)
            self.voich.source.volume=self.volume

    @commands.command("プレイリスト作成")
    async def playlist_make(self, ctx, se:str):
        if os.path.exists("music/"+se+".mp3")!=True and os.path.exists("music/"+se+".m4a")!=True:
            await ctx.send("SEが存在しません")
            return
        with open("json/bot_id.json","r")as f:
            dic=json.load(f)
        dic[str(ctx.author.id)]["playlist"].append(se)
        queue_list=""
        count=1
        for name in dic[str(ctx.author.id)]["playlist"]:
            queue_list+=f"{count}, {name}"+"\n"+"\n"
            count+=1
        embed = discord.Embed(title="あなたのプレイリスト",description=queue_list)
        embed.set_footer(text="この順番に再生されます")
        await ctx.send(embed=embed)
        with open("json/bot_id.json","w")as f:
            json.dump(dic,f,indent=3)

    @commands.command("プレイリスト削除")
    async def playlist_delete(self, ctx):
        with open("json/bot_id.json","r")as f:
            dic=json.load(f)
            dic[str(ctx.author.id)]["playlist"]=[]
        with open("json/bot_id.json","w")as f:
            json.dump(dic,f,indent=3)

    @commands.command("プレイリスト確認")
    async def playlist_check(self, ctx):
        with open("json/bot_id.json","r")as f:
            dic=json.load(f)
        queue_list=""
        count=1
        for name in dic[str(ctx.author.id)]["playlist"]:
            queue_list+=f"{count}, {name}"+"\n"+"\n"
            count+=1
        embed = discord.Embed(title="あなたのプレイリスト",description=queue_list)
        embed.set_footer(text="この順番に再生されます")
        await ctx.send(embed=embed)

    @commands.command("プレイリスト再生")
    async def playlist_play(self, ctx):
        with open("json/bot_id.json","r")as f:
            dic=json.load(f)
        self.music_queue=dic[str(ctx.author.id)]["playlist"]
        queue_list=""
        count=1
        for name in dic[str(ctx.author.id)]["playlist"]:
            queue_list+=f"{count}, {name}"+"\n"+"\n"
            count+=1
        embed = discord.Embed(title="あなたのプレイリスト",description=queue_list)
        embed.set_footer(text="この順番に再生されます")
        await ctx.send(embed=embed)



    @commands.command("キュー")
    async def queue(self, ctx, se:str):
        if os.path.exists("music/"+se+".mp3")!=True and os.path.exists("music/"+se+".m4a")!=True:
            await ctx.send("SEが存在しません")
            return
        self.music_queue.append(se)
        queue_list=""
        count=1
        for name in self.music_queue:
            queue_list+=f"{count}, {name}"+"\n"+"\n"
            count+=1
        embed = discord.Embed(title="再生リスト",description=queue_list)
        embed.set_footer(text="この順番に再生されます")
        await ctx.send(embed=embed)

    @commands.command()
    async def pause(self, ctx):
        if self.voich.is_playing():
            self.voich.pause()

    @commands.command()
    async def stop(self, ctx):
        if self.voich.is_playing():
            self.voich.stop()
            self.music_queue=[]

    @commands.command()
    async def restart(self, ctx):
        if self.voich.is_playing():
            pass
        else:
            self.voich.resume()

    @commands.Cog.listener()
    async def on_voice_state_update(self,member,before,after):
        if member.bot:
            return
        def check_error(er):
                print('Error check: '+ er)

        if before.channel is None and self.voich!=None:
            if random.randint(1,10)==1:
               self.voich.play(discord.FFmpegPCMAudio('music/ここだよダーリン.m4a'), after=check_error)
            else:
               self.voich.play(discord.FFmpegPCMAudio('music/hayate_yatta.m4a'), after=check_error)

# Bot本体側からコグを読み込む際に呼び出される関数。
def setup(bot):

    bot.add_cog(Idol(bot)) # TestCogにBotを渡してインスタンス化し、Botにコグとして登録する。
