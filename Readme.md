# TicNova

TicNova is a desktop-based local two-player Tic-Tac-Toe game built with Python and Pygame. It features a persistent player profile system, stat tracking across matches, level-based session progression, and a final session summary.

---

## Features

### Core Gameplay
* **Classic 3×3 Grid:** Standard local two-player Tic-Tac-Toe mechanics.
* **Mouse-Driven Controls:** Players click on empty cells to place markers.
* **Turn Order:** Player X always moves first at the start of each level.
* **Win & Draw Detection:** Evaluates rows, columns, and both diagonals after each move.
* **Visual Highlight:** Draws a yellow strike line across the winning combination.
* **Move Tracking:** Tracks and displays the number of moves made in each level.
* **Quick Reset / Next Level:** Press `R` after a game concludes to immediately start the next level.

### Persistent Player Profiles
* **Profile Creation:** Create custom player profiles (up to 18 characters).
* **Tracked Statistics:** Each profile permanently records:
  * Name
  * Wins
  * Losses
  * Draws
  * Total games played
  * Personal match history
* **Selection Safeguards:** The same profile cannot be selected as both Player X and Player O simultaneously.
* **Automatic Updates:** Player statistics update automatically after each finished match.

### Main Menu & Player Selection
* **Main Menu Interface:** Manage selections for Player X and Player O, create new profiles, start matches, or clear data.
* **Numeric Selection:** Select existing profiles quickly using the number keys (`1`, `2`, etc.).
* **Live Stats Preview:** View lifetime player stats directly while selecting a profile.
* **Direct Creation:** Create new profiles on demand from the selection screen.

### Level & Session System
* **Level Progression:** Each completed round advances the match to a new **LEVEL**.
* **In-Game Session Panel:** Displays the latest **3 levels** played during the current session, showing:
  * Level number
  * Player X and Player O names
  * Winner and match outcome
  * Move count
* **Session Finalization:** Press `F` to finish the current series and calculate the overall session winner based on level wins.
* **Tie Handling:** Declares an overall draw if both players finish the session with an equal number of wins.

### Final Result Screen
When a session is concluded via `F`, a comprehensive report displays:
* Overall lifetime stats for Player X and Player O.
* Total wins for each player within the current session.
* Total draws and total games played in the session.
* Final session winner (or draw).
* Navigation options to start a new game or return to the main menu.

---

## Data Storage: Persistent vs. In-Memory

| Data Type | Storage Method | Persistence | Description |
| :--- | :--- | :--- | :--- |
| **Player Profiles & Lifetime Stats** | `data.json` | **Persistent** | Saved to disk. Retained across application restarts. |
| **Session History (`session_history`)** | RAM / In-Memory | **Session-Only** | Exists only while the current session runs; resets on exit. |

> **Note:** The `data.json` file is managed automatically by the application and is created or updated whenever player data is saved or modified.

---

## Controls

| Key / Input | Context | Action |
| :--- | :--- | :--- |
| **Left Mouse Click** | Game Board | Place marker (**X** or **O**) in an empty cell |
| `1` | Main Menu | Select profile for **Player X** |
| `2` | Main Menu | Select profile for **Player O** |
| `N` | Menu / Selection | Create a new player profile |
| `ENTER` | Main Menu / Input | Start game (requires both players selected) / Confirm player name |
| `R` | Game Board | Restart current level / Advance to next level |
| `F` | Game Board | Finish current session and display final results |
| `C` | Main Menu | Clear all saved player data from disk |
| `ESC` | Menus / Submenus | Return to previous menu or main menu |
| **Window Close (`X`)** | Anywhere | Exit the application |

---

## Technologies Used

* **Python 3** — Core application programming language.
* **Pygame** — Display management, event loop handling, 2D graphics rendering, and font processing.
* **JSON (`json`)** — Python standard library module used for data serialization and persistent disk storage.
* **OS (`os`)** — Python standard library module used for handling file paths and checking filesystem status.

---

## Requirements

* Python 3.8 or higher
* `pygame`

---

## Installation

1. Ensure Python 3 is installed on your system.
2. Install the required `pygame` dependency using `pip`:

```bash
pip install pygame
```

---

## Running the Game

Launch the application directly with Python from the project directory:

```bash
python tic_nova.py
```

---

## Project Structure

```text
├── tic_nova.py    # Main executable script containing all game logic, rendering, and UI states
├── data.json      # Persistent storage file for player profiles and lifetime stats (auto-generated)
└── README.md      # Project documentation
```

### File Details
* **`tic_nova.py`**: Contains the complete source code, including state machine management (menu, player selection, gameplay, final screen), drawing routines, event handling, and data read/write logic.
* **`data.json`**: Holds profile structures, win/loss/draw records, and historical player logs. If absent, it will be generated upon saving player data.
* **`README.md`**: Provides technical overview, controls, rules, and setup instructions.

---

## Future Improvements

The following items are planned enhancements for future iterations:

* **AI Opponent:** Single-player mode featuring variable difficulty levels (e.g., Minimax algorithm).
* **Online Multiplayer:** Networked socket connections for remote head-to-head play.
* **Persistent Session History:** Writing session level logs to disk alongside profile records.
* **Audio Integration:** Sound effects for moves, menu interactions, victories, and draws.
* **Custom Themes:** Configurable board color schemes and custom UI accents.
* **Profile Management:** Options to rename or delete individual player profiles without clearing the entire database.

## 👨‍💻 Author

<<<<<<< HEAD
Developed by **[Your Name / Your GitHub Profile]([https://github.com/your-username](https://github.com/amiralimii/Ticnova-PyGame.git))**.
=======
Developed by **[Your Name / Your GitHub Profile](https://github.com/amiralimii/Ticnova-PyGame.git)**.
>>>>>>> 1543ce2 (change something)
