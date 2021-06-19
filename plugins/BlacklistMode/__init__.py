import discord
from discord.ext import commands

from Plugin import AutomataPlugin

BLACKLIST_MODE = True #can be set to True/Fale based on requirements

class BlacklistMode(AutomataPlugin):
  """Special security system to protect your server from profanity (and other blacklisted terms)"""
  @client.event
  async def on_message(message):
    if message.author == client.user:
      return #ignore what bot says in server so no message loop
    channel = message.channel
  if BLACKLIST_MODE:
    blackList =                                                                                                                                                                         ["","swine","asshole","bitch","wtf", "wot thy fuck", "suicide", "kill", "bad", "bruh", "sucks", "wth", "blyat", "delet", "idk", "fuck", "shit", "bastard", "retard", "shit", "haramjada", "damn", "bruh", "lmao", "hentai", "perv", "idiot", "baka", "blin", "heck", "milf", "sex"] #place swear words and restricted words in this list. Or use a .txt file or external source.

  if any(word in message.content.lower() for word in blackList):
    await message.delete()
