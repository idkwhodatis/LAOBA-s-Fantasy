# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import requests
from youtube_dl import YoutubeDL
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.ext.commands.errors import ClientException


client=commands.Bot(command_prefix="-")

@client.command()
async def play(ctx,url):
    if ctx.message.author.voice is not None:
        try:
            await ctx.message.author.voice.channel.connect()
        except ClientException:
            pass
    else:
        await ctx.message.channel.send("Please join a voice channel first.")
        return

    YDL_OPTIONS={'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice=get(client.voice_clients, guild=ctx.guild)

        
    if url.startswith("https://www.youtube.com/"):
        if url.startswith("https://www.youtube.com/shorts/"):
            url=url.replace("shorts/","watch?v=")
        info=YoutubeDL(YDL_OPTIONS).extract_info(url, download=False)
        song=info["formats"][0]
        URL=song["url"]
        await ctx.message.channel.send("Playing: "+info["title"])
    elif url.startswith("https://music.163.com/#/song?id="):
        id=url[url.find("id")+3:]
        info=requests.get("http://127.0.0.1:3000/song/detail?ids="+id).json()
        if info["songs"][0]["fee"]==0 or info["songs"][0]["fee"]==8:
            song=requests.get("http://127.0.0.1:3000/song/url?id="+id).json()
            URL=song["data"][0]["url"]
        else:
            await ctx.message.channel.send("VIP only on Netease music, playing on Youtube instead.")
            keywords=info["songs"][0]["name"]
            for i in info["songs"][0]["ar"]:
                keywords+=" "+i["name"]
            song=YoutubeDL(YDL_OPTIONS).extract_info(f"ytsearch:{keywords}", download=False)["entries"][0]
            URL=song["url"]
        await ctx.message.channel.send("Playing: "+info["songs"][0]["name"]+" - "+"/".join([i["name"] for i in info["songs"][0]["ar"]]))
    else:
        await ctx.message.channel.send("Please enter link of a Netease music song or Youtube video")
        return

    if voice.is_playing():
        voice.stop()
    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    voice.is_playing()

@client.command()
async def search(ctx,*args):
    if ctx.message.author.voice is not None:
        try:
            await ctx.message.author.voice.channel.connect()
        except ClientException:
            pass
    else:
        await ctx.message.channel.send("Please join a voice channel first.")

    YDL_OPTIONS={'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS={'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice=get(client.voice_clients, guild=ctx.guild)

    keywords=" ".join(args)
    id=str(requests.get("http://127.0.0.1:3000/search?keywords="+keywords+"&limit=1").json()["result"]["songs"][0]["id"])
    
    info=requests.get("http://127.0.0.1:3000/song/detail?ids="+id).json()
    if info["songs"][0]["fee"]==0 or info["songs"][0]["fee"]==8:
        song=requests.get("http://127.0.0.1:3000/song/url?id="+id).json()
        URL=song["data"][0]["url"]
    else:
        await ctx.message.channel.send("VIP only on Netease music, playing on Youtube instead.")
        keywords=info["songs"][0]["name"]
        for i in info["songs"][0]["ar"]:
            keywords+=" "+i["name"]
        song=YoutubeDL(YDL_OPTIONS).extract_info(f"ytsearch:{keywords}", download=False)["entries"][0]
        URL=song["url"]
    await ctx.message.channel.send("Playing: "+info["songs"][0]["name"]+" - "+"/".join([i["name"] for i in info["songs"][0]["ar"]]))

    if voice.is_playing():
        voice.stop()
    voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    voice.is_playing()

@client.command()
async def join(ctx):
    if ctx.message.author.voice is not None:
        try:
            await ctx.message.author.voice.channel.connect()
        except ClientException:
            await ctx.message.channel.send("Already connected to a voice channel.")
    else:
        await ctx.message.channel.send("Please join a voice channel first.")

@client.command()
async def stop(ctx):
    voice=discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    await client.voice_clients[0].disconnect()

@client.command()
async def laoba(ctx):
    await ctx.message.channel.send("奥里给干了兄弟们!")

@client.command()
async def test(ctx):
    print(ctx.channel)

client.run("Your Token")
