# ✋ GESTURE CONTROL — Windows Edition
**Control your entire PC with hand gestures. $0. No API key. Runs offline.**

---

## 🎮 All 8 Gestures

| Gesture | Hand Shape | Action |
|---|---|---|
| ☝️ **MOUSE** | Index finger only | Moves cursor smoothly |
| 🤏 **CLICK** | Pinch thumb + index | Left click |
| ✌️ **R-CLICK** | Index + Middle | Right click |
| 🖐️ **VOLUME** | Full open hand | Hand height = volume level |
| 👈👉 **SWIPE** | Open hand, move left/right | Alt+Tab (switch windows) |
| 🤟 **WIN+D** | Index + Middle + Ring | Show/hide desktop |
| 🤘 **WIN+TAB**| Index + Pinky | Task View |
| ✊ **PAUSE** | Fist (hold 1.2s) | Pause / Resume all controls |

---

## ⚡ Setup (3 steps)

### Step 1 — Install Python
Download from **https://python.org/downloads**
> ⚠️ During install, check **"Add Python to PATH"**

### Step 2 — Install & Run
Just double-click **`START.bat`**

It will:
- Install all dependencies automatically (first time only, ~2 min)
- Launch the app

### Step 3 — Use it!
A window opens showing your webcam feed with a HUD overlay.
Show your hand to the camera and start gesturing.

---

## 🛠️ Manual install (if START.bat fails)

Open Command Prompt in this folder:
```
pip install -r requirements.txt
python gesture_control.py
```

---

## 📁 Project Structure
```
gesture-control/
├── gesture_control.py   ← Main app (all logic here)
├── requirements.txt     ← Python dependencies
├── START.bat            ← Double-click to run on Windows
└── README.md            ← This file
```

---

## 🔧 Tweaking (inside gesture_control.py)

| Config var | What it does | Default |
|---|---|---|
| `SMOOTH_FACTOR` | Mouse smoothness (higher = smoother but slower) | `6` |
| `PINCH_DIST` | How close thumb+index must be to click | `0.055` |
| `SWIPE_VEL` | How fast to swipe for Alt+Tab | `0.022` |
| `SWIPE_COOLDOWN` | Seconds between swipes | `0.9` |

---

## 💡 Tips
- **Good lighting** makes detection more accurate
- Keep your hand **30–60 cm** from the camera
- **Neutral background** helps MediaPipe track better
- If mouse feels jittery, increase `SMOOTH_FACTOR` to `8` or `10`

---

## 📦 Dependencies
| Package | Purpose |
|---|---|
| `mediapipe` | Hand landmark detection (Google) |
| `opencv-python` | Webcam capture + HUD drawing |
| `pyautogui` | Control mouse & keyboard |
| `pycaw` | Windows audio volume control |
| `numpy` | Coordinate math |

All free, all open source, all offline.

---

**Built with:** MediaPipe · OpenCV · PyAutoGUI · pycaw · $0
