import pandas as pd
import numpy as np
import random

def generate_shot_data(num_samples=10000):
    """
    Generate a comprehensive dataset for penalty shootout simulation
    
    Columns:
    - shot_x: Horizontal shot coordinate (0-400)
    - shot_y: Vertical shot coordinate (0-300)
    - shot_power: Shot power (1-10)
    - shot_angle: Shooting angle (-45 to 45 degrees)
    - goalkeeper_skill: Goalkeeper skill level (0-10)
    - goalkeeper_reaction_time: Reaction time (ms)
    - goal_scored: Binary outcome (1 = goal, 0 = saved)
    """
    data = {
        'shot_x': [],
        'shot_y': [],
        'shot_power': [],
        'shot_angle': [],
        'goalkeeper_skill': [],
        'goalkeeper_reaction_time': [],
        'goal_scored': []
    }
    
    # Goal dimensions
    GOAL_WIDTH = 200
    GOAL_HEIGHT = 100
    GOAL_X = 100  # Starting X of goal
    GOAL_Y = 50   # Starting Y of goal
    
    for _ in range(num_samples):
        # Generate shot coordinates within goal area
        shot_x = random.uniform(GOAL_X, GOAL_X + GOAL_WIDTH)
        shot_y = random.uniform(GOAL_Y, GOAL_Y + GOAL_HEIGHT)
        
        # Shot power with more realistic distribution
        shot_power = np.random.beta(5, 2) * 10  # Skewed towards higher power
        
        # Shooting angle
        shot_angle = np.random.normal(0, 15)  # Centered around 0, with spread
        
        # Goalkeeper characteristics
        goalkeeper_skill = random.uniform(0, 10)
        goalkeeper_reaction_time = random.uniform(100, 500)  # milliseconds
        
        # Goal scoring probability based on multiple factors
        goal_prob = (
            (shot_x > GOAL_X + GOAL_WIDTH * 0.2) and  # not too close to posts
            (shot_x < GOAL_X + GOAL_WIDTH * 0.8) and
            (shot_y > GOAL_Y + GOAL_HEIGHT * 0.2) and
            (shot_y < GOAL_Y + GOAL_HEIGHT * 0.8) and
            (shot_power > 7) and  # high power
            (goalkeeper_skill < 5)  # lower goalkeeper skill
        )
        
        goal_scored = 1 if goal_prob else 0
        
        # Append to dataset
        data['shot_x'].append(shot_x)
        data['shot_y'].append(shot_y)
        data['shot_power'].append(shot_power)
        data['shot_angle'].append(shot_angle)
        data['goalkeeper_skill'].append(goalkeeper_skill)
        data['goalkeeper_reaction_time'].append(goalkeeper_reaction_time)
        data['goal_scored'].append(goal_scored)
    
    return pd.DataFrame(data)

# Generate and save dataset
dataset = generate_shot_data(50000)
dataset.to_csv('../data/advanced_shots_data.csv', index=False)
print(f"Dataset generated with {len(dataset)} samples")
print(dataset.describe())