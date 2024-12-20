# Fall 2024 Projects

This repository contains various projects completed during the Fall 2024 semester as part of my **Data Science** studies at the University of Wisconsin-Madison.

## Overview

The projects in this repository showcase the use of *Machine Learning* and *Artificial Intelligence*. The emphasis of this directory of projects will be on machine learning techniques (including various neural networks), styles, and methods.

## Projects

### 1. hw2
- **Description**: The Bayes rule is one of the most fundemntal concepts in the field of probability theory, statistical probability, and generative language methods. This project will utilize the Bayes rule to determine if various documents are written in English or Spanish based soley upon the amount of times a letter occurred in the mystery documents.
- **Key Techniques**: Bayes Rule, Probability Theory
- **Files**: `hw2.py`, `hw2/samples/*`

### 2. hw3
- **Description**: *Principle Component Analysis* (PCA) is one of the most well known data science techniques and is used for dimensionality reduction. Often times we can approximate a data set using fewer dimensions by defining new coordinates where the variance is large so that we can capture more information with less numbers/features. This project will perform PCA on the Label Faces in the Wild dataset (13233 face images of size 64x64) and eventually reconstruct and distort them.
- **Key Techniques**: PCA, Dimensionality Reduction, Reconstruction, Distortion
- **Files**: `hw3.py`

### 3. hw4
- **Description**: Another useful tool is finding patterns and/or finding a way to determine how similiar certain items are to each other (Data Mining), and one of the ways this can be accomplished is through something called *Hierarchical Agglomerative Clustering* (HAC). The end goal of this project is to essentially create a Dendrogram (a diagram that illustrates which items are similar to which items, and by how much?) which shows the hierarchical clustering (similarity groups) of a dataset.
- **Key Techniques and Libraries**: Hierarchical Agglomerative Clustering, Distance Metrics, Distance Matrix, NumPy, Matplotlib, DictReader
- **Files**: `hw4.py`, `function.py`, `countries.csv`

### 4. hw5
- **Description**: Arguably the most important aspect of machine learning is a method called *Gradient Descent*, which is what makes the machine "learn". Basically, we want to minimize a cost/loss function so that our model performs its duty the best. To do this, we need to calculate the gradient of the cost function and adjust the weights so that it becomes zero, thus focusing in on a minimum of the cost function. This project will examine the most basic case, linear regression, and will use gradiant descent as a way to verify the closed-form solution to the problem, which is fitting a linear regression to a dataset about ice formation as a function of year. The grand idea is that we want to construct a model to predict the number of icy days based upon some amount of features.
- **Key Techniques and Libraries**: Linear Regression, Gradient Descent, Perceptron, Pandas, Matplotlib, NumPy 
- **Files**: `hw5.py`, `ice.csv`

### 5. hw6
- **Description**: Welcome to one of the most powerful tools in Data Science, *Neural Networks*. In this project we will implement a neural network to classify images of the MNIST database using PyTorch. Neural Networks are incredibly powerful models that serve a variety of purposes, one of the most useful being classification. For example, the 2024 Nobel Prize in Physics was given to two people (John J. Hopfield and Geoffrey Hinton) for creating specialized neural networks in the field of physics. It's now your turn to implement a classic version of a neural network, while gaining familiarity with PyTorch!
- **Key Techniques**: Neural Networks, Data Loaders, Training a Neural Network, Evaluating a Neural Network, Predicting Labels, Gradient Descent, PyTorch
- **Files**: `intro_pytorch.py`, `data/FashionMNIST/*`

### 6. hw7
- **Description**: Another high-level, performance-enhancing neural network is called a *Convolutional Neural Network*. The network takes in an image, applies some filter-like matrix operations, condenses the numbers, and then outputs which classification the image most likely belongs to. Typically this type of neural network performs better than a classic, fully connected neural network (which was made in the previous project). This project will build and implement a Convolutional Neural Network to classify the Miniplaces challenge dataset, which contains 120,000 color images of various places (note: this setup is called LeNet-5, and is widely renowned for its historical influence on neural networks and deep learning).
- **Key Techniques**: Convolutional Neural Networks, Parameter Hypertuning, Training, Evaluation, PyTorch, PyTorch-Vision, tqdm
- **Files**: `student_code.py`, `train_miniplaces.py`


### 7. hw8
- **Description**: We will now shift our attention to game theory. One of the biggest, most recent accomplishments was that the grand master of the game Go was beaten by a computer, marking a historic landmark in the field of computer and data science. The outcome space is something on the order of 10^150, and it wasn't expected to have succeeded for at least another 5 years. In spirit of such an instrumental event, we will be coding a solver to solve a 3x3 puzzle tile game, where the goal is move the tiles into their goal state, usually to create a picture. This project will introduce the idea of a *Heuristic*, and incorporate this additonal information into a tree search. Therefore this project will implement the search algorithm **A*** to solve such a puzzle.
- **Key Techniques**: Breath-first and depth-first search algorithms, Heuristics, distance calculation, optimization, heapq, A* algorithm.
- **Files**: `funny_puzzle.py`, `h8Debug.ipynb`

  
### 8. hw9
- **Description**: To continue with our knowlege of game theory, we will develope an AI to play the game Teeko. You can think of Teeko as a game similar to connect-4, but the grid is 5 by 5 and players may move their tiles/pieces. We will implement a very important game theory algorithm called **Minimax**. Addtionally, in order to maximize the possible solutions states our AI can explore, we will implement alpha-beta pruning on minimax. The goal of this alogrithm is to be other, similar AIs that have their own programming. Like the last project, you will also need to implement a heuristic. Your huristic will be very important, as this will be what leads to the success of your AI over other AIs. 
- **Key Techniques**: Minimax algorithm, alpha-beta pruning, Heuristics, distance calculation, optimization, state expansion. 
- **Files**: `game.py`


### 9. hw10
- **Description**: To conclude the course and our experience with game theory, we will shift our attention to a technique called **Q-Learning**. In this project, we will focus on various actions that a player (you) can take in a given state, and the rewards associated with the aformentioned actions and their states. The goal of this project will be to maximize the rewards given from taking certain actions. The main algorithms to do this are called Q-Learning and SARSA, and this project will implement them both. We will take the classic example of starting from a corner of a grid, and the goal is to get to the other side. The catch is that there is a cliff along the most direct path, so your character (AI) will attempt to navigate the environment. 
- **Key Techniques**: Q-Learning, SARSA, Q-Tables, Gymnasium, discount factors, actions, states, Bellman Equation. 
- **Files**: `Q_Learning.py`, `SARSA.py`, `Q_TABLE_QLearning.pkl`, `Q_TABLE_SARSA.pkl`
