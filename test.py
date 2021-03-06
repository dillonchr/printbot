import os
import discord
from discord.ext import commands
import requests
import uuid
from wand.image import Image
from dotenv import load_dotenv
import datetime

load_dotenv()
bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def question(ctx, *args):
    await ctx.send("go ahead, caller. i'm listening")
    print_text(f"[=]Q\n\n{' '.join(args)}")


def print_text(content):
    now = datetime.datetime.now()
    os.system("echo {} > /dev/usb/lp0".format(now))
    path = f"/tmp/{uuid.uuid4()}.txt"
    with open(path, "w") as file:
            file.write(str(content))    
    os.system("cat {} | python /home/pi/pppppprint/print.py > /dev/usb/lp0".format(path))


def print_contents(message):
    print_text(message.content)


@bot.listen()
async def on_message(message):
    if not message.author.bot and message.channel.type == discord.ChannelType.private and not message.content.startswith(">"):
        if not message.attachments or message.attachments.count == 0:
            print_contents(message)
            await message.reply("hello")
        else:
            for a in message.attachments:
                url = a.proxy_url
                ext = url.split(".").pop()
                if ext.lower() in ("png", "jpg", "jpeg", "gif", "jfif", "webp", "bmp", "tif", "tiff"):
                    content = requests.get(url)
                    image_path = f"/tmp/{uuid.uuid4()}.{ext.lower()}"
                    converted_path = image_path + ".conv.png"
                    open(image_path, "wb").write(content.content)
                    try:
                        i = Image(filename=image_path)
                        i.transform(resize="400")
                        i.strip()
                        i.brightness_contrast(30, 100)
                        i.transform_colorspace("gray")
                        i.ordered_dither(threshold_map="h6x6a")
                        c = i.convert("png")
                        c.save(filename=converted_path)
                        await message.reply(converted_path)
                        print_contents(message)
                        os.system(f"/home/pi/png2pos/prrrrint.sh {converted_path}")
                    except Exception as e:
                        print(f"{e}")


bot.run(os.environ["BOT_KEY"])
