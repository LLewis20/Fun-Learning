import datetime
import os
import news
import time
import asyncio
import discord
from discord.ext import commands
from discord import Interaction
from dotenv import load_dotenv



client = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@client.event
async def on_ready():
    await client.tree.sync()
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="NWMSU Media"), status=discord.Status.do_not_disturb)
    print(f"{client.user.name} is ready to report the news!")


@client.command()
async def hello(ctx):
    await ctx.send("Hello! I'm a bot that reports the news!")



# FINISH : FIX LIMIT PARAMETER OR FIGURE OUT WHY IT DOESN'T WORK
# TODO : FIND A WAY TO CONSTANTLY UPDATE THE NEWS WHEN NEW ARTICLES ARE POSTED
# TODO : FIND ANOTHER COMMAND TO ADD TO THE BOT
# TODO : ADD A COMMAND TO GET THE WEATHER FORECAST FOR THE WEEK
# TODO : ADD A COMMAND TO GET THE WEATHER FORECAST FOR THE DAY
# TODO : ADD A COMMAND FOR CREATING EVENTS FROM THE NORTHWEST CALENDAR





@client.tree.command(name='get_news', description='Get the latest news from the Northwest Missourian')
async def get_news(Interaction: Interaction, number_of_articles : int = None, month : int = datetime.datetime.now().month, year : int = datetime.datetime.now().year):

    # slow the interaction
    await Interaction.response.defer()

    loop = asyncio.get_event_loop()

    # run get_articles in an executor
    articles = await loop.run_in_executor(None, lambda: list(news.get_articles(number_of_articles, month, year)))

    # iterate over the articles and send each one as it is received
    for article_details in articles:
        embed = discord.Embed(color=discord.Color.brand_green(),
                              title=article_details['title'], 
                              url=article_details['link'],
                              description=article_details['description']
                              )
        embed.set_image(url=article_details['image_url'])
        embed.set_author(name=article_details['author'], url="https://www.nwmissouri.edu/media/news/", icon_url="https://www.nwmissouri.edu/marketing/images/design/logos/samp-N60-2Stack-Full.jpg")
        embed.set_footer(text=article_details['date'])
        await Interaction.followup.send(embed=embed)


load_dotenv()
client.run(os.getenv("TOKEN"))