import discord
from discord.ext import commands
import asyncio
import re

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='.', intents=intents)
search_cooldown = commands.CooldownMapping.from_cooldown(1, 8.0, commands.BucketType.user)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)

@client.command()
async def search(ctx, *, query):
    bucket = search_cooldown.get_bucket(ctx.message)
    retry_after = bucket.update_rate_limit()
    if retry_after:
        embed = discord.Embed(title="Wait", description=f"On Cooldown\nWait 8 seconds to use that command again.", color=discord.Color.red())
        cooldown_msg = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await cooldown_msg.delete()
    else:
        formatted_query = query.replace(" ", "+")
        search_link = f"https://letmegooglethat.com/?q={formatted_query}"
        await ctx.send(search_link)

@client.command()
async def say(ctx, *, message):
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("<:8533clown:1181520634380034059>")
        return

    command_parts = message.split(",", 1)
    if len(command_parts) < 2:
        await ctx.send("https://cdn.discordapp.com/attachments/1216295263828705400/1218054787296133181/image0.jpg?ex=660644eb&is=65f3cfeb&hm=14c036fdd4b298b14ad7d7e99ff7e70fcad184c07bf7dce7d6cdb22762bf1c7f& ")
        return
    
    title, description = map(str.strip, command_parts)
    
    if title.startswith('.say'):
        title = title[len('.say'):].strip()
    
    embed = discord.Embed(title=title, description=description, color=0xFFFFFF)
    await ctx.send(embed=embed)
    
    await ctx.message.delete()

@client.command()
async def cframe(ctx, *, message):
    if ctx.channel.id != 1217930874142588938:
        embed = discord.Embed(title="Warn", description="This command can only be used in <#1217930874142588938>.", color=discord.Color.orange())
        response = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await response.delete()
        return
# .
    if '.' not in message and '-' not in message and ',' not in message:
        embed = discord.Embed(title="Warn", description="Message must contain at least one of '.', '-' or ','.", color=discord.Color.orange())
        response = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await response.delete()
        return

    split_message = re.split(r'[.,-]', message)
    cframe_values = [float(part.strip()) for part in split_message if part.strip().replace('.', '').replace('-', '').isdigit()]

    if len(cframe_values) == 0:
        embed = discord.Embed(title="Warn", description="Message must contain at least one numerical value.", color=discord.Color.orange())
        response = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await response.delete()
        return
# string ikura do this it's lua
    cframe_str = f"game:GetService('Players').LocalPlayer.Character.HumanoidRootPart.CFrame = CFrame.new({', '.join(map(str, cframe_values))})"
    
    author_mention = ctx.author.mention
    embed = discord.Embed(title="CFrame Teleport", description=f"{author_mention}\n```lua\n{cframe_str}\n```", color=0x00ff00)
    await ctx.send(embed=embed)

@client.command()
async def pivotto(ctx, *, path):
    if ctx.channel.id != 1217930874142588938:
        embed = discord.Embed(title="Warn", description="This command can only be used in <#1217930874142588938>.", color=discord.Color.orange())
        response = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await response.delete()
        return

    path = path.strip()
    pivotto_str = f"game.Players.LocalPlayer.Character:PivotTo({path}.CFrame)"

    embed = discord.Embed(title="PivotTo", description=f"```lua\n{pivotto_str}\n```\nNote: When the path has numbers, it will give you a warning. You need to close it using square brackets and a string [\"Number\"] or ping Gray.", color=discord.Color.gold())
    await ctx.send(embed=embed)
# Bot token 
client.run('No Token')
