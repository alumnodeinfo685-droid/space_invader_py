# Space Invader Py

A small Python game built with a clean architecture approach and Pygame integration.

## Overview

This project implements a simple Space Invader-style game using Python and Pygame. The codebase separates domain logic, use cases, input/output adapters, and infrastructure.

## Project structure

- `run.py` - main entrypoint that boots the game.
- `src/domain/` - domain entities and game state definitions.
- `src/use_cases/` - game engine and business logic.
- `src/adapters/` - adapter interfaces and Pygame-specific adapter implementations.
- `src/infrastructure/` - Pygame game loop and platform-specific infrastructure.

## Requirements

- Python 3.11+ (or compatible Python 3 version)
- `pygame`

## Setup

1. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install pygame
```

## Run

From the project root:

```powershell
python run.py
```

## Notes

- The game starts from `run.py` and uses `GameEngine` to initialize enemies and wire input/output adapters.
- Pygame is used for rendering and input handling.
