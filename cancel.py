import pickledb


async def interactionCancel(interaction):
  db = pickledb.load('logiTicket.json', True)
  message = interaction.message
  ticketnum = int(message.embeds[0].title.split(" #")[1].split(":")[0])
  if str(interaction.user.id)==db.get(str(ticketnum)).split("//")[0]:
    db.rem(str(ticketnum))
    await message.delete()