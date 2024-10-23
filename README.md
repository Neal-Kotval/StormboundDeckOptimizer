# StormboundDeckOptimizer

Welcome to the **Stormbound Deck Optimization** project! This is a Python-based simulation designed to analyze and optimize mana usage in the game **Stormbound**. If you’re unfamiliar with Stormbound, it’s a strategy card game where players build decks of 12 cards and use those cards in turns to destroy the enemy's base.

This project explores ways to **optimize the mana economy** in Stormbound by minimizing mana wastage through various mathematical techniques. It’s the first step in an ambitious multi-part series aiming to find the **best deck** in Stormbound.

## Project Overview

### Stormbound Game Basics
In **Stormbound**, players use decks of 12 cards, each with unique abilities and mana costs. Each player draws a hand of 4 cards from their deck and uses mana to play cards each turn. The mana budget increases by 1 each turn, but sometimes, if all cards in hand cost more than the available mana, **mana is wasted**.

Our goal in this project is to **minimize mana wastage** by analyzing all possible hands and finding the best way to play them based on the available mana each turn.

### Roadmap
This project is divided into three phases:
1. **Mana Optimization**: Focus on mana wastage, mana curve, and the overall mana economy.
2. **Card Value Optimization**: Analyze card values based on abilities and how they contribute to winning games.
3. **Synergy Optimization**: Investigate how cards work together to create the best deck synergy.

## Phase 1: Mana Optimization

### The Rules
In Stormbound, each card has a mana cost between 1 and 9, and players draw 4 cards per turn from a deck of 12 cards. We’re focusing on optimizing the **mana economy**—specifically, minimizing the **wasted mana** when the cards in hand exceed the available mana for that turn.

### The Mana Curve
A key concept in Stormbound deck analysis is the **mana curve**, which helps to balance how much mana can be spent per turn and how well cards can be played. We aim to optimize two things:
1. **Mana Line**: How efficiently the mana is spent.
2. **Cards Line**: How many cards can be played per turn.

The **ideal mana line** stays high and stable, while the **ideal cards line** rises quickly and remains stable. Our simulation calculates this based on the possible hands drawn and the available mana per turn.

### Idealizing the Mana Curve
In our simulation:
- We analyze all possible hands, which involves 495 combinations from the 12-card deck.
- For each hand, we calculate the possible subsets of cards that can be played and sum their mana costs.
- We select the subset that **maximizes mana usage** while staying within the mana budget, and calculate the leftover mana as wasted mana.

### Formula Overview
We’ve created a mathematical formula to model this and implemented it in Python. Here’s a simplified version:
- For each turn, calculate all possible **subsets of cards** in hand.
- Choose the subset that uses the most mana but doesn’t exceed the turn’s mana budget.
- Track how much mana is wasted each turn and aim to minimize this over multiple turns.

## Phase 2: Genetic Algorithms for Deck Optimization
Analyzing all possible decks (over **282 billion combinations**) would require an enormous amount of computational power. Instead, we use **genetic algorithms** to evolve better decks over time.

### Genetic Algorithm Approach
1. Decks are treated like "genes," and they "reproduce" by having children (new decks).
2. Decks compete based on their **fitness**, where the **fitness function** is the **negative of their total mana wastage**—the lower the mana wastage, the better the fitness.
3. Over many generations, the genetic algorithm will converge toward a deck that minimizes mana wastage.

This approach gives us a **near-optimal solution** for the best mana-efficient deck without requiring astronomical computing power.

## Phase 3: Drawing Mechanics
Stormbound’s drawing mechanics affect the randomness of drawing cards. In this phase, we:
1. **Weight each card**: Initially, each card gets a weight. After playing or drawing a card, the weights adjust based on certain rules.
2. **Action Options**: We can play, draw, or cycle cards, each affecting the weights and available cards.
3. **Branching Hands**: We calculate how hands evolve based on cards drawn and played, using the weights to simulate drawing probabilities.

### Drawing Formula
Each card in the deck starts with a weight, and the weights adjust every time a card is drawn or played.

- When a card is played, all other cards' weights are updated based on their original weight.
- When a card is drawn, its weight is reset.
- When a card is cycled, it counts as both a play and a draw, affecting the entire deck’s weights.

This system models how Stormbound’s drawing mechanics work and helps predict future draws based on previous actions.

## How the Python Simulation Works

### Mana Curve Optimization
1. **Hands and Subsets**: The simulation breaks the deck into 495 possible hands (combinations of 4 cards). For each hand, it calculates all possible subsets (ways to play cards) that are under the available mana budget.
2. **Maximizing Mana Usage**: The subset that maximizes mana usage without exceeding the mana budget is chosen, and the remaining mana is calculated as **wasted mana**.
3. **Running Over Multiple Turns**: The simulation runs over multiple turns, tracking how much mana is wasted, and calculates an average **wasted mana** per deck.

### Genetic Algorithm Approach
- Decks evolve over many generations, and their **fitness** is determined by minimizing the total mana wastage.
- **Children decks** inherit traits from their parents and compete with each other to find the best solution.
- This approach provides a near-optimal deck configuration for minimal mana wastage.

### Installation & Usage (NOT FINISHED)

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/stormbound-mana-optimization.git
    cd stormbound-mana-optimization
    ```

2. **Run the simulation**:
    ```bash
    python mana_simulation.py
    ```

3. **Modify the Deck**:
    You can modify the `deck` list in the script to simulate different deck combinations. For example:
    ```python
    deck = [1, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 6]
    ```

4. **Output**:
    The simulation will output the **total mana wasted** for the given deck configuration.

### Future Enhancements
- **Value Optimization**: In the next phase, we’ll explore how to assign value to cards and optimize the deck for both mana and value efficiency.
- **Synergy Analysis**: We’ll also study how different cards synergize with each other to create the ultimate deck.
