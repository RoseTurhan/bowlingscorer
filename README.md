# Bowling Scorer

## Overview

This project is a simple Python bowling scorer for a complete 10-frame bowling game.

I selected **Option B: Rolls** for the input format. This means the scorer accepts a flat list of rolls in order.

Example input:

```python
["8", "/", "5", "4", "9", "0", "X", "X", "5", "/", "5", "3", "6", "3", "9", "/", "9", "/", "X"]
```

Example output:

```python
[15, 24, 33, 58, 78, 93, 101, 110, 129, 149]
```

## Rules Supported

- `X` or `x` means strike.
- `/` means spare.
- `0-9` means the number of pins knocked down.
- A strike is worth 10 plus the next two rolls.
- A spare is worth 10 plus the next one roll.
- An open frame is worth the total pins knocked down in that frame.
- The 10th frame supports valid bonus rolls for strikes and spares.

## Validation

The scorer raises a `ValueError` for invalid games, including:

- Spare as the first roll of a frame
- Invalid symbols
- Frame pin count greater than 10 without a spare
- Invalid 10th-frame bonus rolls
- Extra rolls after a completed game
- Incomplete games

## How to Run Tests

Install pytest if needed:

```bash
pip install pytest
```

Run tests:

```bash
pytest
```

## Example Usage

```python
from bowling import score_game

rolls = ["8", "/", "5", "4", "9", "0", "X", "X", "5", "/", "5", "3", "6", "3", "9", "/", "9", "/", "X"]

print(score_game(rolls))
```
