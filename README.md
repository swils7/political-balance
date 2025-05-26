# Political Balance Game

A card-based political simulation game where you make decisions that affect your popularity with different factions.

## Setup Instructions

1. Make sure you have Python 3.8 or higher installed on your system
2. Clone or download this repository
3. Open a terminal/command prompt in the project directory
4. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
5. Activate the virtual environment:
   - Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source venv/bin/activate
     ```
6. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
7. Run the application:
   ```bash
   python app.py
   ```
8. Open a web browser and go to: http://127.0.0.1:5000

## How to Play

1. You'll see executive orders that require your decision
2. For each order:
   - Swipe left (or press left arrow key) to reject
   - Swipe right (or press right arrow key) to sign
3. Each decision affects your popularity with three factions:
   - Military (✝)
   - Business ($)
   - Citizens (👤)
4. Keep your popularity between 0% and 100% with all factions to stay in power
5. Try to survive as many years as possible!

## Game Over Conditions

The game ends if any faction's popularity reaches:
- 0% (complete disapproval)
- 100% (too much influence)

## Development

This is a beta version for testing. Please report any bugs or feedback to the development team.
