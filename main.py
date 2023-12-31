

import discord
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)



sad_words = ['sad', "depressed", 'unhappy', "angry", 'miserable', 'depressing']

starter_encouragements = [
    'Cheer up!', "Hang in there.", "You are a great person / bot!"
]

help_command = ['$inspire to get a inspiration, $add to add a encouragement, $list to list all encouragements early added and $del to delete']

my_secret = os.environ['Encourage_Bot']

if 'responding' not in db.keys():
  db['responding'] = True


def get_quote():
  response = requests.get('https://zenquotes.io/api/random')
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + ' -' + json_data[0]['a']
  return quote


def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db['encouragements']
    encouragements.append(encouraging_message)
    db['encouragements'] = encouragements
  else:
    db['encouragements'] = [encouraging_message]


def delete_encouragements(index):
  encouragements = db['encouragements']
  if len(encouragements) > index:
    del encouragements[index]
    db['encouragements'] = encouragements


@client.event
async def on_ready():
  print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if db['responding']:
    options = starter_encouragements
    if 'encouragements' in db.keys():
      options = options + db['encouragements'].value

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith('$add'):
    encouraging_message = msg.split('$add', 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send('New encouraging message added.')

  if msg.startswith('$del'):
    encouragements = []
    if 'encouragements' in db.keys():
      index = int(msg.split('$del', 1)[1])
      delete_encouragements(index)
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  if msg.startswith('$list'):
    encouragements = []
    if 'encouragements' in db.keys():
      encouragements = db['encouragements']
    await message.channel.send(encouragements)

  if msg.startswith('$responding'):
    value = msg.splt('$responding ', 1)[1]
    if value.lower() == 'true':
      db['responding'] = True
      await message.channel.send('Re sponding is on.')
    else:
      db['respoding'] = False
      await message.channel.send('Responding is off.')
  if msg.startswith('$help'):
    await message.channel.send(help_command)


keep_alive()
client.run(os.getenv("Encourage_Bot"))
