# 🎮 AirWave Adventure — Gesture-Controlled Game

> **A real-time, controller-free game controlled entirely by your index finger using a webcam!**

---

## 🚀 Demo

> Move your **index finger** in front of your webcam → your character moves on screen.  
> Dodge cars 🚗 · Collect coins 🪙 · No keyboard. No mouse. Just your hand!

---

## 📌 About The Project

**AirWave Adventure** is a real-time **computer vision-based game** built in Python.  
It uses **MediaPipe** for hand landmark detection and **OpenCV** for webcam processing to track the player's index finger and map it to character movement in a **Pygame** environment.

This project demonstrates how **Human-Computer Interaction (HCI)** can be reimagined through gesture recognition — eliminating traditional input devices entirely.

---

## 🧠 How It Works

```
Webcam Feed → OpenCV → MediaPipe Hand Detection
           → Index Finger Tip (x position)
           → Maps to Character Position on Screen
           → Pygame renders game in real-time
```

1. Webcam captures live video frames via OpenCV
2. MediaPipe detects hand landmarks (21 key points)
3. Index finger tip (`INDEX_FINGER_TIP`) X coordinate is extracted
4. Character position is updated to match finger movement
5. Collision detection handles cars and coin collection
6. Flask server receives game-over event with final score

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **MediaPipe** | Real-time hand landmark detection |
| **OpenCV** | Webcam capture & frame processing |
| **Pygame** | Game rendering & event loop |
| **Flask** | Backend server for score handling |

---

## 🎯 Features

- ✅ **Real-time finger tracking** via webcam — 30 FPS
- ✅ **No keyboard/mouse required** — fully gesture-controlled
- ✅ **Randomized vehicle & coin spawning** — no overlap logic
- ✅ **Collision detection** — game ends on vehicle hit
- ✅ **Coin collection system** — score tracked live
- ✅ **Flask API integration** — final score posted on game over
- ✅ **Visual hand landmarks** drawn on webcam feed

---

## 📁 Project Structure

```
AirWave-Adventure/
├── game1.py                  # Main game loop + gesture control
├── server.py                 # Flask backend for score tracking
├── Airwave Adventure.pptx    # Project presentation
├── project algorithms.docx   # Algorithm documentation
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/KavyaThakar/AirWave-Adventure.git
cd AirWave-Adventure
```

### 2. Install Dependencies
```bash
pip install pygame opencv-python mediapipe flask requests
```

### 3. Add Game Assets
Place these image files in the project root:
```
sky.png
road_texture.png
left_building.png
right_building.png
car.png
character.png
coin1.png
```

### 4. Run the Flask Server
```bash
python server.py
```

### 5. Run the Game
```bash
python game1.py
```

---

## 🎮 How To Play

| Action | Gesture |
|---|---|
| **Move Left** | Move index finger left |
| **Move Right** | Move index finger right |
| **Collect Coin** | Move character over coin |
| **Game Over** | Character hits a vehicle |

---

## 📊 Game Logic

- **3 vehicles** and **3 coins** active on screen at all times
- Objects move downward at speed 5 px/frame
- When an object exits screen bottom → respawns at top with random X position
- **Safe zone** around player spawn point prevents instant collision at game start
- Final score (coin count) is sent to Flask server via POST request on game over

---

## 🔮 Future Enhancements

- [ ] Multiple gesture controls (fist = pause, two fingers = speed boost)
- [ ] Difficulty levels (increasing vehicle speed)
- [ ] High score leaderboard
- [ ] Sound effects and background music
- [ ] Mobile deployment via browser-based webcam

---

## 👩‍💻 Author

**Kavya Thakar**  
B.Tech CSE — Marwadi University, Rajkot  
📧 kavyathakar12@gmail.com  
🔗 [GitHub](https://github.com/KavyaThakar)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
