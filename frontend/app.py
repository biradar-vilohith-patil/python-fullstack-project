# frontend/app.py

import streamlit as st
import requests
import time
from typing import Optional, Dict

# --- Configuration ---
API_BASE_URL = "https://timescape-backend.onrender.com/"

# Set a dark, modern theme for a Shadcn-like aesthetic
st.set_page_config(
    page_title="TimeScape",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for a cleaner, modern look (simulating cards, dark theme)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d1117; /* Dark background */
        color: #c9d1d9; /* Light text */
    }
    .main-header {
        color: #58a6ff; /* Primary blue color */
        text-align: center;
        margin-bottom: 20px;
    }
    .stat-card {
        background-color: #161b22; /* Darker card background */
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 10px;
        border-left: 4px solid #58a6ff; /* Accent border */
    }
    .stat-value {
        font-size: 24px;
        font-weight: bold;
        color: #ffffff;
    }
    .game-message {
        background-color: #21262d;
        padding: 15px;
        border-radius: 8px;
        margin-top: 20px;
        border-left: 5px solid #f0b343; /* Warning/Info color */
    }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        border: 1px solid #30363d;
        background-color: #21262d;
        color: #c9d1d9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- API UTILITIES ---

@st.cache_data
def fetch_choices():
    """Fetches static choices from the API (cached)."""
    try:
        response = requests.get(f"{API_BASE_URL}/choices")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to fetch choices. Is the backend running? Error: {e}")
        return []

def fetch_player_data(player_id: int):
    """Fetches a player's current state."""
    try:
        response = requests.get(f"{API_BASE_URL}/players/{player_id}")
        response.raise_for_status()
        return response.json()
    except Exception:
        return None

def create_new_player(name: str):
    """Creates a new player via API."""
    try:
        response = requests.post(f"{API_BASE_URL}/players/create?name={name}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Failed to create player: {e}")
        return None

def perform_action(player_id: int, choice_name: str):
    """Sends the chosen action to the API and returns the game response."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/game/{player_id}/action",
            json={"choice_name": choice_name}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        st.error(f"Game Error: {e.response.json().get('detail', 'An unknown error occurred.')}")
        return None
    except Exception as e:
        st.error(f"Network Error: {e}")
        return None


# --- UI COMPONENTS ---

def display_stats(stats: Dict):
    """Displays player stats in a responsive grid of cards."""
    st.subheader("Current State")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Define stat displays
    stat_info = [
        ("TIME ⏳", stats.get('time'), "#f0b343"),
        ("XP 🧠", stats.get('xp'), "#58a6ff"),
        ("FUN 🎉", stats.get('fun'), "#a371f7"),
        ("HEALTH ❤️", stats.get('health'), "#f85149"),
        ("STRESS 💢", stats.get('stress'), "#e6005c"),
    ]

    for i, (label, value, color) in enumerate(stat_info):
        col = [col1, col2, col3, col4, col5][i]
        with col:
            st.markdown(
                f"""
                <div class='stat-card' style='border-left-color: {color};'>
                    <small>{label}</small><br>
                    <span class='stat-value'>{value}</span>
                </div>
                """,
                unsafe_allow_html=True
            )

def display_game_over(ending_title: str):
    """Displays the Game Over screen."""
    st.markdown("---")
    st.markdown(
        f"<h1 style='color: #f85149; text-align: center;'>GAME OVER</h1>", 
        unsafe_allow_html=True
    )
    st.markdown(
        f"<h2 style='text-align: center;'>Your Destiny: {ending_title}</h2>", 
        unsafe_allow_html=True
    )
    if st.button("Start New Game", key="restart_btn"):
        st.session_state.player_id = None
        st.rerun()

def display_main_game(player_id: int):
    """The main game loop where the player chooses actions."""
    
    # 1. Fetch data
    current_player_data = fetch_player_data(player_id)
    if not current_player_data:
        st.error("Error: Could not retrieve player state.")
        st.session_state.player_id = None # Go back to start screen
        st.rerun()
    
    choices = fetch_choices()
    
    # 2. Display Stats
    display_stats(current_player_data)
    
    # 3. Check for Game Over (Client-side check, though API handles the source of truth)
    if current_player_data.get('time', 0) <= 0 or current_player_data.get('stress', 0) > 100:
        # Fallback in case the API's first check missed the game over state
        st.session_state.game_over_title = "Undetermined Fate"
        display_game_over(st.session_state.game_over_title)
        return

    st.markdown("---")
    st.subheader("Choose Your Action")
    
    # 4. Display Action Buttons (responsive grid)
    cols = st.columns(3)
    
    for i, choice in enumerate(choices):
        col = cols[i % 3]
        with col:
            if col.button(choice['name'], key=f"choice_{choice['id']}"):
                
                # --- API Integration: Action Request ---
                with st.spinner(f"Performing action: {choice['name']}..."):
                    response = perform_action(player_id, choice['name'])

                if response:
                    # Save the new game state flags
                    st.session_state.game_over = response['game_over']
                    st.session_state.game_over_title = response['ending_title']
                    st.session_state.last_message = f"**Action Taken:** {choice['name']}"
                    
                    if response['achievement_unlocked']:
                        ach_titles = ", ".join([a['title'] for a in response['achievement_unlocked']])
                        st.session_state.last_message += f"<br>**✨ Achievement Unlocked:** {ach_titles}"

                    # Rerun to update stats and UI
                    st.rerun()
                else:
                    # The perform_action utility already displayed the error
                    pass 
    
    # 5. Display Last Message/Feedback
    if st.session_state.get('last_message'):
        st.markdown(
            f"<div class='game-message'>{st.session_state.last_message}</div>", 
            unsafe_allow_html=True
        )

# --- MAIN APP FLOW ---

def main():
    st.markdown(
        "<h1 class='main-header'>🎮 Time Scape</h1><p style='text-align:center;'>Time is your only currency.</p>",
        unsafe_allow_html=True
    )

    # Initialize session state variables
    if 'player_id' not in st.session_state:
        st.session_state.player_id = None
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False

    # --- Start Screen (No Player ID) ---
    if st.session_state.player_id is None:
        player_name = st.text_input("Enter your name to start the adventure:")
        if st.button("Begin Life", key="start_game_btn"):
            if player_name:
                # --- API Integration: Create Player ---
                new_player_data = create_new_player(player_name)
                if new_player_data and new_player_data.get('id'):
                    st.session_state.player_id = new_player_data['id']
                    st.success(f"Welcome, {new_player_data['name']}! Your journey begins.")
                    st.rerun()
            else:
                st.warning("Please enter a name.")

    # --- Game Over Screen ---
    elif st.session_state.game_over:
        display_game_over(st.session_state.get('game_over_title', "Game Over"))

    # --- Main Game Loop ---
    else:
        display_main_game(st.session_state.player_id)


if __name__ == "__main__":
    main()
