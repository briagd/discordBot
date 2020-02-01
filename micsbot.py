import discord
import json
import praw
import random
import pyowm
import retrieval

with open('data.json') as f:
  data = json.load(f)
discord_id = data['discordID']
client_id = data['redditID']
client_secret = data['redditSecret']
user_agent = data['redditAgent']
owm_key = data['owmKey']


#Instantiate the reddit api
reddit = praw.Reddit(client_id = client_id,
                     client_secret = client_secret,
                     user_agent = user_agent)
#Instantiate the open weather api
owm = pyowm.OWM(owm_key)

#
retrievAns = retrieval.Retrieval()

#create a discord client
client = discord.Client()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author.id == client.user.id: return

    if any(x in  message.content.lower() for x in ["hi", "hello"]):
        await message.channel.send("Hello "+message.author.name+", I hope you come in peace.")

    if "!meme" in message.content.lower():
        subreddit = reddit.subreddit('programmingmemes')
        max_posts = 50
        posts = [post for post in subreddit.hot(limit=max_posts)]
        random_post = posts[random.randint(0, max_posts-1)]
        await message.channel.send(random_post.url)

    if "!joke" in message.content.lower():
        subreddit = reddit.subreddit('Jokes')
        max_posts = 50
        posts = [post for post in subreddit.hot(limit=max_posts)]
        random_post = posts[random.randint(0, max_posts-1)]
        joke = random_post.title + " " + random_post.selftext
        await message.channel.send(joke)

    if "!weather" in message.content.lower():
        obs = owm.weather_at_place('Belval, Luxembourg')
        w = obs.get_weather()
        await message.channel.send(w.get_weather_icon_url())
        status = w.get_detailed_status().lower()
        temperature = w.get_temperature(unit='celsius')['temp']
        await message.channel.send("Today's report is {} and the temperature is {} degrees.".format(status, temperature))

    if "!retrieval" in message.content.lower():
        request = message.content.lower().strip("!retrieval")
        await message.channel.send(retrievAns.response(request))

    if "!help"  in message.content.lower():
        help = open("help.txt", "r")
        await message.channel.send(help.read())

# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

client.run(discord_id)
