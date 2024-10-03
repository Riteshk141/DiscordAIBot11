import asyncio
from discord import Message, utils

class SpamProtection:
    def __init__(self, client, warning_threshold=7, mute_duration=10000):
        self.client = client
        self.warning_threshold = warning_threshold
        self.mute_duration = mute_duration
        self.user_messages = {}
        self.warning_sent = {}

    async def check_spam(self, message: Message):
        user_id = message.author.id
        now = asyncio.get_event_loop().time()

        if user_id not in self.user_messages:
            self.user_messages[user_id] = []

        # Add the current message time to the user's message list
        self.user_messages[user_id].append(now)

        # Keep only messages within the last 5 seconds
        self.user_messages[user_id] = [msg_time for msg_time in self.user_messages[user_id] if now - msg_time <= 25]  # list comprehension


        # Check if the user has sent more than the threshold number of messages
        if len(self.user_messages[user_id]) > self.warning_threshold:
            if user_id not in self.warning_sent:
                await message.channel.send(f"{message.author.mention} Woah, slow down there! You are sending too many messages!")
                self.warning_sent[user_id] = True
            else:
                await self.mute_user(message)

    async def mute_user(self, message: Message):
        user = message.author
        role = utils.get(message.guild.roles, name="Mute Members")

        if role is None:
            await message.channel.send("Mute Members role not found. Please create a role named 'Mute Members'.")
            return

        await user.add_roles(role)
        await message.channel.send(f"{user.mention} has been muted for spamming.")

        await asyncio.sleep(self.mute_duration)

        await user.remove_roles(role)
        await message.channel.send(f"{user.mention} has been unmuted.")

        # Clear the user's messages and warnings after muting
        self.user_messages.pop(user.id, None)
        self.warning_sent.pop(user.id, None)
