import discord
from discord.ext import commands

# Define your bot's token
TOKEN = 'MTE2MDMwNzc4OTMwNzA2ODU3Ng.GDGkeZ.nySbozz5dodX5S7RLGg65aWkusXXQ9oQAV7beo'

# Define the intents your bot needs
intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with intents
bot = commands.Bot(command_prefix='/', intents=intents)

# Define the color for the embed (light red)
embed_color = discord.Color.from_rgb(255, 102, 102)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Event handler for message events
@bot.event
async def on_message(message):
    # Check if the message was sent by the bot itself
    if message.author == bot.user:
        return  # Ignore messages sent by the bot
    
    # Check if the message contains "discord.gift"
    if "discord.gift" in message.content:
        # Find the "nitro" channel
        nitro_channel = discord.utils.get(message.guild.text_channels, name='nitro')
        
        if nitro_channel:
            # Create an embed message
            embed = discord.Embed(
                title="ALERT",
                color=embed_color
            )
            embed.add_field(name=f"**{message.author.display_name}** Sent a gift link!", value=message.content)
            
            # Send the embed message in the #nitro channel
            await nitro_channel.send(embed=embed)
            
            # Find the "nitro" role
            nitro_role = discord.utils.get(message.guild.roles, name='nitro')
            
            if nitro_role:
                # Ping the @nitro role in the #nitro channel
                await nitro_channel.send(f"{nitro_role.mention}")
    
    # Allow other event handlers to process the message
    await bot.process_commands(message)

# Run the bot
bot.run(TOKEN)
