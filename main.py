from discord import app_commands
from discord.ext import commands
import discord
from colorama import Back, Fore, Style
import data

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="!",intents=discord.Intents.all())
		self.filecogs = ["cogs.LoginRequest","cogs.ChannelRequest","cogs.Admin","cogs.ChannelType"]

	async def setup_hook(self):
		for filename in self.filecogs:
			await self.load_extension(filename) 
			print(Fore.WHITE + Style.BRIGHT+ f"Loaded Cog: " + Fore.YELLOW + filename + Fore.RESET + Style.RESET_ALL)


	async def on_ready(self):
		print(Fore.WHITE + Style.BRIGHT+ f"Logged in as " + Fore.YELLOW + self.user.name + Fore.RESET + Style.RESET_ALL)
		print(Fore.WHITE + Style.BRIGHT+ f"Bot ID " + Fore.YELLOW + str(self.user.id) + Fore.RESET + Style.RESET_ALL)
		synced = await self.tree.sync()
	
bot = Bot()

@bot.command()
async def reload(ctx):
	for filename in bot.filecogs:
		bot.reload_extension(filename)
		await ctx.send('Reload!')

bot.run(data.bot_token)