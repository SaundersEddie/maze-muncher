# Maze Muncher

Just my initial waffling of a README... 


Maze Muncher is a small Pac-Man-inspired game built in Python using Pygame Community Edition.

The goal of the project is to create a compact, playable arcade-style game while keeping the underlying game logic clean, testable, and separate from the rendering layer.

This is intended to be a quick-fire coding project rather than a full recreation of the original Pac-Man. The focus is on solid structure, sensible scope, automated tests, and actually finishing the thing.

## Project Goals

* Build a simple maze-based arcade game
* Keep core game logic independent from Pygame where practical
* Use automated tests from the beginning
* Maintain a small and achievable feature set
* Produce a playable project that can be expanded later
* Avoid turning a quick project into a three-month archaeological dig

## Planned Features

The initial version is expected to include:

* One fixed maze
* Grid-based player movement
* Walls and valid movement paths
* Collectible pellets
* Power pellets
* Score tracking
* Player lives
* At least one enemy
* Collision handling
* Win and game-over states
* Keyboard controls
* Simple Pygame rendering

Additional features may be considered after the first playable version is complete.

## Technical Approach

Maze Muncher separates game rules from graphics wherever possible.

Pygame will handle:

* Window creation
* Keyboard input
* Drawing
* Audio
* Frame timing

Regular Python modules will handle:

* Board data
* Movement rules
* Collision detection
* Scoring
* Game state
* Enemy behaviour

This makes the important parts of the game easier to test without opening a graphical window.

## Requirements

* Python 3.13
* Pygame Community Edition
* pytest
* pytest-cov

Python 3.14 is intentionally not supported for this project due to dependency compatibility issues encountered during setup.

## Development Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the project and development dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install pygame-ce pytest pytest-cov
```

## Running Tests

Run the test suite with:

```bash
python -m pytest
```

Run tests with coverage:

```bash
python -m pytest --cov=maze_muncher
```

## Current Project Structure

```text
maze-muncher/
├── src/
│   └── maze_muncher/
│       └── __init__.py
├── tests/
│   └── test_environment.py
├── .python-version
├── pyproject.toml
└── README.md
```

The structure will expand as the board, player, enemy, scoring, and rendering systems are added.

## Current Status

The initial project environment is complete.

Current progress:

* Repository created
* Python 3.13 configured
* Virtual environment working
* Project dependencies installed
* Source package created
* Test directory created
* Initial environment test passing

The next development step is to create the board representation and test valid and invalid movement through the maze.

## Testing Philosophy

Tests are not being added after the game is finished as decorative proof that everything probably works.

The project will test game rules as they are introduced, including:

* Wall collisions
* Valid movement
* Pellet collection
* Score changes
* Player and enemy collisions
* Remaining lives
* Win conditions
* Game-over conditions
* Enemy movement decisions

Rendering tests will be kept limited. The goal is to test behaviour, not whether Pygame successfully drew a yellow circle.

## Scope

This project is inspired by classic maze arcade games but is not intended to be an exact recreation of Pac-Man.

Maze Muncher will use its own code, layout, presentation, and project structure.

## License

This project is licensed under the MIT License.
