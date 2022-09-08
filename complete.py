import discord
import cancel
import reserve
import pickledb


def split(word):
    return [char for char in word]

class completeButton(discord.ui.View):
  @discord.ui.button(style = discord.ButtonStyle.grey, label="Unreserve")
  async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    db = pickledb.load('logiTicket.json', True)
    await interaction.response.defer()                        
    embedVar = interaction.message.embeds[0]
    embedVar.set_footer(text="All completion of tickets works on an honesty policy, please do not abuse the system")
    msg = interaction.message
    ticketnum = int(embedVar.title.split(" #")[1].split(":")[0])
    dbContent = db.get(str(ticketnum)).split("//")
    if dbContent[5] == str(interaction.user.id):
      del dbContent[5]
      dbContentConc=""
      for i in range(len(dbContent)):
        dbContentConc = dbContentConc+dbContent[i]+"//"
      dbContentConc = dbContentConc+"%<><>!"
      db.set(str(ticketnum), dbContentConc.replace("//%<><>!",""))
      await msg.edit(embed=embedVar, view=reserve.reserveButton())
  
  @discord.ui.button(style = discord.ButtonStyle.green, label='Complete')
  async def click_me_button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
    db = pickledb.load('logiTicket.json', True)
    ticketnum = int(interaction.message.embeds[0].title.split(" #")[1].split(":")[0])
    if str(interaction.user.id)==db.get(str(ticketnum)).split("//")[5]:
      channel = interaction.channel
      message = "<@"+str(db.get(str(ticketnum)).split("//")[0])+"> ```Your Order (#"+str(ticketnum)+") was completed by: "+interaction.user.display_name+"```"
      await channel.send(message)
      leaderboard = db.get("lb")
      lb = leaderboard.split("//")
      del lb[0]
      leaderboard="//"
      x=0
      for i in range(len(lb)):
        if lb[i][0:18] == str(db.get(str(ticketnum)).split("//")[5]):
          lbSplit=split(lb[i])
          score=""
          for z in range(18, len(lbSplit)):
            score=score+lbSplit[z]
          score=str(int(score)+1)
          lbConc=""
          for k in range(len(lbSplit)-len(split(score))):
            lbConc=lbConc+lbSplit[k]
          lbConc+=score
          lb[i]=lbConc
          print(lb[i])
          for i in range(len(lb)):
            leaderboard = leaderboard+lb[i]+"//"
          db.set("lb", leaderboard.replace("////","//"))
          break
        else:
          x+=1
      if x == len(lb):
        db.set("lb", db.get("lb")+str(db.get(str(ticketnum)).split("//")[5])+"1//")
      db.rem(str(ticketnum))    
      await interaction.message.delete()
    

  @discord.ui.button(style = discord.ButtonStyle.red, label='Cancel')
  async def click_me_button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
    await cancel.interactionCancel(interaction)     