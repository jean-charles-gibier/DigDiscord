# ex from :
# https://github.com/Rapptz/discord.py/blob/v1.7.3/examples/background_task.py

import discord

my_token = 'NzE5MTMxNDM4ODg4MjU1NTMx.Xty9Vw.hu0m-1l8Qw-GD4DkAZxsbhlWFBE'

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        channel = self.get_channel(778208282573275139) # channel ID goes here
        await channel.send("What a wonderful world !")
        await self.close()


client = MyClient()
client.run(my_token)
exit()