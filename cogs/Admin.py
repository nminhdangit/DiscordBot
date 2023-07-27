import discord	
from discord import app_commands
from discord.ext import commands
import asyncio
import datetime
import pytz

class Admin(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@commands.command(name="check",pass_context=True)
	async def checkQuestion(self,ctx,id: str):
		channel = self.bot.get_channel(int(id))
		thread = channel.get_thread(channel.threads[0].id)
		message = await channel.fetch_message(1056433128937373736)
		await thread.send(message.content)



async def setup(bot:commands.Bot):
	await bot.add_cog(Admin(bot))