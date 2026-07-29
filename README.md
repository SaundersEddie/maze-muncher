# Maze Muncher

Maze Muncher is a small Pac-Man-inspired game built in Python using Pygame Community Edition.

The goal is to create a compact, playable arcade-style game while keeping the underlying game logic clean, testable, and separate from the rendering layer.

This is a quick-fire coding project rather than a full recreation of Pac-Man. The focus is on sensible scope, automated tests, clear structure, and actually finishing the thing.

## Project Goals

* Build a simple maze-based arcade game
* Keep core game logic independent from Pygame where practical
* Add automated tests alongside each feature
* Maintain a small and achievable scope
* Support development on macOS and Windows
* Produce a playable project that can be expanded later

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

Maze Muncher separates game rules from graphics wherever practical.

Pygame will eventually handle:

* Window creation
* Keyboard input
* Drawing
* Audio
* Frame timing

Regular Python modules handle:

* Board data
* Position tracking
* Movement rules
* Wall collision
* Pellet collection
* Game state
* Enemy behaviour
* Scoring

This keeps the important game rules testable without opening a graphical window.

## Requirements

* Python 3.13
* Pygame Community Edition
* pytest
* pytest-cov

Python 3.14 is intentionally not supported for this project due to dependency compatibility issues encountered during setup.

## Development Setup

### macOS

Create the virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### Windows PowerShell

Create the virtual environment:

```powershell
py -3.13 -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

### Install Dependencies

After activating the virtual environment:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

## Running Tests

Run the full test suite:

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
│       ├── __init__.py
│       ├── board.py
│       ├── movement.py
│       └── player.py
├── tests/
│   ├── test_board.py
│   ├── test_environment.py
│   ├── test_movement.py
│   └── test_player.py
├── .python-version
├── pyproject.toml
└── README.md
```

## Current Features

### Board

The board currently supports:

* Rectangular layout validation
* Empty-layout validation
* Position boundary checks
* Wall detection
* Movement validation
* Pellet detection
* Pellet collection
* Remaining pellet counts

### Movement

The movement system currently supports:

* Up
* Down
* Left
* Right
* Calculating the next grid position

### Player

The player currently supports:

* Tracking its current position
* Moving onto valid tiles
* Refusing movement into walls
* Refusing movement outside the board
* Multiple sequential moves

## Current Test Coverage

The test suite currently verifies:

* Python 3.13 is being used
* Empty boards are rejected
* Uneven board rows are rejected
* Positions inside and outside the board are detected
* Walls cannot be entered
* Floor and pellet tiles can be entered
* Direction changes produce the correct coordinates
* The player moves onto valid tiles
* The player remains in place when blocked
* Pellets are detected
* Pellets are removed when collected
* Pellets cannot be collected twice
* Remaining pellets are counted correctly

## Current Status

The project foundation and initial game logic are complete.

Completed so far:

* Repository created
* Python 3.13 configured
* macOS environment tested
* Windows environment tested
* Pygame Community Edition installed
* pytest configured
* Board representation created
* Movement system created
* Player movement created
* Wall collision implemented
* Pellet collection implemented
* Automated tests passing

The next development step is to connect player movement with pellet collection and scoring.

## Testing Philosophy

Tests are being added as game rules are introduced rather than being bolted on after the game is finished.

The project focuses on testing behaviour, including:

* Valid and invalid movement
* Wall collision
* Pellet collection
* Score changes
* Player and enemy collisions
* Remaining lives
* Win conditions
* Game-over conditions
* Enemy movement decisions

Rendering tests will remain limited. The goal is to test game behaviour, not whether Pygame successfully drew a yellow circle.

## Scope

Maze Muncher is inspired by classic maze arcade games but is not intended to be an exact recreation of Pac-Man.

The project will use its own code, maze layout, presentation, and structure.

## License

This project is licensed under the MIT License.
