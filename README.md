# ✋ Gesture Control — Windows Edition

> **Control your entire Windows PC with hand gestures — no API key, no internet, 100% offline and free.**

---

## 🚀 Overview

**Gesture Control** turns your ordinary webcam into a touchless input device. Using real-time hand landmark detection, it maps specific hand shapes and motions to system-level actions: moving the mouse, clicking, adjusting volume, switching windows, and more.

It runs entirely on your local machine — no cloud calls, no subscriptions, no setup beyond a one-time `pip install`. Just point your hand at the camera and start controlling your PC.

**Who is it for?**
- Developers and makers exploring computer vision
- Users who want accessibility-friendly, touch-free PC control
- Anyone curious about gesture-based HCI (Human-Computer Interaction)

---

## ✨ Features

- 🖱️ **Smooth mouse control** — move the cursor using just your index finger
- 🖱️ **Left & right click** — pinch or peace-sign gestures trigger clicks
- 🔊 **Volume control** — raise/lower your hand to adjust system volume in real time
- 🔄 **Window switching** — swipe your open hand left or right to Alt+Tab
- 🖥️ **Show desktop** — three-finger gesture triggers Win+D
- 📋 **Task View** — index + pinky gesture triggers Win+Tab
- ⏸️ **Pause / Resume** — hold a fist for 1.5 seconds to freeze or unfreeze all controls
- 🎨 **Live HUD overlay** — real-time heads-up display with gesture name, FPS, volume bar, and action log
- ⚡ **Zero latency design** — `pyautogui.PAUSE = 0`, frame-level gesture dispatch
- 📴 **Fully offline** — no API keys, no cloud, no data sent anywhere

---

## 🧠 How It Works

```
Webcam Frame
     │
     ▼
┌─────────────────────────────────┐
│  cvzone HandDetector            │
│  (MediaPipe under the hood)     │
│  → 21 hand landmarks (x, y, z)  │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Gesture Classifier             │
│  fingersUp() + pinch distance   │
│  → POINT / PINCH / PEACE /      │
│    OPEN / THREE / ROCK / FIST   │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  Action Dispatcher              │
│  → PyAutoGUI  (mouse/keyboard)  │
│  → keyboard   (volume keys)     │
└─────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────┐
│  HUD Renderer (OpenCV)          │
│  → Gesture badge, FPS, vol bar  │
│  → On-screen action log         │
└─────────────────────────────────┘
```

1. **Capture** — OpenCV reads webcam frames at 960×540 @ 30 fps.
2. **Detect** — cvzone's `HandDetector` (powered by MediaPipe) extracts 21 3D landmarks for one hand per frame.
3. **Classify** — `fingersUp()` returns which fingers are extended; combined with thumb-index pinch distance, a gesture label is assigned.
4. **Act** — The gesture label is dispatched to an action function that calls PyAutoGUI or the `keyboard` library to control the OS.
5. **Display** — OpenCV draws a semi-transparent HUD over the webcam feed showing the active gesture, FPS counter, volume bar, and a fading action log.

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.11 |
| **Hand Tracking** | [cvzone](https://github.com/cvzone/cvzone) + [MediaPipe](https://mediapipe.dev/) |
| **Computer Vision** | [OpenCV](https://opencv.org/) (`opencv-python`) |
| **Mouse / Keyboard** | [PyAutoGUI](https://pyautogui.readthedocs.io/) |
| **Volume Keys** | [keyboard](https://github.com/boppreh/keyboard) |
| **Math / Arrays** | [NumPy](https://numpy.org/) |
| **Platform** | Windows (tested) |

---

## 🎮 Gesture Reference

| Gesture | Hand Shape | Action |
|---|---|---|
| ☝️ **POINT** | Index finger only | Move mouse cursor |
| 🤏 **PINCH** | Pinch thumb + index | Left click |
| ✌️ **PEACE** | Index + Middle fingers | Right click |
| 🖐️ **OPEN** | All fingers extended | Volume (hand height = level) |
| 👈👉 **SWIPE** | Open hand, move horizontally | Alt+Tab / Alt+Shift+Tab |
| 🤟 **THREE** | Index + Middle + Ring | Win+D (show/hide desktop) |
| 🤘 **ROCK** | Index + Pinky | Win+Tab (Task View) |
| ✊ **FIST** | All fingers closed (hold 1.5s) | Pause / Resume all controls |

---

## 📂 Project Structure

```
gesture-control/
├── gesture_control.py   ← Main application — all detection, gesture, and HUD logic
├── requirements.txt     ← Python package dependencies
├── START.bat            ← One-click Windows launcher (installs deps on first run)
├── ins.txt              ← Quick manual install reference
└── README.md            ← This file
```

`gesture_control.py` is a single-file application organized into clear sections:

| Section | What it contains |
|---|---|
| **Config** | Camera resolution, smoothing, pinch threshold, cooldowns |
| **State** | Global variables for tracking gesture continuity |
| **Helpers** | `dist()` — Euclidean distance; `push_log()` — action log; `get_gesture()` — classifier |
| **Actions** | `action_mouse`, `action_click`, `action_rclick`, `action_volume`, `action_swipe`, `action_win_d`, `action_win_tab`, `action_fist` |
| **HUD** | `draw_hud()` — renders the full overlay onto each frame |
| **Main loop** | Camera init, frame capture, hand detection, gesture dispatch, display |

---

## ⚙️ Installation

### Requirements
- **Windows** (PyAutoGUI's `hotkey` and `keyboard` volume send are Windows-native)
- **Python 3.11** — MediaPipe 0.10.x does not support Python 3.12+
- **Webcam**

### Option A — One-click launcher (recommended)

1. Install **Python 3.11** from [python.org/downloads/release/python-3119](https://www.python.org/downloads/release/python-3119/)
   > ⚠️ During install, check **"Add Python to PATH"**
2. Double-click **`START.bat`**

`START.bat` will:
- Verify Python 3.11 is available
- Install all dependencies automatically (first time only, ~2 minutes)
- Launch the application

### Option B — Manual install

```bash
# Clone the repository
git clone https://github.com/engrmaziz/gesture-control.git
cd gesture-control

# Install dependencies with Python 3.11
py -3.11 -m pip install cvzone mediapipe==0.10.14 opencv-python pyautogui numpy keyboard

# Run
py -3.11 gesture_control.py
```

### Option C — pip with requirements file

> **Note:** `cvzone` is not included in `requirements.txt` and must be installed separately.

```bash
py -3.11 -m pip install cvzone -r requirements.txt
py -3.11 gesture_control.py
```

---

## 🔧 Configuration

All tuneable constants live at the top of `gesture_control.py`:

| Variable | Default | What it controls |
|---|---|---|
| `CAM_W`, `CAM_H` | `960`, `540` | Camera capture resolution |
| `SMOOTH` | `5` | Mouse smoothing factor — higher = smoother but slightly slower |
| `PINCH_PX` | `45` | Pixel distance between thumb and index tip to trigger a click |
| `SWIPE_VEL` | `0.025` | Minimum wrist velocity (normalized) to trigger Alt+Tab |
| `SWIPE_CD` | `1.0` | Seconds between consecutive swipe actions |
| `CLICK_CD` | `0.45` | Seconds between consecutive click actions |
| `FIST_HOLD` | `1.5` | Seconds to hold a fist before toggling pause |
| `VOL_TOP` | `0.15` | Normalized camera Y for maximum volume |
| `VOL_BOT` | `0.85` | Normalized camera Y for minimum volume |
| `MARGIN` | `100` | Pixel margin used to map hand position to screen edges |

---

## 💡 Tips for Best Results

- **Good lighting** dramatically improves hand detection accuracy
- Position your hand **30–60 cm** from the camera
- A **plain or neutral background** helps MediaPipe track landmarks more reliably
- If the mouse feels jittery, increase `SMOOTH` from `5` to `8` or `10`
- If clicks are triggering too fast, increase `CLICK_CD` (e.g., `0.6`)
- Press **Q** in the camera window to quit

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `cvzone` | latest | High-level hand tracking wrapper for MediaPipe |
| `mediapipe` | `0.10.14` | Google's hand landmark detection model |
| `opencv-python` | latest | Webcam capture and HUD rendering |
| `pyautogui` | latest | Mouse movement, clicks, and keyboard shortcuts |
| `keyboard` | latest | System-level volume key simulation |
| `numpy` | latest | Coordinate interpolation and math |

All packages are free, open source, and run 100% offline.

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Install Python 3.11 from python.org
# 2. Clone and install
git clone https://github.com/engrmaziz/gesture-control.git
cd gesture-control
py -3.11 -m pip install cvzone mediapipe==0.10.14 opencv-python pyautogui numpy keyboard
# 3. Run
py -3.11 gesture_control.py
```

Then show your hand to the webcam and start gesturing. Press **Q** to quit.

---

**Built with:** cvzone · MediaPipe · OpenCV · PyAutoGUI · keyboard · $0
