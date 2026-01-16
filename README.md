# Raycasting Engine with Simultaneous Map View

This project is a simple raycasting engine implemented from scratch in Python using Pygame.
It visualizes both the 2D map and the raycasting process in real time, allowing the internal
mechanics of the rendering technique to be observed alongside the final projected view.

The left side of the screen displays an 8x8 grid-based map along with the casted rays,
while the right side shows the corresponding pseudo-3D projection generated from those rays.

## Key Features
- Custom raycasting implementation (grid-based intersection checks)
- Real-time rendering of rays and projected walls
- Fish-eye correction and distance-based projection
- Manual movement and rotation system
- Clear separation between map logic, player logic and rendering

## How to Run

```
python3 raycasting.py
```

## Controls
- W / S : Move forward / backward
- A / D : Rotate left / right

## Notes
This project was built to understand the low-level mechanics behind classic 3D rendering
techniques used in early game engines, with a focus on geometry, trigonometry and real-time
rendering logic rather than gameplay.
