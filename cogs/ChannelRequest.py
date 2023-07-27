import discord	
import data
from discord import app_commands
from discord.ext import commands
import asyncio

class ChannelRequest(commands.Cog):
	def __init__(self,bot):
		self.bot = bot

	@app_commands.command(name="invite", description="Invite Supporter")
	async def invite(self, interaction: discord.Interaction, user_id: str):
		member = interaction.guild.get_member(int(user_id))
		if member:
			view = RequestJoinChannelButton(member)
			embed = discord.Embed(title=f"Invite",description=f"Bạn có chắc sẽ cho {member.mention} vào room.\nChọn **`Accept`** hoặc **`Ignore`**.\nAutoDelete after 3mins." ,colour=discord.Color.dark_theme())
			message = await interaction.response.send_message(embed=embed,view=view,delete_after=60)

		else:
			await interaction.response.send_message(id + " is not a member")		

class RequestJoinChannelButton(discord.ui.View):
	def __init__(self,user):
		super().__init__()
		self.user = user

	@discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
	async def Accept(self,interaction: discord.Interaction, button: discord.ui.Button):
		embed1 = discord.Embed(title=":white_check_mark: Accept",description=f"Accepted the request.",colour=discord.Colour.green())
		await interaction.channel.set_permissions(self.user, view_channel=True,read_message_history=True,send_messages=True,read_messages=True,attach_files=True,send_messages_in_threads=True)
		await interaction.response.send_message(embed=embed1,ephemeral=True,delete_after=10)		

	@discord.ui.button(label="Ignore",style=discord.ButtonStyle.red)
	async def Help(self,interaction: discord.Interaction, button: discord.ui.Button):
		embed = discord.Embed(title=":x: Ignore",description=f"Ignored the request.",colour=discord.Colour.red())
		await interaction.response.send_message(embed=embed,ephemeral=True,delete_after=10)

	
async def setup(bot:commands.Bot):
	await bot.add_cog(ChannelRequest(bot))