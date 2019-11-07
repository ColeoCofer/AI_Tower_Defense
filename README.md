#### AI_Tower_Defense
Artificial Intelligence Project PSU 2019 AI Tower Defense Game

We built this tower defense game from scratch using Pygame with the motivation of training an AI agent that could exploit flaws in the games mechanics and ultimately outplay us at the game. 

### Modes
There is a manual game playing mode with an interface for purchasing and placing towers, as well as a training mode for three different types of AI agents including: Genetics Algorithm, Q-Learning, and Deep Q-Learning. This mode does not render the screen for added efficiency, and will run multiple games in parallel if `PARALLEL_MODE` is set to `True`.

### Setup
Install the following packages:
```
pygame==1.9.6
joblib
tensorflow==1.13.1
matplotlib==3.1.0
numpy==1.16.4
joblib==0.13.2
```

### Run the game
Simply run `python3 main.py` located in the `AI_Tower_Defense/src/` directory.
See main.py to change the game mode. For example, set `GAME_MODE = MODE.manual` to play the game manually.

Performance Note: You may need to run the game in fullscreen mode if you have a high resolution monitor (especially on MacOS). Enable fullscreen mode by setting `FULLSCREEN_MODE` to `True` in `gameConstants.py`.

If using latest mac OSX Mojave, you must have the latest version of python installed or graphics will not render.
I'm currently using `3.7.3` and it works great.

### Results
We were very pleased at the outcome of our AI agents. The most successful agent was trained using a genetic algorithm, which ended up exploiting the game in a manner that we did not expect. The agent received much higher scores than us humans could. When analyzing it's tower placements after training, we discovered that it concentrated towers at the end of the path near the "City" tower - which is a given default tower that each player gets and is placed at the end of the path. This made sense to us because the City can also attack, and you are wasting resources by putting towers near the front during the early game. After learning about this and changing our tactics we could achieve higher scores than the AI, but not by much. 

# Genetic Algorithm
Here is a graph of an agent playing games trained using a genetic algorithm. Each data point is an average score for ten games that ran in parallel, for a total of 1000 games. You can see it getting better and better scores as it learns more about the game play. <br>
![Results from GA agent.](https://raw.githubusercontent.com/ColeoCofer/AI_Tower_Defense/master/AI_Tower_Defense/Images/GA_Results.png)
<br>Here is a random game sample to see how the GA agent placed towers after it figured out how to play the game.
![Example tower placement from a randomly selected game.](https://raw.githubusercontent.com/ColeoCofer/AI_Tower_Defense/master/AI_Tower_Defense/Images/GA_Gameplay.png)

For more information about the algorithms used, please view our slide deck: https://docs.google.com/presentation/d/1mFf90QteQjmz9a49Rur2uVP5XGhfNgp2cQkRj2i9yeQ/edit?usp=sharing

Sample video of gameplay: https://www.youtube.com/watch?v=bxZmVyfHosE

### Assets
All assets are royalty free - provided from https://opengameart.org/art-search?keys=tower&page=1.
![Example of the enemy and tower assets.](https://raw.githubusercontent.com/ColeoCofer/AI_Tower_Defense/master/AI_Tower_Defense/Images/Assets.png)

### License
This project is licensed under the terms of the MIT license.



