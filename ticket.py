import discord
import towns
import cancel
import pickledb
db = pickledb.load('logiTicket.json', False)
selectList = [discord.SelectOption(label = 'Error', value ='Error')]


def locationList(locations,index):
  location = str(index)
  for i in range(len(locations)):
    if locations[i][0] == location:
      location = locations[i][1]
      break
  selectListOutput=[]
  for i in range(len(location)):
      selectListOutput.append(discord.SelectOption(label = location[i], value = location[i]))
  return selectListOutput


class InfoButton(discord.ui.View):
  @discord.ui.button(style = discord.ButtonStyle.red, label='Cancel')
  async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await cancel.interactionCancel(interaction)   


async def initialDropDown(interaction,select):
    global ticketnum
    ticketnum = int(interaction.message.embeds[0].title.split(" #")[1].split(":")[0])
    global index
    index = str(select.values[0])    
    db.set(str(ticketnum), db.get(str(ticketnum))+str(index)+"//")
    global selectList
    selectList = locationList(towns.setLocations(),index)
    
    class DropDownTowns(discord.ui.View):
      @discord.ui.select(options = selectList)
      async def click_me_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        db.set(str(ticketnum), db.get(str(ticketnum))+str(select.values[0])+"//")
        embedVar = discord.Embed(title="Order #"+str(ticketnum)+": "+str(index)+", "+str(select.values[0]))
        embedVar.add_field(name="Information: ",value='Type "%info [Amount and item needed with precise location]"')
        title = "Compiling Ticket for: "+str(interaction.user.display_name)
        embedVar.set_author(name=title)
        await interaction.message.delete()
        message = await interaction.channel.send(embed=embedVar, view = InfoButton())
        db.set(str(ticketnum), db.get(str(ticketnum)) + "%" + str(message.id))
     
      @discord.ui.button(style = discord.ButtonStyle.red, label='Cancel')
      async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await cancel.interactionCancel(interaction)     
  
    embedVar = discord.Embed(title="Order #"+str(ticketnum)+":")
    file = discord.File("images/"+index+".png", filename="output.png")
    embedVar.set_image(url="attachment://output.png")
    embedVar.set_footer(text="Select Town and press enter")
    title = "Compiling Ticket for: "+str(interaction.user.display_name)
    embedVar.set_author(name=title)
    await interaction.message.delete()
    await interaction.channel.send(file=file, embed=embedVar,view = DropDownTowns())
    

async def MoreOptions(interaction, level):
  ticketnum = int(interaction.message.embeds[0].title.split(" #")[1].split(":")[0])
  embedVar = discord.Embed(title="Order #"+str(ticketnum)+":")
  file = discord.File("images/map.png", filename="output.png")
  embedVar.set_image(url="attachment://output.png")
  embedVar.set_footer(text="Select Region and press enter")
  title = "Compiling Ticket for: "+str(interaction.user.display_name)
  embedVar.set_author(name=title)
  await interaction.message.delete()
  if level == 0:
    await interaction.channel.send(file=file, embed=embedVar,view = DropDownRegions())
  else:
    await interaction.channel.send(file=file, embed=embedVar,view = MoreDropDownRegions())


class MoreDropDownRegions(discord.ui.View):
  @discord.ui.select(options = towns.setSecondaryRegions())
  async def click_me_select(self, interaction: discord.Interaction, select: discord.ui.Select):
    await initialDropDown(interaction,select)
  
  @discord.ui.button(style = discord.ButtonStyle.grey, label='More Options')
  async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.defer()
    await MoreOptions(interaction, 0)
  
  @discord.ui.button(style = discord.ButtonStyle.red, label='Cancel')
  async def click_me_button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
    await cancel.interactionCancel(interaction)  


class DropDownRegions(discord.ui.View):
  @discord.ui.select(options = towns.setPrimaryRegions())
  async def click_me_select(self, interaction: discord.Interaction, select: discord.ui.Select):
    await initialDropDown(interaction,select)
  
  @discord.ui.button(style = discord.ButtonStyle.grey, label='More Options')
  async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.defer()
    await MoreOptions(interaction, 1)
  
  @discord.ui.button(style = discord.ButtonStyle.red, label='Cancel')
  async def click_me_button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
    await cancel.interactionCancel(interaction)     
        