# Stickman Obstacle Jumping Game 🎮

A simple OpenGL-based obstacle jumping game where you control a stickman to avoid obstacles.

## 🎯 Game Objectives
* Control the stickman to jump over obstacles
* Avoid colliding with thorns and half circles
* Get the highest score possible

## 🎮 Controls
* **Space** - Jump
* **Mouse Click**:
  * Level selection buttons
  * Pause/Resume button
  * Restart button
  * Exit button

## 🏃 Gameplay Features
### Difficulty Levels
* 🟢 **Easy** - Lower speed and fewer obstacles
* 🟡 **Medium** - Moderate speed and obstacle frequency 
* 🔴 **Hard** - High speed and frequent obstacles

### Game Elements
* **Stickman**: The player character
* **Obstacles**:
  * Thorns - Ground-based obstacles
  * Half Circles - Additional hazards to avoid
* **Score**: Increases as you survive longer

### Game States
* Menu
* Playing
* Game Over

## ⚙️ Technical Requirements
* Python 3.x
* OpenGL libraries:
  * `OpenGL.GL`
  * `OpenGL.GLUT`
  * `OpenGL.GLU`

## 🛠️ Installation
1. Extract the OpenGL zip file
2. Place `myProject.py` in the same directory as the extracted OpenGL files
3. Run the game using:
```bash
python myProject.py