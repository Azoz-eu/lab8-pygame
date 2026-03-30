# Pygame Moving Squares Project

A simple pygame application that displays 10 randomly positioned moving squares on the screen.

## Project Description

This project demonstrates core pygame concepts including:
- Game loop fundamentals (event handling, updating, rendering)
- Sprite movement and velocity
- Boundary collision detection with bouncing behavior
- Object-oriented design with a Square class

## Requirements

- Python 3.7+
- pygame 2.6.1+

## Setup Instructions

### 1. Create and Activate Virtual Environment

```bash
python -m venv .venv
```

**On Windows (PowerShell):**
```bash
.venv\Scripts\Activate.ps1
```

**On macOS/Linux:**
```bash
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python main.py
```

A window will open with 10 colored squares moving randomly across the screen. The squares will bounce off the edges of the window.

## Features

- 10 randomly positioned squares
- Random velocity for each square
- Bouncing behavior at screen boundaries
- Smooth animation at 60 FPS

## Project Structure

```
lab8-pygame/
├── main.py           # Main application entry point
├── README.md         # Project documentation
├── requirements.txt  # Project dependencies
└── .venv/           # Virtual environment (auto-generated)
```

## Future Enhancements

- Add mouse interaction
- Implement collision detection between squares
- Add sound effects
- Create score tracking

## License

This project is for educational purposes.
