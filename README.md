# Penalty Shootout Simulator

An advanced penalty shootout game that uses machine learning to create realistic goalkeeper behavior and shot predictions.

## Features

- Real-time penalty shooting simulation
- Machine learning-powered goalkeeper decisions
- Interactive GUI with smooth animations
- Dynamic difficulty settings
- Comprehensive statistics tracking
- Realistic ball trajectory physics

## Machine Learning Implementation

The game uses:
- Random Forest and Gradient Boosting Classifiers
- Features include shot position, power, angle, and goalkeeper attributes
- Model trained on 50,000 simulated penalty shots
- Scikit-learn for model implementation
- Real-time prediction for goalkeeper movements

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/penalty_shootout_game.git
cd penalty_shootout_game
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Generate training data:
```bash
python data_generator.py
```

4. Train the model:
```bash
python train_model.py
```

5. Run the game:
```bash
python game_gui.py
```

## How to Play

1. Use the sliders to adjust shot power and angle
2. Click anywhere in the goal area to shoot
3. Watch the ball trajectory and goalkeeper's response
4. Track your success rate in the stats panel
5. Adjust difficulty through the Game menu

## System Requirements

- Python 3.7+
- tkinter support
- Minimum 4GB RAM
- Screen resolution: 1024x768 or higher

