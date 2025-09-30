# src/logic.py
from src.models import Player, Choice
from typing import List, Dict

# --- 1. CORE ACTION PROCESSOR ---

def process_action(player: Player, choice: Choice) -> Player:
    """
    Applies the effects of a chosen action and specialized pivot rules 
    (deterministic consequences) to the player's stats.
    """
    
    updated_player = player.model_copy()

    # 1. Apply Base Effects
    updated_player.time += choice.time_cost
    updated_player.xp += choice.xp
    updated_player.fun += choice.fun
    updated_player.health += choice.health
    updated_player.stress += choice.stress
        
    # --- 2. Implement Pivot Logic ---
    choice_name = choice.name.lower()
    
    # Productive Action Logic (Efficiency/Time Refund)
    if 'code' in choice_name or 'study' in choice_name:
        if updated_player.stress < 30:
            updated_player.time += 2  # Small time refund for peak efficiency
        
    # Wasting Time Penalty (Guilt/Binge Mode)
    if 'social media' in choice_name or 'party' in choice_name:
        # Heavy penalty if time is low OR stress is high
        if updated_player.time < 20 or updated_player.stress > 80:
            updated_player.time -= 10
            updated_player.stress += 5
            
    # 3. Implement Stat Boundaries
    updated_player.health = max(0, min(100, updated_player.health))
    updated_player.fun = min(100, updated_player.fun)
    updated_player.xp = max(0, updated_player.xp)

    return updated_player


# --- 2. GAME STATUS CHECK ---

def check_game_status(player: Player) -> bool:
    """Checks if the player has met any Game Over conditions."""
    
    if player.time <= 0:
        return True
    
    if player.stress > 100:
        return True
        
    return False


# --- 3. ENDING DETERMINATION ---

def determine_ending(player: Player) -> str:
    """Assigns a final title based on the player's dominant stats at Game Over."""
    
    if player.stress > 100:
        return "Burnout Zombie 🧟"

    stats_map = {
        'xp': player.xp,
        'fun': player.fun,
        'health': player.health
    }
    
    dominant_stat_key = max(stats_map, key=stats_map.get)
    
    positive_stats = [player.xp, player.fun, player.health]
    
    if (max(positive_stats) - min(positive_stats)) <= 50:
        return "Master of Time ⏳"
        
    if dominant_stat_key == 'xp':
        return "Code Monk 👨‍💻"
    if dominant_stat_key == 'fun':
        return "Party Legend 🍻"
    if dominant_stat_key == 'health':
        return "Zen Master 🧘"
    
    return "Undecided Fate ❓"


# --- 4. ACHIEVEMENT CHECK ---

def check_for_achievements(player: Player) -> List[Dict]:
    """
    Checks if any achievements are unlocked. Returns a list of achievement data.
    """
    unlocked_achievements = []
    
    # Note: In a production app, you would check the DB if the player already has these.
    
    if player.xp >= 50:
        unlocked_achievements.append({
            "title": "Rookie Coder", 
            "description": "Reached 50 XP for the first time.",
            "xp_reward": 10,
            "time_reward": 5
        })
        
    return unlocked_achievements