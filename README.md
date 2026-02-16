#  3D Car Racing Game (PyOpenGL)

A simple yet engaging **3D car racing / lane-dodging game** built using **Python and PyOpenGL**.  
The player controls a car on a 3-lane road and must avoid incoming obstacle cars while the game speed increases over time.

---

##  Gameplay Overview

- Control a **player car** driving forward on a 3D road
- Dodge **randomly spawning obstacle cars**
- Speed increases gradually as the **score increases**
- Collision detection ends the game
- Restart anytime after game over

---

##  Technologies Used

- **Python 3**
- **PyOpenGL**
- **GLUT (OpenGL Utility Toolkit)**

---

##  Features

- ✅ 3D perspective road with depth
- ✅ Dynamic lane-based movement
- ✅ Increasing difficulty (adaptive speed)
- ✅ Collision detection system
- ✅ Lighting and material shading
- ✅ Score tracking
- ✅ Restart and exit controls
- ✅ Clean and structured code

---

##  Controls

| Key | Action |
|----|-------|
| ⬅ Left Arrow | Move car left |
| ➡ Right Arrow | Move car right |
| **R** | Restart game (after Game Over) |
| **ESC** | Exit game |

---

##  Game Logic Summary

- The road uses **perspective scaling** for realism
- Lanes are calculated dynamically based on road width
- Obstacle cars spawn at random lanes and move toward the player
- Collision is detected when two cars are in the same lane and close in depth (`z` axis)

---

##  Project Structure

Car Racing/  
│  
├── car_racing.py # Main game source code  
├── README.md # Project documentation  


---

##  How to Run

### 1️⃣ Install Dependencies
```bash
pip install PyOpenGL PyOpenGL_accelerate
```
### 2️⃣ Run the Game

```
python car_racing.py
```
⚠️ Make sure your system supports OpenGL rendering.

## Preview

- Blue car → Player

- Red cars → Obstacles

- White lines → Lane dividers

- Black surface → Road



## Educational Purpose

This project was created for:

- Learning computer graphics

- Understanding 3D transformations

- Practicing game loops & collision detection

- Exploring OpenGL lighting and materials

##  Author

### Mejbah Uddin Bhuiyan
BSc in Computer Science & Engineering  
BRAC University  

## License

This project is intended for educational and academic use.  
You are free to modify, extend, and experiment with the code.  
