# 🎮 Time Scape – The Clock Adventure

**A fun, educational, and gamified life-simulator game where time is your most precious currency! ⏳**

---

## 🔹 Core Concept

Life is a game of choices, but here the only currency is **Time**. You start with **100 time coins**, and every decision either:

- **Burns your time** 🔥 (wasting hours)
- **Rewards you** ⛏️ (productive actions)

When your balance hits **0**, the game ends with a **funny or insightful title** based on how you spent your time.

---

## 🔹 Features

- **Player Management**: Create and track multiple player profiles.
- **Time-based Currency**: Every action consumes or rewards time coins.
- **Dynamic Choices**: Multiple actions like Study, Party, Code, Sleep, Exercise, Scroll Social Media.
- **Player Stats Tracking**: XP, Fun, Health, Stress.
- **Achievements**: Unlock achievements for reaching milestones.
- **Game Endings**: Different endings based on your stats (e.g., Code Monk, Party Legend, Zen Master, Burnout Zombie, Master of Time).
- **Replayability**: Each playthrough is unique due to random events and choice outcomes.
- **Python OOP Implementation**: Classes, constructors, polymorphism, and data structures.
- **Optional Database Integration**: Store players, choices, events, and achievements in MySQL or Supabase.
- **Interactive Console UI**: Formatted text and suspenseful delays using Python modules like `textwrap` and `time`.

### Project Structure
```
TIMESCAPE/
│
├── src/ # Core application logic
│ ├── logic.py # Business logic and task operations
│ └── db.py # Database operations
│
├── api/ # Backend API
│ └── main.py # FastAPI endpoints
│
├── frontend/ # Frontend application
│ └── app.py # Streamlit web interface
│
├── requirements.txt # Python dependencies
├── README.md # Project documentation
└── .env # Environment variables (API keys, DB credentials, etc.) 
```

### Prerequisites
- python 3.0 or higher
- A supabase Account
- Git & GitHub

#### 1.clone or download the project
git clone <repo url>

#### Install all required python project
pip install -r requirements.txt

#### set up supabase Database
- 1.Create a supabase project
- 2.create the tables:
- go to sql editor in your supabase dash board and run this SQL command


``` sql

CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    time INT NOT NULL DEFAULT 100,
    xp INT NOT NULL DEFAULT 0,
    fun INT NOT NULL DEFAULT 0,
    health INT NOT NULL DEFAULT 50,
    stress INT NOT NULL DEFAULT 0
);

CREATE TABLE choices (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    time_cost INT NOT NULL,
    xp INT NOT NULL DEFAULT 0,
    fun INT NOT NULL DEFAULT 0,
    health INT NOT NULL DEFAULT 0,
    stress INT NOT NULL DEFAULT 0
);


CREATE TABLE achievements (
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    xp_reward INT NOT NULL DEFAULT 0,
    time_reward INT NOT NULL DEFAULT 0,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

3. Get your credentials:


#### 4.Configure environment variables

1. create a `.env` file .
2. add your supabase credentials to `.env` file.


### 5.Run the application

#### StreamLit frontend
streamlit run frontend/app.py

The app will open at http://localhost:8080

#### FastAPI backend
cd api
python main.py

The api will be available at http://localhost:8000

### Key Components 
1. **`src/db,py`**:Database operations - handles all crud operations with supabase
2. **`src/logic.py`** : Business Logic - Task validation and processing.

## 🔹 Gameplay Flow

### **1️⃣ Player Creation**
- Enter your name
- Starting stats:
  - Time = 100 coins
  - XP = 0
  - Fun = 0
  - Health = 50
  - Stress = 0

### **2️⃣ Actions (Choices)**
Each round, choose an action:

| Action | Time Cost | XP | Fun | Health | Stress |
|--------|-----------|----|-----|--------|--------|
| Study 📚 | -10 | +5 | 0 | 0 | 0 |
| Party 🎉 | -20 | 0 | +10 | 0 | +5 |
| Sleep 😴 | -15 | 0 | 0 | +10 | -5 |
| Code 👨‍💻 | -12 | +8 | 0 | 0 | +2 |
| Scroll Social Media 📱 | -8 | 0 | 0 | 0 | +5 |
| Exercise 💪 | -10 | 0 | 0 | +5 | -2 |

> These can be extended dynamically via the **choices table** in the database.

### **3️⃣ Player Stats**
- **Time** (main currency)
- **XP** (knowledge/skill)
- **Fun** (entertainment)
- **Health**
- **Stress** → If Stress > 100 → Burnout → Game Over

### **4️⃣ Random Events**
- Triggered occasionally using the **random** module.
- Examples:
  - “You found an extra 5 time coins ⏳.”
  - “You got stuck in traffic 🚦. Lose 10 time.”
  - “You discovered a life hack ⚡. Gain +3 XP.”

### **5️⃣ Game Endings**
When time hits 0, the game assigns a title based on stats:

| Stats Condition | Ending Title |
|----------------|--------------|
| High XP | “Code Monk 👨‍💻” |
| High Fun | “Party Legend 🍻” |
| High Health | “Zen Master 🧘” |
| High Stress | “Burnout Zombie 🧟” |
| Balanced Stats | “Master of Time ⏳” |

---

## 🔹 Python Modules Used

| Module | Purpose |
|--------|---------|
| `random` | Trigger random events, random rewards |
| `time` | Add suspense with delays, simulate in-game days |
| `os` | Clear the console screen for clean UI |
| `textwrap` | Format text neatly for story narration |

> Minimum version: `random` + `time`. Optional: `os`, `textwrap`.

---

### TroubleShooting

#### Common Issues
1. **`Module not found` errors**
- make sure you installed the requirements from `requirements.txt`
- make sure to run the command from same directory

### Future Enhancements

The core game is complete, but Time Scape is ready for expansion. Future development will focus on enriching the simulation, boosting replayability, and enhancing the player experience:

- Advanced Game Stages: Introduce distinct phases like Student, Job, and Retirement, each featuring unique choices, stat dependencies, and custom success/failure conditions.

- Dynamic Choice Unlocking: Implement a mechanism to unlock special, high-impact actions (e.g., "Invest in Crypto 📈," "Launch Startup 💡") once a player hits specific XP thresholds or accumulates wealth/health.

- Persistent Achievements: Enhance the achievement system by using a new GET endpoint to check if an achievement has been previously earned, ensuring they are unlocked only once per player.

- Fatigue and Energy Mechanics: Introduce a separate Energy/Fatigue stat that limits the frequency of certain actions (like coding or exercise), making the "Sleep" action strategically essential.

- Leaderboard Integration: Build a simple public leaderboard API endpoint to track high scores based on longest survival time or final balanced stats, encouraging competition.

- Web UI Polish: Upgrade the Streamlit interface with more interactive plots and custom components for a truly professional, data-rich dashboard feel.


### Support 
- if any complaints or errors , please mail to <compaints.timescape@gmail.com>

