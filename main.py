import os
import pickledb
import discord
import discord.utils
from dotenv import load_dotenv
import ticket
import reserve
db = pickledb.load('logiTicket.json', True)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)


global message_id
global commandChannel
global ticketChannel


commandChannel = 1016682697248223272
ticketChannel = 1016682702629503077


def split(word):
    return [char for char in word]

@client.event
async def on_message(message, user=discord.Member):
  if message.author.id != 915715481112023051:
    if message.content.split(" ")[0] == "%ticket":
      db = pickledb.load('logiTicket.json', True)
      waitmsg= await message.channel.send("```Loading Interface ....```")
      try:
        ticketnum = db.get("TicketNum")
      except(Exception):
        db.set("TicketNum", -1)
        ticketnum = db.get("TicketNum") 
      db.set("TicketNum",ticketnum+1)
      db.set(str(ticketnum) , str(message.author.id)+"//")
      embedVar = discord.Embed(title="Order #"+str(ticketnum)+":")
      file = discord.File("images/map.png", filename="output.png")
      embedVar.set_image(url="attachment://output.png")
      embedVar.set_footer(text="Select Region and press enter")
      title = "Compiling Ticket for: "+str(message.author.display_name)
      embedVar.set_author(name=title)
      await message.channel.send(file=file, embed=embedVar,view = ticket.DropDownRegions())
      await waitmsg.delete()
      await message.delete()

    
    if message.content.split(" ")[0]=="%info":
      db = pickledb.load('logiTicket.json', True)
      channel = message.channel
      keys = str(db.getall()).replace("dict_keys([","").replace("]","").replace("'","").replace(")","").split(", ")
      print(keys)
      for i in range(len(keys)):
        key = str(db.get(keys[i]))
        print(key)
        if key.split("//")[0] == str(message.author.id):
          ticketnum = keys[i]
          break
      messageContent = message.content.split("%info ")[1]
      await message.delete()
      delMessageId = int(db.get(ticketnum).split("%")[1])
      delMessage = await channel.fetch_message(delMessageId)
      await delMessage.delete()
      db.set(ticketnum, db.get(ticketnum).split("%")[0]+messageContent)
      
      channel = await client.fetch_channel(ticketChannel)
      embedVar = discord.Embed(title="Order #"+str(ticketnum)+": "+str(db.get(ticketnum).split("//")[1])+", "+str(db.get(ticketnum).split("//")[2]))
      guild= channel.guild
      user = guild.get_member(int(db.get(ticketnum).split("//")[0]))
      embedVar.add_field(name="```Recipient: ```",value="```"+user.display_name+"```")
      embedVar.add_field(name="```Information: ```",value="```"+str(db.get(ticketnum).split("//")[3])+"```")
      embedVar.set_footer(text="All completion of tickets works on an honesty policy, please do not abuse the system")
      message = await channel.send(embed=embedVar, view = reserve.reserveButton())
      db.set(ticketnum, db.get(ticketnum)+"//"+str(message.id))      

    if message.content.split(" ")[0]=="%lb":
      db = pickledb.load('logiTicket.json', True)
      lb = db.get("lb").split("//")
      lbSplit =[[]]
      for i in range(len(lb)):
        if lb[i] != "":
          lbSplit.append([lb[i][0:18],lb[i][18:len(split(lb[i]))]])
      del lbSplit[0]
      lbSplit = sorted(lbSplit, key=lambda x: x[1], reverse=True)
      for i in range(len(lbSplit)):
        lbSplit[i][0]=message.guild.get_member(int(lbSplit[i][0])).display_name
      print(lbSplit)
      lbOutput=""
      for i in range(10):
        try:
          lbOutput="```#"+str(i+1)+"      "+lbSplit[i][0]+"      "+lbSplit[i][1]+"```\n"
        except:
          break
      embedVar = discord.Embed(title="Leaderboard")
      embedVar.set_footer(text= "- Made by Stolas")
      embedVar.add_field(name="```Place:   Name:   Orders Completed:```",value=lbOutput)
      title = "Top ten"
      embedVar.set_author(name=title)
      await message.channel.send(embed=embedVar)
      await message.delete()
      
      

client.run(TOKEN)