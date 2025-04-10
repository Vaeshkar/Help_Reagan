![version](https://img.shields.io/badge/version-1.4-blue.svg)

# Help Reagan – A Pygame Platformer

**Help Reagan** is a retro-style 2D platformer built for macOS using Python and Pygame. The goal: help Reagan survive as waves of students try to overrun him!

## 🎮 Features
- Pixel art world inspired by Mario
- Jump, run, and dodge animated students
- Reagan says quirky educational quotes when he jumps
- Background music, sound effects, and speech bubbles
- Game over animation and restart system
- Fully packaged macOS `.app` version

## 📦 macOS App Version
- Open `Help Reagan.app` by **double-clicking** the app.
- On first launch, go to your system settings and scroll down to 'Privacy & Security'
- Scroll down in the window towards 'Security' and there you see the Help Reagan.app.
- Press on the button: 'Open Anyway'
- You are prompted with a password/fingerprint auth to accept you are not opening a real Apple.app
- No Python installation required – it's all bundled!

## 📁 Folder Structure
```
help_reagan_game/
├── assets/              # Images, sprites, backgrounds
├── sounds/              # Sound effects and music
├── help_reagan.py       # Main game script
├── help_reagan.spec     # PyInstaller config
├── Help Reagan.app/     # macOS standalone app
├── setup.py             # (for py2app, optional)
└── requirements.txt
```

## 🧙 Credits
Created by Konstantin, Dennis — with help from ChatGPT.
Approved by the Software Engineers SE#01_WBS Foundation
Authorized representative: Linus Climber Tech Tips
All artwork and sound assets were either original or generated using pixel art tools and free sound libraries.
© 2025, all rights reserved

## 📝 Changelog

### v1.4 – Stable Release
- Polished Reagan jump animations
- Background music and sound effects implemented
- Fully bundled macOS `.app` with icon
- Added end screen and restart system
- Speech bubbles for Reagan’s iconic lines

### v1.3
- Added new sprite sheet for Reagan's 6-frame run animation
- Introduced speech bubble system with educational quotes
- Refined jump and run mechanics
- Implemented game-over screen with restart functionality
- Added 26 more questions with a game loop timeout, timeout set to 1,5s

### v1.2
- Background and foreground pixel art updated and optimized
- Foreground movement fixed and resized for game window
- Students (cactus equivalents) animated and randomized
- Added in-game score display and start screen instructions

### v1.1
- Replaced placeholder graphics with themed Reagan and student sprites
- Implemented animated speech bubbles on jump
- Added sound effects for jump, walk, and collision
- Added 4 test questions with a game loop timeout, timeout set to 1s

### v1.0
- Initial game logic and loop
- Basic collision and jumping
- Placeholder sprites and assets

---

Enjoy the game! 🕹️🎓
