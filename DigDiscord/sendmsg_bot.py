# ex from :
# https://github.com/Rapptz/discord.py/blob/v1.7.3/examples/background_task.py

import discord
import os
import sys

my_token = os.environ.get('BOT_TOKEN')
my_channel = os.environ.get('BOT_CHANNEL')
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_stat_link(self, link):
        self.link = link

    async def on_ready(self):
        print('Logged in as')
        print('username: {}'.format(self.user.name))
        print('user id : {}'.format(self.user.id))
        print('channel : {}'.format(my_channel))
        # await self.wait_until_ready()
        channel = self.get_channel(int(my_channel)) # channel ID goes here
                await channel.send(f"Top contributeurs de la semaine !\n {self.link}")
        await self.close()


client = MyClient()
client.set_stat_link(sys.argv[1])
client.run(my_token)
exit()
