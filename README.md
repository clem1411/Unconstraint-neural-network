# Project Title

This project aims to create an AI for playing the game of snake using a genetic algorithm.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)

## Installation

Instructions on how to install and set up the project.

```bash
# Clone the repository
git clone https://github.com/clem1411/Unconstraint-neural-network.git

# Navigate to the project directory
cd '.\Snake AI\'

# Install dependencies
pip install -r requirements.txt
```

## Usage

How to use the project.

```python
# To run the game and train the AI
python snake.py
```

Then 3 options will be available:

- Play the game yourself using the arrow keys : 1
- Use a genetic algorithm to train the AI : 2
  You can choose whether to display the game or not (it will be faster without displaying the game)
  If the current best AI is better than the one existing, it will be saved in the file "bestGenome.json". If you want to save it anyway, modify the fitness in bestGenome.json to 0.
- Use the AI to play the game : 3

# To plot the evolution

python graph.py

It plots the average and the best fitness of each generation and is updated each minute. It is based on the file "fitness_data.csv" which contains the fitness of the best AI and the average fitness of each generation.

```python

```
