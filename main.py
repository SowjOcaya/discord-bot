import discord,os
from discord.ext import commands

#Global vars
token = os.getenv("bot_token")
bot_name = "My First Bot"
cmd_prefix = "|"
mod_role = "Mod Role Name"

client = commands.Bot(command_prefix = cmd_prefix)
client.remove_command('help')

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game(name=f"{cmd_prefix}help"))
  print("Bot Online")

@client.command()
async def ping(ctx):
  await ctx.send(f'Pong! {round(client.latency * 1000)}ms')

@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = 'Help',
    description = "Try out these commmands below",
    colour = discord.Colour.orange()
  )

  embed.set_footer(text = "Made By @Fishball_Noodles. Bot Realeased Since June 01,2020")
  embed.set_author(name = bot_name)
  embed.add_field(name = f"{cmd_prefix}ping", value = "Check Ping",inline = False)
  embed.add_field(name = f"{cmd_prefix}clear <Number of Messages to clear>", value = "Clear Messages (Default 10)",inline= False)
  embed.add_field(name = f"{cmd_prefix}suggest <Suggestion>", value = "Suggest a New Function for Any Bot With The Role Original or just a server function",inline = False)
  await ctx.send(embed=embed)

@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def suggest(ctx,*,suggestion):
  author=ctx.message.author
  embed = discord.Embed(
    title = 'Suggestion',
    description = "This Was Suggested By",
    colour = discord.Colour.orange()
  )

  embed.set_footer(text = "Made By @Fishball_Noodles with .py")
  embed.set_author(name = bot_name)
  embed.add_field(name = author, value = suggestion,inline = False)
  channel = client.get_channel(suggestion_channel)
  await ctx.send("Suggestion Submitted")
  msg = await channel.send(embed=embed)
  await msg.add_reaction('👍')
  await msg.add_reaction('👎')

@suggest.error
async def suggest_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		em = discord.Embed(title=f"**Slow it down bro!**",description=f"Try again in {error.retry_after:.2f} seconds.", color=didsocrd.Colour.red())
		await ctx.send(embed=em)

@client.command()
@commands.has_role(mod_role)
async def clear(ctx,amount=10):
	await ctx.message.delete()
	await ctx.channel.clear(limit=amount)

#Manually Give Command
@client.command()
@commands.has_role(mod_role)
async def give_role(ctx,member:discord.Member,role:discord.Role,*,reason=None):
  member.add_roles(role,reason=reason)

#AutoRole
@client.command()
async def gamer_role(ctx):
	role_id_togive = 3456787654323456
	member = ctx.message.author
	role = ctx.guild.get_role(role_id_togive)
	await member.add_roles(role)
	await ctx.send("{} Have Been Given The Role `{}`".format(member.mention,role.name))

client.run(token)