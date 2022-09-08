import pickledb
db = pickledb.load('logiTicket.json', False)

db.set("TicketNum",0)
db.set("lb","//")
for i in range(len(db.getall())+100):
  try:
    if i<=100: 
      print(str(i)+"%")
    db.rem(str(i))
  except:
    i=i

