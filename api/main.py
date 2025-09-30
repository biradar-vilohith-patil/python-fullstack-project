# api/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict

# Import your core logic and database functions
from src import db, logic
from src.models import Player, Choice, GameActionResponse # Import models

# Define a simple Pydantic model for the incoming action request
class ActionRequest(BaseModel):
    choice_name: str

# Initialize the FastAPI application
app = FastAPI(title="TimeScape Game API", version="1.0.0")


@app.get("/")
def read_root():
    return {"message": "Welcome to the TimeScape API! Use /docs to view endpoints."}

# --- 1. Server Status (Health Check) ---
@app.get("/status")
def get_server_status():
    """Simple check to ensure the API is running."""
    return {"status": "ok", "message": "TimeScape API is running!"}

# --- 2. Player Creation ---
@app.post("/players/create", response_model=Player)
def create_player_profile(name: str):
    """Creates a new player profile and returns the starting stats."""
    player_data = db.create_player(name)
    
    if not player_data:
        raise HTTPException(status_code=500, detail="Could not create player in the database.")
    
    return Player(**player_data)

# --- 3. Get All Choices ---
@app.get("/choices", response_model=List[Choice])
def get_all_choices_api():
    """Retrieves all available choices for the game."""
    choices_data = db.get_all_choices()
    
    # Convert list of dictionaries to list of Choice Pydantic models
    return [Choice(**c) for c in choices_data]

# --- 4. Get Player State ---
@app.get("/players/{player_id}", response_model=Player)
def get_player_state(player_id: int):
    """Retrieves the current state and stats of a player."""
    player_data = db.get_player(player_id)
    
    if not player_data:
        raise HTTPException(status_code=404, detail=f"Player with ID {player_id} not found.")
        
    return Player(**player_data)

# --- 5. Core Game Action ---
@app.post("/game/{player_id}/action", response_model=GameActionResponse)
def perform_game_action(player_id: int, action_request: ActionRequest):
    """Handles one turn of the game (choice, calculation, update, status check)."""
    
    # 1. READ: Fetch player and choice data from the DB
    current_player_data = db.get_player(player_id)
    choice_data = db.get_choice_by_name(action_request.choice_name)
    
    if not current_player_data or not choice_data:
        raise HTTPException(status_code=404, detail="Player or Choice not found.")
        
    # Convert dicts to OOP models for logic processing
    current_player = Player(**current_player_data)
    chosen_choice = Choice(**choice_data)
    
    # 2. CALCULATE: Process the action using the logic layer
    new_player_state = logic.process_action(current_player, chosen_choice)
    
    # 3. CHECK ACHIEVEMENTS
    achievements_to_save = logic.check_for_achievements(new_player_state)
    
    # 4. SAVE ACHIEVEMENTS and apply rewards (optional loop)
    # This loop saves to DB and updates the player state with the reward
    for achievement in achievements_to_save:
        db.save_achievement(
            player_id, 
            achievement['title'], 
            achievement['description'], 
            achievement['xp_reward'], 
            achievement['time_reward']
        )
        new_player_state.xp += achievement['xp_reward']
        new_player_state.time += achievement['time_reward']


    # 5. UPDATE: Save the final state to the database (after rewards)
    updated_player_data = db.update_stats(player_id, new_player_state.model_dump())
    
    if not updated_player_data:
        raise HTTPException(status_code=500, detail="Failed to update player stats in DB.")
        
    # 6. CHECK GAME STATUS
    is_game_over = logic.check_game_status(new_player_state)
    ending_title = None
    
    if is_game_over:
        ending_title = logic.determine_ending(new_player_state)
        
    # Return the final response
    return GameActionResponse(
        player=Player(**updated_player_data),
        game_over=is_game_over,
        ending_title=ending_title,
        achievement_unlocked=achievements_to_save
    )