import requests
import json

# Function to print a warning message in bright bold red without a background color
def print_warning(message):
    print("\033[1;31m" + message + "\033[m")

# Ask the user for a Minecraft username
username = input("Enter the Minecraft username to check: ")

# Make a request to Mojang's API to get the player's UUID
mojang_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
mojang_response = requests.get(mojang_url)

# Check if the request to Mojang's API was successful (status code 200)
if mojang_response.status_code == 200:
    mojang_data = mojang_response.json()
    
    # Extract the UUID from the Mojang response
    uuid = mojang_data.get("id")
    
    # Define the API URL and parameters for the Hypixel status request
    status_url = "https://api.hypixel.net/status"
    status_params = {
        "uuid": uuid
    }
    
    # Define the common headers
    headers = {
        "api-key": "7ad4d70a-fa2e-4fc3-a818-71d770f2ffff"
    }
    
    # Make the GET request to status endpoint
    response_status = requests.get(status_url, params=status_params, headers=headers)
    
    # Check if the status request was successful (status code 200)
    if response_status.status_code == 200:
        status_data = response_status.json()
        
        # Check if the user is offline
        if not status_data["session"]["online"]:
            print_warning("WARNING: USER IS OFFLINE")
        else:
            print("User is online.")
        
        # Define the API URL and parameters for the Hypixel /player request
        player_url = "https://api.hypixel.net/player"
        player_params = {
            "uuid": uuid
        }
        
        # Make the GET request to player endpoint
        response_player = requests.get(player_url, params=player_params, headers=headers)
        
        # Check if the request to /player was successful (status code 200)
        if response_player.status_code == 200:
            player_data = response_player.json()
            
            # Beautify and save player data to a file
            player_formatted_data = json.dumps(player_data, indent=4)
            player_filename = f"{uuid}-player-output.json"
            with open(player_filename, "w") as player_file:
                player_file.write(player_formatted_data)
            
            print(f"Player data saved to {player_filename}")
        else:
            print("Request to /player failed.")
        
        # Define the API URL and parameters for the Hypixel /recentgames request
        recent_games_url = "https://api.hypixel.net/recentgames"
        recent_games_params = {
            "uuid": uuid
        }
        
        # Make the GET request to recentgames endpoint
        response_recent_games = requests.get(recent_games_url, params=recent_games_params, headers=headers)
        
        # Check if the request to /recentgames was successful (status code 200)
        if response_recent_games.status_code == 200:
            recent_games_data = response_recent_games.json()
            
            # Beautify and save recent games data to a file
            recent_games_formatted_data = json.dumps(recent_games_data, indent=4)
            recent_games_filename = f"{uuid}-recent-games-output.json"
            with open(recent_games_filename, "w") as recent_games_file:
                recent_games_file.write(recent_games_formatted_data)
            
            print(f"Recent games data saved to {recent_games_filename}")
        else:
            print("Request to /recentgames failed.")
    
    else:
        print("Status request to Hypixel API failed.")
else:
    print("Mojang API request failed. Check the provided username.")
