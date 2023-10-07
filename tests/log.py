import discord
from discord.ext import commands

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    # Check if the message is in the #general channel and not sent by the bot itself
    if message.channel.name == 'general' and message.author != bot.user:
        # Get the logs channel by name (replace 'logs' with your actual channel name)
        logs_channel = discord.utils.get(message.guild.text_channels, name='logs')
        
        if logs_channel:
            # Create an embed with a blue color
            embed = discord.Embed(color=discord.Color.blue())
            # Add the formatted message content to the embed
            embed.add_field(
                name=f"**{message.author.name}** (@{message.author.display_name})",
                value=message.content
            )
            
            # Send the embed to the logs channel
            await logs_channel.send(embed=embed)

            # Log the message content to the file
            with open('logged.txt', 'a') as file:
                file.write(f"{message.author.name} (@{message.author.display_name}): {message.content}\n")
        else:
            print('Logs channel not found!')

# Run the bot with your token
bot.run('MTE2MDMwMDIyMjY3Nzc4Njc1NQ.GtzSoU.864QwXYJKIUMBUqYbX7IvWRYHE58TO2k187EjA')
