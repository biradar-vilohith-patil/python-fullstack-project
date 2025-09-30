import os
from datetime import datetime
from supabase import create_client, Client # pip install supabase
from dotenv import load_dotenv # pip install python-dotenv
 
load_dotenv()
 
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    # Use a clear ValueError to stop execution if credentials aren't found
    raise ValueError("SUPABASE_URL or SUPABASE_KEY not found in environment variables. Check your .env file.")

sb: Client = create_client(url, key)

def create_player(name):
    try:
        player = sb.table("players").insert({"name": name}).execute()
        if player.data:
            return player.data[0]
        return None 
    except Exception as e:
        print( f"Player is not created due to {e}")
        return None

def update_stats(player_id , stats : dict ):
    try:
        player = sb.table("players").update(stats).eq("id",player_id).execute()
        if player.data:
            return player.data[0]
        return None 
    except Exception as e:
        print(f"failed due to {e}")
        return None

def get_player (player_id : int):
    try:
        player = sb.table("players").select("*").eq("id",player_id).single().execute()
        return player.data
    except Exception as e:
        if "No rows found" in str(e) or "404" in str(e): # Handle 404 for clarity
            return None
        print(f"Failed to retrieve player {player_id} due to {e}")
        return None 

def get_all_choices():
    try:
        choice = sb.table("choices").select("*").execute()
        return choice.data
    except Exception as e:
        print(f"failed to retrive due to {e}")
        return []

def get_choice_by_name(name):
    try :
        ch = sb.table("choices").select("*").eq("name" , name).single().execute()
        return ch.data
    except Exception as e:
        if "No rows found" in str(e) or "404" in str(e): # Handle 404 for clarity
            return None
        print(f"Failed to retrieve choice {name} due to {e}")
        return None 


def save_achievement(player_id: int, title: str, description: str, xp_reward: int, time_reward: int):
    try:
        achievement_data = {
            "player_id": player_id,
            "title": title,
            "description": description,
            "xp_reward": xp_reward,
            "time_reward": time_reward,
            # 'unlocked_at' uses the DB default (CURRENT_TIMESTAMP)
        }
        
        resp = sb.table("achievements").insert(achievement_data).execute()
        
        if resp.data:
            return resp.data[0] # Return the created achievement record
        return None
        
    except Exception as e:
        print(f"Error saving achievement for player {player_id}: {e}")
        return None
    

    