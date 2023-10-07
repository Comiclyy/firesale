import discord
from discord.ext import commands
import requests
import pytz
from datetime import datetime

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# Function to format an item ID
def format_item_id(item_id):
    # Replace underscores with spaces and capitalize the first letter of each word
    words = item_id.split('_')
    formatted_item_id = ' '.join([word.capitalize() for word in words])
    return formatted_item_id

@bot.command(name="fire")
async def fire_command(ctx):
    # Send a GET request to the Hypixel API
    api_url = "https://api.hypixel.net/skyblock/firesales"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            # Check if there are any sales
            if 'sales' in data and data['sales']:
                # Extract the first sale's details
                sale = data['sales'][0]
                item_id = sale['item_id']
                formatted_item_id = format_item_id(item_id)
                
                # Convert Unix timestamps to the user's local timezone
                user_timezone = pytz.timezone('EST')  # Replace 'Your_Timezone_Here' with the user's timezone
                start_time_utc = datetime.utcfromtimestamp(sale['start'] / 1000)
                start_time_local = start_time_utc.astimezone(user_timezone)
                end_time_utc = datetime.utcfromtimestamp(sale['end'] / 1000)
                end_time_local = end_time_utc.astimezone(user_timezone)

                # Format and send detailed sale information as the bot's response
                response_message = (
                    f"Sale: {formatted_item_id}\n"
                    f"Start Time: {start_time_local.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
                    f"End Time: {end_time_local.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
                    f"Amount: {sale['amount']}\n"
                    f"Price: {sale['price']}"
                )
                await ctx.send(response_message)
            else:
                await ctx.send("No sales data available.")
        else:
            await ctx.send("API request was not successful.")
    else:
        await ctx.send(f"Failed to fetch data. Status code: {response.status_code}")

# Replace 'MTE2MDI3MDM2NDgyNDMxMzg2Ng.GNaE40.2Nvh4HrlIU2RuK9CePYqDHfYvJJMw6jwjZBbMk' with your actual Discord bot token
bot.run('MTE2MDI3MDM2NDgyNDMxMzg2Ng.GNaE40.2Nvh4HrlIU2RuK9CePYqDHfYvJJMw6jwjZBbMk')
