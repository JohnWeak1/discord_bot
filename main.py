import nextcord
from nextcord import Interaction
from nextcord.utils import get
from nextcord.ext import commands
import threading
from mcstatus import MinecraftServer
from datetime import datetime
import dropDowns
import database
import time
import func
import json



f = open("bot_config.json", "r")

TOKEN = json.load(f)["token_alt"]

intents = nextcord.Intents.default()

intents.members = True
intents.guild_messages = True
intents.messages = True
intents.guilds = True


client = commands.Bot(command_prefix=";",intents=intents)


print("launching")



@client.event
async def on_ready():
    print("ready {0.user}".format(client))
    database.initdatabase()
    global server
    server = client.get_guild(717100212027392080)


@client.slash_command(guild_ids=[521256432058761226,717100212027392080])
async def mc(interaction : Interaction):
    embed = nextcord.Embed(title="MC server status :", color=0x88ff00)
    embed.set_footer(text="requested by: " + interaction.user.name + " ")
    embed.timestamp = datetime.now()
    server = MinecraftServer.lookup("fuckoffpls.ddns.net")
    async with interaction.channel.typing():
        try:
            status = server.status()
            query = server.query()
            if status.players.online != 0:
                ply = '\n'.join(query.players.names)
                embed.add_field(name=f"players ({status.players.online}/{status.players.max})) :",value=f"`{ply}`",inline=False)
            else:
                embed.add_field(name=f"players (0/{status.players.max}):",value="`no players`",inline=False)

            embed.add_field(name="ip :",value="fuckoffpls.ddns.net",inline=True)
            embed.add_field(name="version :", value=f"{status.version.name}",inline=True)


        except:
            embed.color = 0xff0000
            embed.add_field(name="Server is offline",value="sorry for the inconvenience but the minecraft server is offline")

    await interaction.response.send_message(embed=embed,delete_after=30)


@client.user_command(guild_ids=[521256432058761226,717100212027392080],name="role profile")
async def role_profile(interaction : Interaction,member : nextcord.Member):



    embed = nextcord.Embed(color=0x3dfc03)
    embed.set_footer(text="requested by: " + interaction.user.name + " ")
    embed.timestamp = datetime.now()

    if member != None:
        msgCount = database.getmsgcount(member.id)
        voiceCount = database.getvoicecount(member.id)
        strtime = time.strftime('%H:%M:%S', time.gmtime(voiceCount))
        min, sec = divmod(voiceCount, 60)
        totalXP = round(func.getTotalXp(member))
        days = func.staytime(member)
        if member.nick != None:
            title = member.nick + "'s role status"
        else:
            title = member.name + "'s role status"
        embed.title = title
        if totalXP != "none":

            if totalXP < 500:
                bar = func.progressBar(totalXP, 500)
                embed.add_field(name="totalXP :",value=f"{totalXP}┤{bar}├500",inline=False)
            elif totalXP < 1500:
                bar = func.progressBar(totalXP, 1500)
                embed.add_field(name="totalXP :",value=f"{totalXP}┤{bar}├1500",inline=False)
            else:
                bar = func.progressBar(totalXP, 4500)
                embed.add_field(name="totalXP :",value=f"{totalXP}┤{bar}├4500",inline=False)

            if member.guild_avatar != None:
                embed.set_thumbnail(url=member.guild_avatar.url)
            elif member.avatar != None:
                embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="staytime :", value=f"{days} days\n({round(days*0.75)} xp)")
            embed.add_field(name="messages :", value=f"{msgCount} messages\n({msgCount*2} xp)")
            embed.add_field(name="voice :", value=f"{strtime} \n({round(voiceCount/120)} xp)")
        else:
            embed.description = "that person does not have any xp"
            embed.color = 0xff0000


    await interaction.response.send_message(embed=embed,delete_after=30)

@client.slash_command(guild_ids=[521256432058761226,717100212027392080], description="example: /poll 'how are y'all ?' 'good;bad:ok'")
async def poll(interaction : Interaction, tittle : str, choices : str):
    choicesAr = choices.split(";")

    embed = nextcord.Embed(title=f"{tittle}", description="vote results :")

    for choice in choicesAr:
        embed.add_field(name=f"{choice} (0%):",value="no votes",inline=False)

    View = dropDowns.dropdown(choicesAr, tittle)



    await interaction.response.send_message("poll :",embed=embed,view=View,delete_after=43200)



@client.event
async def on_message(msg):
    await client.process_commands(msg)
    if msg.author == client.user:
        return


    database.addmessage(msg.author.id)

    role = msg.guild.get_role(918592356058558534)
    role2 = msg.guild.get_role(735163816253325372)
    role3 = msg.guild.get_role(920757941328551976)

    if role not in msg.author.roles:
        if func.getTotalXp(msg.author) > 500:
            await msg.author.add_roles(role, reason="promotion")
    elif role2 not in msg.author.roles:
        if func.getTotalXp(msg.author) > 1500:
            await msg.author.add_roles(role2,reason="promotion")
    elif role3:
        if func.getTotalXp(msg.author) > 4500:
            await msg.author.add_roles(role2,reason="promotion")

    print(msg.content)




@client.event
async def on_member_join(member):
    print("member join: " + member.name)
    channel = client.get_channel(735176471378788383)

    title = "Welcome, " + member.name
    desc = "Welcome to : " + member.guild.name
    embed = nextcord.Embed(title=title, description=desc, color=0x00ff26)
    embed.timestamp = datetime.now()

    await channel.send(embed=embed)
    await member.add_roles(get(member.guild.roles, id=735173045882322955))


@client.event
async def on_member_remove(member):
    print("member leave: " + member.name)
    channel = client.get_channel(735176471378788383)

    tittle = "Goodbye, " + member.name
    embed = nextcord.Embed(title=tittle, description="We hope you enjoyed your stay", color=0xff0000)
    embed.timestamp = datetime.now()

    await channel.send(embed=embed)




def timedcheck():
    threading.Timer(5.0, timedcheck).start()
    if client.is_ready():
        for vc in server.voice_channels:
            for member in vc.members:
                if not member.voice.deaf and not member.voice.self_deaf and not member.voice.afk:
                    database.addvoice(member.id,5)


timedcheck()



client.run(TOKEN)