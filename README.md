# Maze Muncher

Maze Muncher is a small maze-based arcade game built in Python using Pygame Community Edition.

The project began as a quick-fire coding exercise: build something playable, keep the scope under control, test the important logic, and actually finish the thing instead of allowing it to become another glorious monument to unfinished ambition.

It is inspired by classic maze-chase games, but it uses its own code, maze layout, presentation, structure, and gloriously named enemies: the meanies.

## Current Status

Maze Muncher is now fully playable.

The player can navigate the maze, collect pellets, activate power mode, eat frightened meanies, lose lives, pause the game, win by clearing the board, or reach game over by making several questionable navigational decisions.

The main gameplay systems are working and covered by automated tests. The remaining work is primarily balancing, options, additional polish, documentation, and final release preparation.

## Features

- One fixed maze
- Grid-based player movement
- Arrow-key and WASD controls
- Wall and boundary collision
- Standard pellets
- Power pellets
- Score tracking
- Three player lives
- Two independently moving meanies
- Random legal enemy movement
- Meanies avoid immediately reversing direction unless trapped
- Player and enemy collision handling
- Temporary power mode
- Frightened meanies move at half speed
- Frightened meanies can be eaten for bonus points
- Individual meanie colors
- Ghost-style meanie rendering
- Player facing direction
- Player mouth rendering
- Life-lost state
- Win state
- Game-over state
- Replay and return-to-menu controls
- Pause and resume
- Music and sound effects
- Separate game logic, rendering, and audio modules
- Automated tests for the core game rules

## Controls

### Menu

| Key | Action |
| --- | --- |
| `Enter` or `Space` | Start the game |
| `Escape` | Quit |

### Gameplay

| Key | Action |
| --- | --- |
| Arrow keys | Move |
| `W`, `A`, `S`, `D` | Move |
| `P` | Pause or resume |
| `Escape` | Pause or resume |

### Win and Game Over Screens

| Key | Action |
| --- | --- |
| `Enter` or `Space` | Play again |
| `Escape` | Return to the main menu |

## Scoring

| Action | Points |
| --- | ---: |
| Collect a pellet | 10 |
| Collect a power pellet | 50 |
| Eat a frightened meanie | 200 |

Power mode lasts for eight successful player moves.

Blocked movement does not reduce the remaining power duration.

## Gameplay

The goal is to collect every pellet in the maze.

The two meanies move independently on a timer. Their movement is random but restricted to valid paths, and they will not immediately reverse direction unless they reach a dead end.

Colliding with a meanie during normal play costs one life and resets the player and meanies to their starting positions.

Collecting a power pellet temporarily turns both meanies blue and slows their movement. During this period, colliding with a meanie eats it, awards bonus points, and returns that meanie to its starting position.

The game is won when every pellet has been collected.

The game ends when the player loses all three lives.

## Technical Approach

Maze Muncher separates gameplay rules from Pygame-specific presentation wherever practical.

### Core Python modules handle

- Board representation
- Position tracking
- Movement rules
- Wall and boundary collision
- Pellet collection
- Power-pellet behavior
- Score calculation
- Player lives
- Game states
- Enemy movement decisions
- Collision resolution
- Enemy resets
- Win and game-over conditions

### Pygame handles

- Window creation
- Keyboard input
- Rendering
- Audio playback
- Timed enemy movement
- Frame timing
- Menu and overlay presentation

This separation keeps the important game behavior testable without requiring a graphical window.

## Project Structure

```text
maze-muncher/
├── assets/
│   └── audio/
│       ├── menu_theme.mp3
│       ├── gameover_theme.mp3
│       └── sfx/
├── src/
│   └── maze_muncher/
│       ├── __init__.py
│       ├── app.py
│       ├── audio.py
│       ├── board.py
│       ├── enemy.py
│       ├── game.py
│       ├── movement.py
│       ├── player.py
│       └── renderer.py
├── tests/
├── .python-version
├── pyproject.toml
└── README.md
```

## Requirements

- Python 3.13
- Pygame Community Edition
- pytest
- pytest-cov

Python 3.14 is intentionally not supported by the current project configuration because dependency compatibility problems were encountered during the original setup.

## Development Setup

### macOS

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

### Windows PowerShell

Create a virtual environment:

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

## Running the Game

```bash
python -m maze_muncher.app
```

## Running Tests

Run the full test suite:

```bash
python -m pytest
```

Run the tests with coverage:

```bash
python -m pytest --cov=maze_muncher
```

## Testing Philosophy

Tests are added as game rules are introduced rather than being bolted onto the project after development.

The test suite focuses on behavior, including:

- Board validation
- Position boundaries
- Valid and invalid movement
- Wall collision
- Pellet collection
- Power-pellet collection
- Score changes
- Power-mode duration
- Player and enemy collisions
- Eating frightened enemies
- Enemy movement decisions
- Multiple-enemy behavior
- Remaining lives
- Player and enemy resets
- Win conditions
- Game-over conditions
- Menu and end-screen keyboard actions

Rendering tests are intentionally limited. The useful question is whether the game behaves correctly, not whether Pygame successfully drew a yellow circle.

## Audio

Maze Muncher includes:

- Menu music
- Game-over music
- Player-start sound
- Meanie-spawn sound
- Pellet-pickup sound
- Power-pellet sound
- Enemy-movement sound
- Meanie-eaten sound
- Life-lost sound
- Victory sound
- Game-over sound

Audio volume controls and final sound balancing remain planned work.

Audio credits and generation details will be added before the final release.

## Remaining Work

The current finishing list includes:

- Music-volume controls
- SFX-volume controls
- Final audio balancing
- Final enemy-speed tuning
- Collision edge-case testing
- Optional pause-menu actions
- Optional lives shown as player icons
- Optional player mouth animation
- Optional warning flash near the end of power mode
- Screenshot and repository presentation
- Final full playthrough
- Final test and coverage run

## Scope

Maze Muncher is not intended to be a complete recreation of Pac-Man.

It is a compact Python arcade project focused on:

- Clean structure
- Testable game rules
- Controlled scope
- Cross-platform development
- Incremental progress
- Reaching a finished, playable result

Additional mazes, enemy personalities, level progression, animation, executable packaging, and other larger features may be considered after the first finished release.

## License

This project is licensed under the MIT License.
