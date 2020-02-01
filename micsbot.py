import discord
import json
import praw
import random
import pyowm

with open('data.json') as f:
  data = json.load(f)
discord_id = data['discordID']
client_id = data['redditID']
client_secret = data['redditSecret']
user_agent = data['redditAgent']
owm_key = data['owmKey']



reddit = praw.Reddit(client_id = client_id,
                     client_secret = client_secret,
                     user_agent = user_agent)
owm = pyowm.OWM(owm_key)



client = discord.Client()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):

    if message.author.id == client.user.id: return

    if any(x in  message.content.lower() for x in ["hi", "hello"]):
        await message.channel.send("Hello friend, I hope you come in peace.")

    if "!meme" in message.content.lower():
        subreddit = reddit.subreddit('programmingmemes')
        max_posts = 50
        posts = [post for post in subreddit.hot(limit=max_posts)]
        random_post = posts[random.randint(0, max_posts-1)]
        #for post in posts:
          #image_urls.append(post.url.encode('utf-8'))
        await message.channel.send(random_post.url)

    if "!weather" in message.content.lower():
        obs = owm.weather_at_place('Belval, Luxembourg')
        w = obs.get_weather()
        await message.channel.send(w.get_weather_icon_url())
        status = w.get_detailed_status().lower()
        temperature = w.get_temperature(unit='celsius')['temp']
        await message.channel.send("Today's report is {} and the temperature is {} degrees.".format(status, temperature))

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
