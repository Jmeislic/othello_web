Othello AI Web Application

This project is a Flask-based web application that allows users to play the game of Othello (Reversi) against multiple AI opponents with varying levels of intelligence and strategy.

The goal of this project is to explore different approaches to game-playing AI, ranging from simple baselines to reinforcement learning.

Features

Interactive Flask web interface for playing Othello in the browser

Multiple AI opponents with increasing complexity

Real-time move validation and game state updates

Designed for experimentation and comparison between AI strategies

AI Opponents

The application supports three different types of AI players:

1. Random Bot

The Random Bot serves as a baseline opponent.

Selects a valid move uniformly at random

No strategic reasoning

Useful for testing and initial training

2. Heuristics Bot

The Heuristics Bot uses classic Othello strategies to make decisions.

Key priorities include:

Maximizing corner captures

Limiting opponent mobility

Favoring stable positions and avoiding risky moves when possible

This bot represents a traditional, rule-based approach to Othello AI.

3. PPO-Trained AI Agent

The most advanced opponent is a reinforcement learning agent trained using Proximal Policy Optimization (PPO).

Training Details

The PPO agent was trained through self-play and competitive play against:

The Random Bot

The Heuristics Bot

An older version of itself

This mixed training environment helps the model:

Avoid overfitting to a single strategy

Adapt to diverse play styles

Improve long-term decision-making

Technology Stack

Python

Flask (web server and routing)

HTML / CSS / JavaScript (frontend)

Reinforcement Learning (PPO)

Custom Othello game engine and AI logic

Running the Application

To start the Flask web server locally:

python app.py


Once running, open your browser and navigate to:

http://localhost:5000


From there, you can choose an AI opponent and begin playing.

Project Goals

Compare rule-based and learning-based AI strategies

Demonstrate reinforcement learning applied to classic board games

Provide an interactive environment for AI experimentation

Future Improvements

Adjustable difficulty levels

Visual indicators for AI decision reasoning

Additional reinforcement learning algorithms

Online multiplayer support
