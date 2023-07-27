import discord	
from discord import app_commands
from discord.ext import commands
from discord.components import *
import asyncio
import re
# import io
# import requests
# import pytesseract
# from PIL import Image
import datetime
import pytz
import data

class ChannelType(commands.Cog):
	def __init__(self,bot):
		self.bot = bot


	@commands.command(name="ping",pass_context=True)
	@commands.has_role("Admin")
	async def ping(self,ctx):
		channel = botChannel(self.bot,ctx)
		await channel.run()

class botChannel:
	def __init__(self,bot,ctx):
		self._bot = bot
		self._ctx = ctx
		self._finish = False

	async def inputName(self,msg,error):
		await self._channel.send(msg)
		def check(m):
			return m.author.id == 586169972384858123
		while True:
			message = await self._bot.wait_for("message",check=check)
			if len(message.content) < 15:
				return message.content
			await self._channel.send(error)
	
	async def inputInt(self,msg,error):
		await self._channel.send(msg)
		def check(m):
			return m.author.id == 586169972384858123
		while True:
			try:
				message = await self._bot.wait_for("message",check=check)
				return int(message.content)
			except ValueError:
				await self._channel.send(error)

	async def inputFloat(self,msg,error):
		await self._channel.send(msg)
		def check(m):
			return m.author.id == 586169972384858123
		while True:
			try:
				message = await self._bot.wait_for("message",check=check)
				return float(message.content)
			except ValueError:
				await self._channel.send(error)

	async def inputValidator(self,pattern,msg,error):
		await self._channel.send(msg)
		def check(m):
			return m.author.id == 586169972384858123
		while True:
			message = await self._bot.wait_for("message",check=check)
			if re.match(pattern=pattern,string=message.content,flags=re.IGNORECASE):
				return str(message.content).lower()
			await self._channel.send(error)

	async def run(self):
		category = discord.utils.get(self._ctx.guild.categories, name="🔰┃Internal")

		self._channel = await category.create_text_channel(name="Settings",overwrites={self._ctx.author: discord.PermissionOverwrite(view_channel=True,read_message_history=True,send_messages=True,read_messages=True)})
		timeout_task = asyncio.create_task(self.timeout())
		getSettings_task = asyncio.create_task(self.getSettings())
		await asyncio.gather(
        timeout_task,
		getSettings_task
    	)

	async def timeout(self):
		await asyncio.sleep(60*2)
		if not self._finish:
			await self._channel.delete()

	async def getSettings(self):
		name = await self.inputName("Input the name of channel: ","Faild!!Re-input the name: ")
		user_id = await self.inputInt("Input the user ID: ","Faild!!Re-input the user ID: ")
		bot_id = await self.inputInt("Input the bot ID: ","Faild!!Re-input the bot ID: ")
		time = await self.inputFloat("Input the usage time: ","Faild!!Re-input the usage time: ")
		type = await self.inputValidator(r"default","Input the type(Default/Medium/Premium): ","Faild!!Re-input the type(Default/Medium/Premium): ")
		channel = default(self._bot,self._ctx,name,user_id,bot_id,time)
		await channel.new()
		asyncio.create_task(channel.run())
		self._finish = True
		await self._channel.delete()
		
class Channel:
	def __init__(self,bot,ctx,name,user_id,bot_id,time):
		self._bot = bot
		self._ctx = ctx
		self._channel = None
		self._time = time
		self._user = user_id
		self._bot_user = bot_id
		self._name = name

	async def new(self):
		category = discord.utils.get(self._ctx.guild.categories, name="⚔ ┃ Tool")
		self._user = self._bot.get_user(self._user)
		self._bot_user = self._bot.get_user(self._bot_user)
		self._channel = await category.create_text_channel(name=self._name)
		await self._channel.edit(sync_permissions=True)
		await self._channel.set_permissions(self._user,view_channel=True,read_message_history=True,send_messages=True,embed_links=True,attach_files=True,send_messages_in_threads=True,use_application_commands=True)
		await self._channel.set_permissions(self._bot_user,view_channel=True,attach_files=True,read_message_history=True,send_messages=True)
		await self._channel.create_thread(name="Writing",type=discord.ChannelType.public_thread)

	async def notification(self):
		channel_view = self._bot.get_channel(data.channel_view)
		self.timeOpen = datetime.datetime.now(pytz.timezone('Asia/Ho_Chi_Minh'))
		self.timeDelete = self.timeOpen + datetime.timedelta(hours=self._time)
		embed = discord.Embed(title=f":satellite: Channel Info",description=f"{self._channel.mention}",colour=discord.Colour.green())
		embed.set_author(name=f"{self._channel}",icon_url="https://cdn.discordapp.com/icons/1031519954811494462/bdff3995b5f588e544750b06dc05a49b.webp?size=100")
		embed.add_field(name=":id:",value=f"{self._channel.id}")
		embed.add_field(name=":page_facing_up: Status",value=f":white_check_mark: Open",inline=True)
		embed.add_field(name=":bust_in_silhouette: Author",value=f"{self._user.mention}",inline=True)
		embed.add_field(name=":hourglass: Open at",value=f"{self.timeOpen}",inline=True)
		embed.add_field(name=":hourglass: Detele at",value=f"{self.timeDelete}",inline=True)
		self.notice = await channel_view.send(embed = embed)

	async def notification_finish(self):
		embed2 = discord.Embed(title=f":satellite: Channel Info",description=f"{self._channel.mention}",colour=discord.Colour.red())
		embed2.set_author(name=f"{self._channel}",icon_url="https://cdn.discordapp.com/icons/1031519954811494462/bdff3995b5f588e544750b06dc05a49b.webp?size=100")
		embed2.add_field(name=":id:",value=f"{self._channel.id}")
		embed2.add_field(name=":page_facing_up: Status",value=f":x: Deleted")
		embed2.add_field(name=":bust_in_silhouette: Author",value=f"{self._user.mention}",inline=True)
		embed2.add_field(name=":hourglass: Open at",value=f"{self.timeOpen}",inline=True)
		embed2.add_field(name=":hourglass: Detele at",value=f"{self.timeDelete}",inline=True)
		await self.notice.edit(embed=embed2)


	async def run(self):
		await self.notification()
		await self.timeout()
		

	async def timeout(self):
		await asyncio.sleep(self._time*60*60)
		await self.notification_finish()
		await self._channel.delete()
		self._channel = None

class default(Channel):
	def __init__(self,bot,ctx,name,user_id,bot_id,time):
		super().__init__(bot,ctx,name,user_id,bot_id,time)

# class medium(Channel):
# 	def __init__(self,bot,ctx,name,user_id,bot_id,time):
# 		super().__init__(bot,ctx,name,user_id,bot_id,time)

# 	async def run(self):
# 		await asyncio.gather(
#         self.timeout(),
# 		self.autoMessage()
#     	)

# 	async def autoMessage(self):
# 		checkImg = None
# 		def check(m):
# 			return m.channel == self._channel
# 		while self._channel is not None:
# 			try:
# 				message = await self._bot.wait_for("message",check=check)
# 			except:
# 				continue
# 			if(message.attachments):
# 				if(message.attachments[0].filename != checkImg and message.attachments[0].content_type == 'image/png'):
# 					checkImg = message.attachments[0].filename
# 				else:
# 					await message.delete()
# 			else:
# 				continue
		
# class premium(Channel):
# 	def __init__(self,bot,ctx,name,user_id,bot_id,time):
# 		self._data = [None] * 50
# 		self._path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# 		self._thread = None
# 		self._question25 = None
# 		self._question50 = None
# 		super().__init__(bot,ctx,name,user_id,bot_id,time)

# 	async def run(self):
# 		self._thread = await self._channel.create_thread(name="UI")
# 		question = Question()
# 		question.set_data(self._data)
# 		await question.filter()
# 		self._question25 = await self._thread.send(view=question.get_question25())
# 		self._question50 = await self._thread.send(view=question.get_question50())
# 		await asyncio.gather(
#         self.timeout(),
# 		self.autoMessage()
#     	)

# 	async def autoMessage(self):
# 		checkImg = None
# 		def check(m):
# 			return m.channel == self._channel
# 		while self._channel is not None:
# 			try:
# 				message = await self._bot.wait_for("message",check=check)
# 			except:
# 				continue
# 			if(message.attachments):
# 				if(message.attachments[0].filename != checkImg and message.attachments[0].content_type == 'image/png'):
# 					checkImg = message.attachments[0].filename
# 					await self.img2text(message)
# 				else:
# 					await message.delete()
# 			else:
# 				continue

# 	async def update_question(self):
# 		question = Question()
# 		question.set_data(self._data)
# 		await question.filter()
# 		await self._question25.edit(view=question.get_question25())
# 		await self._question50.edit(view=question.get_question50())

# 	async def img2text(self,message):
# 		response = requests.get(url=message.attachments[0].proxy_url)
# 		img = Image.open(io.BytesIO(response.content))
# 		left = 90
# 		top = 27
# 		right = 1927
# 		bottom = 810
# 		img = img.crop((left, top, right, bottom))
# 		pytesseract.pytesseract.tesseract_cmd = self._path_to_tesseract
# 		text = pytesseract.image_to_string(img,lang="eng",config='--oem 3 --psm 6')
# 		await self.checkText(f"{text}\n{message.attachments[0].proxy_url}")

# 	async def checkText(self,message):
# 		check = re.search('Multiple choices (\d+)/',message)
# 		if(check == None):
# 			return
# 		else:
# 			self._data[int(check.group(1))-1] = f"{message}"
# 			await self.update_question()


# class Question:
# 	def __init__(self):
# 		self._question25 = Question25()
# 		self._question50 = Question50()
# 		self._data = [None] * 50

# 	def set_data(self,data):
# 		self._data = data

# 	async def filter(self):
# 		data25,data50 = self._data[:25],self._data[25:]
# 		self._question25.set_data(data25)
# 		self._question50.set_data(data50)
# 		await self._question25.create_button()
# 		await self._question50.create_button()

# 	def get_question25(self):
# 		return self._question25

# 	def get_question50(self):
# 		return self._question50



# class Question25(discord.ui.View):
# 	def __init__(self):
# 		super().__init__()
# 		self._data = [None] * 25

# 	def set_data(self,data):
# 		self._data = data

# 	async def create_button(self):
# 		for i in range(25):
# 			if(self._data[i] != None):
# 				button = Button(f"{i+1}",discord.ButtonStyle.green)
# 			else:
# 				button = Button(f"{i+1}",discord.ButtonStyle.grey)
# 			button.data = self._data[i]
# 			self.add_item(button)

# class Question50(discord.ui.View):
# 	def __init__(self):
# 		super().__init__()
# 		self._data = [None] * 25

# 	def set_data(self,data):
# 		self._data = data

# 	async def create_button(self):
# 		for i in range(25):
# 			if(self._data[i] != None):
# 				button = Button(f"{i+26}",discord.ButtonStyle.green)
# 			else:
# 				button = Button(f"{i+26}",discord.ButtonStyle.grey)
# 			button.data = self._data[i]
# 			self.add_item(button)


# class Button(discord.ui.Button):
# 	def __init__(self,label,style):
# 		super().__init__(label=label,style=style)

# 	async def callback(self, interaction: discord.Interaction):
# 		await interaction.response.edit_message(content=self.data)


async def setup(bot:commands.Bot):
	await bot.add_cog(ChannelType(bot))