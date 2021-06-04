BASE_END_POINT = "https://discord.com/api/channels/{}/messages"
# note : Use your personal token is against discord terms of services
# You should try to get your own token by grabbing some tutorials about this subject
# and export it in environement variable named 'DISCORD_USER_TOKEN'
GUILD_ID = "ID_FROM_CONSTANT"
DISCORD_USER_TOKEN = "TOKEN_FROM_CONSTANT"
BASE_END_POINT = "https://discord.com/api"
MESSAGES_CHANNEL_END_POINT = "{}/channels/{{}}/messages".format(BASE_END_POINT)
GUILD_END_POINT = "{}/guilds/{{}}/preview".format(BASE_END_POINT)
CHANNELS_GUILD_END_POINT = "{}/guilds/{{}}/channels".format(BASE_END_POINT)
