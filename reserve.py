import discord
import cancel
import complete
import pickledb
db = pickledb.load('logiTicket.json', False)

class reserveButton(discord.ui.View):
    @discord.ui.button(style=discord.ButtonStyle.green, label='Reserve')
    async def click_me_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()                        
        embedVar = interaction.message.embeds[0]
        embedVar.set_footer(text="Reserved By: " + interaction.user.display_name)
        msg = interaction.message
        ticketnum = int(embedVar.title.split(" #")[1].split(":")[0])
        db.set(str(ticketnum), db.get(str(ticketnum)) + "//" + str(interaction.user.id))
        await msg.edit(embed=embedVar, view=complete.completeButton())

    @discord.ui.button(style=discord.ButtonStyle.grey, disabled=True, label='Complete')
    async def click_me_button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        print("Disabled Button")

    @discord.ui.button(style=discord.ButtonStyle.red, label='Cancel')
    async def click_me_button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await cancel.interactionCancel(interaction)
