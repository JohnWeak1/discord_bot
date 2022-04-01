from datetime import datetime
import database


def findMember(name,guild):
    for mem in guild.members:
        if mem.nick != None:
            memName = mem.nick
        else:
            memName = mem.name

        if memName.lower().find(name) != -1:
            return mem


def staytime(member):
    return (datetime.now() - member.joined_at.replace(tzinfo=None)).days


def getTotalXp(member):
    return staytime(member)*0.75 + database.getmsgcount(member.id)*2 + database.getvoicecount(member.id)/120

def progressBar(i,max):
    nbr = (i/max)*200
    str = ""
    for x in range(20):
        if nbr >= 10:
            str += "█"
        elif nbr > 5:
            str += "▄"
        else:
            str += "‌‍‍─"
        nbr -= 10

    return str