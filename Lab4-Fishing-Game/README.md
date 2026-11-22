# Lab 4: Fishing Game (Vibe Coding & Automated Testing)

**Student Name:** Neel Chandrakar  
**SRN:** `PES2UG24CS310`  
**Section:** Section F  
**Course:** Software Engineering Laboratory (UE24CS351A)  

---

## Overview

This project implements an interactive 2D single-topic Fishing-lite game built with **Pygame** alongside comprehensive unit tests and automated end-to-end (E2E) gameplay verification.

The lab exercises interactive pair programming, bug identification, feature expansion, and test automation.

---

## Tasks Completed & Features Implemented

1. **Bug Remediation (Catch Detection):**
   * *Problem:* The baseline implementation in `game/catch.py` only checked whether the hook's depth matched the fish's depth within a 10-pixel vertical tolerance, ignoring horizontal distance entirely.
   * *Fix:* Implemented 2D bounding box collision detection ensuring catches only occur when the hook and fish genuinely overlap in both `x` and `y` coordinates.

2. **Multiple Fish Varieties & Scored Species:**
   * Introduced multiple visually and behaviorally distinct fish species (e.g. Common Fish, Fast/Golden Trout, Deep Sea variants).
   * Differentiated by swimming speed, swimming depth, sprite dimensions, color palette, and awarded score point values.

3. **Player-Controlled Casting:**
   * Transitioned the casting mechanic from continuous automatic loops to player-controlled keyboard inputs (`SPACE` key).
   * Added state machine guards (`IDLE` → `CASTING` → `RETRACTING` → `IDLE`) preventing active cast interruptions.

4. **30-Second Round Countdown Timer & Game Over State:**
   * Integrated a 30-second countdown timer rendered cleanly on the HUD.
   * Freezes casting mechanics and halts active catches once the timer reaches zero.
   * Displays final game-over score with support for round restarts (`R` key).

---

## Directory Structure

```
Lab4-Fishing-Game/
├── game/
│   ├── catch.py                 # 2D collision & catch detection logic
│   ├── fish.py                  # Fish species models, velocities & wrapping
│   ├── game_engine.py           # Core game state loop, timer & score handling
│   ├── hook.py                  # Hook kinematics, states & casting
│   └── renderer.py              # Pygame display rendering & HUD graphics
├── tests/
│   ├── conftest.py              # Pytest headless display fixtures
│   ├── test_catch.py            # Unit tests for collision detection
│   ├── test_e2e.py              # E2E headless player session tests
│   ├── test_fish.py             # Unit tests for fish kinematics
│   ├── test_game_engine.py      # Unit tests for game round & timer logic
│   └── test_hook.py             # Unit tests for hook states & casting
├── e2e_screenshots/             # PNG captures of automated E2E lifecycle milestones
├── videos/
│   ├── gameplay_before_bug.mp4  # 10s recording showing original catch detection bug
│   └── gameplay_after_fixed.mp4 # 10s recording showing bug fix and new gameplay features
├── e2e_game_test.py             # Standalone E2E game runner
├── main.py                      # Main game entry point
├── pytest.ini                   # Pytest configuration
├── record_gameplay_videos.py    # Headless 60 FPS gameplay video generator
├── requirements.txt             # Project dependencies
└── README.md
```

---

## Execution & Testing

### 1. Run the Game
```bash
python main.py
```
* **Controls:**
  * `SPACE`: Cast fishing hook
  * `R`: Restart round after Game Over

### 2. Run Test Suite
```bash
pytest tests/ -v
```

### 3. Run Automated E2E Session
```bash
python e2e_game_test.py
```

### 4. Regenerate Gameplay Recordings
```bash
python record_gameplay_videos.py
```
