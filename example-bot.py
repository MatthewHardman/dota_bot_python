# This example requires the 'message_content' intent.
from keys import CLIENT_ID
import discord
from discord import app_commands
import  asyncio
from asyncio import sleep 

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


stack_size_global = 0
user_id_global = []
interaction_user_global = ""

@tree.command(name = "ping", description = "replies with pong", guild=discord.Object(id=1072559368735817799))
async def ping(interaction):
    await interaction.response.send_message("pong!")


@tree.command(name = "dotapy", description="pings dota people", guild=discord.Object(id=1072559368735817799))
@app_commands.describe(stack_size = "The number of people you want to play", time_out = "The time you're willing to wait - in minutes")
async def dotapy(interaction, stack_size: app_commands.Range[int, 2, 5], time_out: app_commands.Range[int, 1, 60]):
    global stack_size_global 
    global interaction_user_global
    await interaction.response.send_message("React please")
    msg = await interaction.original_response()
    interaction_user_global = interaction.user.id
    await msg.add_reaction('👍')
    
    stack_size_global = stack_size
    
    await asyncio.sleep(time_out*60)
    await msg.edit(content="This message will now self-destruct")
    await asyncio.sleep(5)
    #channel = msg.channel
    #def check(reaction, user):
    #    return str(reaction.emoji) == '👍'
    #try:
    #    reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=check)
    #except asyncio.TimeoutError:
    #    await channel.send('no reaction')
    #else:
    #    await channel.send('you reacted!')


@client.event
async def on_ready():
    commands = await tree.sync(guild=discord.Object(id = 1072559368735817799))
    print(f'Ready, {len(commands)} uploaded')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@client.event
async def on_reaction_add(reaction, user):
    global user_id_global
    global interaction_user_global
    msg = reaction.message
    if msg.author != client.user or str(reaction.emoji) != '👍':
        return
    if msg.content.startswith('React'):
        user_id_global.append(user.id)
        if reaction.count == stack_size_global:
            user_id_global[0] = interaction_user_global
            reply_message = 'These people reacted: '
            for i in user_id_global:
                reply_message += " " + "<@"+str(i)+">"
            await msg.channel.send(f"{reply_message}")
            await msg.delete()
            user_id_global.clear()

@client.event
async def on_reaction_remove(reaction, user):
    global user_id_global
    msg = reaction.message
    if msg.author != client.user or str(reaction.emoji) != '👍':
        return
    if msg.content.startswith('React'):
        user_id_global.remove(user.id)

@client.event
async def on_app_command_completion(interaction, command):
    global user_id_global 
    if command.name != "dotapy" or len(user_id_global) == 0:
        return
    await interaction.channel.send("Not enough people reacted")
    user_id_global.clear()
    msg = await interaction.original_response()
    await msg.delete()





client.run(CLIENT_ID)
