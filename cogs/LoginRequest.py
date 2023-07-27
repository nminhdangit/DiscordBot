import discord
from discord import app_commands
from discord.ext import commands
import string
import data
import secrets

password = '000000'

class LoginRequest(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		
	@commands.Cog.listener()
	async def on_ready(self):
		view = LoginButton()
		embed = discord.Embed(title="Verification Required!",description="**To access `PinkTeddy`, you need to pass the verification first.**\nPress on the **`Verify`** button below. Press **`Help`** to get more information.",colour=discord.Colour.dark_theme())
		channel = self.bot.get_channel(data.login_channel)
		await channel.send(embed=embed,view=view)

	@commands.Cog.listener()
	async def on_member_join(self,member):
		unverifiedRole = discord.utils.get(member.guild.roles, name='Unverified')
		await member.add_roles(unverifiedRole)

	@app_commands.command(name="getcode", description = "Create a login code for your friend.")
	@app_commands.checks.has_role('Admin')
	async def getcode(self,interaction: discord.Interaction):
		global password
		await interaction.response.send_message(f"Code: {password}",ephemeral=True)

	@getcode.error
	async def getcode_error(self,interaction: discord.Interaction,error):
		if isinstance(error,app_commands.MissingRole):
			await interaction.response.send_message(f"You don't have permission to do this command!",ephemeral=True)
	

class LoginButton(discord.ui.View):
	def __init__(self):
		super().__init__(timeout=None)
		self.value = None
		self.cooldown = commands.CooldownMapping.from_cooldown(1, 60*3, commands.BucketType.member)

	@discord.ui.button(label="Verify", style=discord.ButtonStyle.green)
	async def Verify(self,interaction: discord.Interaction, button: discord.ui.Button):
		interaction.message.author = interaction.user
		bucket = self.cooldown.get_bucket(interaction.message)
		retry = bucket.update_rate_limit()
		if retry:
			return await interaction.response.send_message(f"Retry after {int(retry)} seconds.", ephemeral = True)
		await interaction.response.send_modal(LoginModal())

	@discord.ui.button(label="Help",style=discord.ButtonStyle.gray)
	async def Help(self,interaction: discord.Interaction, button: discord.ui.Button):
		embed = discord.Embed(title="Hướng dẫn lấy code Verify",description=f"Hãy liên hệ với người đã giới thiệu bạn vào nhóm, yêu cầu họ dùng lệnh **`/getcode`** để lấy code, sau đó bạn sử dụng code đó để Verify.\n Mọi thắc mắc xin liên hệ <@586169972384858123>",colour=discord.Colour.dark_theme())
		await interaction.response.send_message(embed=embed,ephemeral=True,delete_after=120)


class LoginModal(discord.ui.Modal, title ="Verify"):
	inputCode = discord.ui.TextInput(label="Code",style=discord.TextStyle.short,placeholder="1a2b3c",required=True,max_length=6)
	async def on_submit(self, interaction: discord.Interaction):
		global password
		if(str(self.inputCode) == password):
			self.hashing()
			memberRole = discord.utils.get(interaction.user.guild.roles,name="Member")
			unverifiedRole = discord.utils.get(interaction.user.guild.roles,name="Unverified")
			await interaction.user.add_roles(memberRole)
			await interaction.user.remove_roles(unverifiedRole)
			await interaction.response.defer(ephemeral=True)
		else:
			await interaction.response.send_message(f'Wrong code!!! Wait for 3 minutes to re-try.', ephemeral=True)

	def hashing(self):
		global password
		alphabet = string.ascii_letters + string.digits
		password = ''.join(secrets.choice(alphabet) for i in range(6))

async def setup(bot:commands.Bot):
	await bot.add_cog(LoginRequest(bot))