<div align="center">

# ✋ Gesture Control

### Control your entire Windows PC with hand gestures — no API key, no internet, 100% offline and free.

<p>
  <a href="https://github.com/engrmaziz/gesture-control/stargazers">
    <img src="https://img.shields.io/github/stars/engrmaziz/gesture-control?style=for-the-badge&logo=starship&color=f4d03f&labelColor=1a1a2e" alt="Stars"/>
  </a>
  <a href="https://github.com/engrmaziz/gesture-control/network/members">
    <img src="https://img.shields.io/github/forks/engrmaziz/gesture-control?style=for-the-badge&logo=git&color=48cae4&labelColor=1a1a2e" alt="Forks"/>
  </a>
  <a href="https://github.com/engrmaziz/gesture-control/issues">
    <img src="https://img.shields.io/github/issues/engrmaziz/gesture-control?style=for-the-badge&logo=github&color=e74c3c&labelColor=1a1a2e" alt="Issues"/>
  </a>
  <a href="https://github.com/engrmaziz/gesture-control/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/engrmaziz/gesture-control?style=for-the-badge&color=2ecc71&labelColor=1a1a2e" alt="License"/>
  </a>
  <a href="https://github.com/engrmaziz/gesture-control/commits">
    <img src="https://img.shields.io/github/last-commit/engrmaziz/gesture-control?style=for-the-badge&logo=github&color=9b59b6&labelColor=1a1a2e" alt="Last Commit"/>
  </a>
  <a href="https://github.com/engrmaziz/gesture-control">
    <img src="https://img.shields.io/github/repo-size/engrmaziz/gesture-control?style=for-the-badge&logo=files&color=e67e22&labelColor=1a1a2e" alt="Repo Size"/>
  </a>
  <a href="https://github.com/engrmaziz/gesture-control/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/engrmaziz/gesture-control?style=for-the-badge&logo=github&color=1abc9c&labelColor=1a1a2e" alt="Contributors"/>
  </a>
</p>

</div>

---

## 🚀 About The Project

**Gesture Control** transforms your ordinary webcam into a touchless, hands-free input device. Powered by Google's MediaPipe neural network — running entirely on your local CPU — it detects 21 hand landmarks in real time and maps natural hand shapes and motions to system-level actions: moving the mouse, clicking, adjusting volume, switching windows, and more.

**The problem it solves:**  
Traditional input devices create friction. Gesture Control removes the physical barrier between you and your computer. Whether you're presenting, cooking, exercising, or simply exploring the frontier of Human-Computer Interaction, you can control your PC without touching anything.

**Who is it for?**
- 🧑‍💻 Developers and makers exploring computer vision and HCI
- ♿ Users who benefit from accessibility-friendly, touch-free PC control
- 🎓 Students learning real-time AI/CV application development
- 🖥️ Presenters who want hands-free slide and window management

> **$0 · No API key · No internet · Runs 100% on your machine.**

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖱️ **Smooth Mouse Control** | Move the cursor naturally using only your index finger — exponential smoothing eliminates jitter |
| 🤏 **Left Click** | Pinch your thumb and index finger together to click |
| ✌️ **Right Click** | Peace-sign (index + middle) triggers a right-click |
| 🔊 **Real-Time Volume Control** | Raise or lower your open hand to set system volume — hand height maps directly to volume level |
| 🔄 **Window Switching** | Swipe your open hand left or right to cycle through windows with Alt+Tab / Alt+Shift+Tab |
| 🖥️ **Show Desktop** | Three-finger gesture instantly triggers Win+D |
| 📋 **Task View** | Index + Pinky (rock sign) opens Win+Tab Task View |
| ⏸️ **Pause / Resume** | Hold a fist for 1.5 seconds to freeze all gesture controls — hold again to resume |
| 🎨 **Live HUD Overlay** | Semi-transparent heads-up display with active gesture badge, FPS counter, volume bar, and fading action log |
| ⚡ **Zero-Latency Design** | `pyautogui.PAUSE = 0` + frame-level gesture dispatch — actions fire within the same frame cycle |
| 📴 **Fully Offline** | No API keys, no cloud endpoints, no telemetry — all inference runs locally on CPU |
| 🚀 **One-Click Launcher** | `START.bat` installs all dependencies and launches the app automatically |

---

## 🧠 How It Works

The system runs a tight 4-stage pipeline on every captured webcam frame:

```
┌──────────────────────────────────────────────────────────────────┐
│                        PIPELINE OVERVIEW                         │
└──────────────────────────────────────────────────────────────────┘

  [Webcam]  960×540 @ 30 fps
      │
      ▼
┌─────────────────────────────────┐
│  1. CAPTURE  (OpenCV)           │
│  cv2.VideoCapture → flip frame  │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  2. DETECT  (cvzone + MediaPipe)│
│  HandDetector.findHands()       │
│  → 21 landmarks (x, y, z) each  │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  3. CLASSIFY  (get_gesture)     │
│  fingersUp() + pinch distance   │
│  → POINT / PINCH / PEACE /      │
│    OPEN / THREE / ROCK / FIST   │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  4. ACT  (action_*)             │
│  PyAutoGUI → mouse / shortcuts  │
│  keyboard  → volume keys        │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│  5. DISPLAY  (draw_hud)         │
│  OpenCV overlay → cv2.imshow    │
└─────────────────────────────────┘
```

1. **Capture** — OpenCV reads webcam frames at 960×540 @ 30 fps and flips them horizontally for a mirror-like experience.
2. **Detect** — cvzone's `HandDetector` (backed by MediaPipe BlazePalm + Hand Landmark models) extracts 21 3D landmarks for up to one hand per frame.
3. **Classify** — `fingersUp()` returns a binary array of which fingers are extended. Combined with the Euclidean pinch distance between thumb tip (lm[4]) and index tip (lm[8]), a named gesture label is assigned.
4. **Act** — The label is dispatched to a dedicated action function. Cooldown timers prevent accidental double-firing. Mouse movement uses exponential smoothing to eliminate jitter.
5. **Display** — OpenCV draws a semi-transparent dark HUD strip, gesture badge, volume bar, swipe notification, fist-hold progress ring, and a fading action log onto each frame before displaying it.

---

## 🏗 Architecture

```
User's Hand
     │
     │  (webcam video)
     ▼
OpenCV (cv2.VideoCapture)
     │
     │  raw BGR frames
     ▼
cvzone HandDetector ──── MediaPipe BlazePalm + Landmark Model
     │
     │  lmList[21][x,y,z]  +  fingersUp[5]
     ▼
Gesture Classifier (get_gesture)
     │
     │  gesture label: POINT / PINCH / PEACE / OPEN / THREE / ROCK / FIST
     ▼
Action Dispatcher
     ├── action_mouse()    ──→  PyAutoGUI.moveTo()
     ├── action_click()    ──→  PyAutoGUI.click()
     ├── action_rclick()   ──→  PyAutoGUI.rightClick()
     ├── action_volume()   ──→  keyboard.send("volume up/down")
     ├── action_swipe()    ──→  PyAutoGUI.hotkey("alt","tab")
     ├── action_win_d()    ──→  PyAutoGUI.hotkey("win","d")
     ├── action_win_tab()  ──→  PyAutoGUI.hotkey("win","tab")
     └── action_fist()     ──→  Toggle paused state
     │
     ▼
draw_hud (OpenCV overlay)
     │
     ▼
cv2.imshow  →  Screen
```

---

## 🛠 Tech Stack

<div align="center">

**Language**

![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)

**AI / Computer Vision**

![MediaPipe](https://img.shields.io/badge/MediaPipe_0.10.14-0F9D58?style=for-the-badge&logo=google&logoColor=white)
![cvzone](https://img.shields.io/badge/cvzone-latest-00B4D8?style=for-the-badge)
![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)

**System Control**

![PyAutoGUI](https://img.shields.io/badge/PyAutoGUI-FF6B6B?style=for-the-badge&logo=python&logoColor=white)
![keyboard](https://img.shields.io/badge/keyboard-4ECDC4?style=for-the-badge&logo=python&logoColor=white)

**Numerical Computing**

![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)

**Platform**

![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

</div>

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11 | Core runtime |
| **Hand Tracking** | [cvzone](https://github.com/cvzone/cvzone) + [MediaPipe](https://mediapipe.dev/) `0.10.14` | 21-landmark hand detection |
| **Computer Vision** | [OpenCV](https://opencv.org/) | Webcam capture, frame processing, HUD rendering |
| **Mouse / Keyboard** | [PyAutoGUI](https://pyautogui.readthedocs.io/) | Mouse movement, clicks, system shortcuts |
| **Volume Keys** | [keyboard](https://github.com/boppreh/keyboard) | Low-level volume key simulation |
| **Math / Arrays** | [NumPy](https://numpy.org/) | Coordinate interpolation, clipping |
| **Platform** | Windows 10/11 | OS target (uses Win32 keyboard/volume APIs) |

---

## 📂 Project Structure

```
gesture-control/
│
├── gesture_control.py   ← Single-file application — all logic lives here
├── requirements.txt     ← Python package dependencies (pip-installable)
├── START.bat            ← One-click Windows launcher (auto-installs deps)
├── ins.txt              ← Quick manual install reference
└── README.md            ← Documentation
```

`gesture_control.py` is organized into clearly commented sections:

| Section | Contents |
|---|---|
| **Config** | `CAM_W/H`, `SMOOTH`, `PINCH_PX`, `SWIPE_VEL`, `CLICK_CD`, `FIST_HOLD`, `VOL_TOP/BOT`, `MARGIN` |
| **Colors** | BGR color constants for the HUD (`CYAN`, `GREEN`, `RED`, `YELLOW`, `PINK`, `DIM`, `WHITE`, `DARK`) |
| **State** | Global variables tracking pause state, smooth cursor position, cooldown timers, volume level |
| **Helpers** | `dist()` — Euclidean distance; `push_log()` — action log; `get_gesture()` — gesture classifier |
| **Actions** | `action_mouse`, `action_click`, `action_rclick`, `action_volume`, `action_swipe`, `action_win_d`, `action_win_tab`, `action_fist` |
| **HUD** | `draw_hud()` — full overlay renderer (gesture badge, FPS, volume bar, swipe label, fist progress, action log, cheat sheet) |
| **Main loop** | Camera init, frame capture loop, hand detection, gesture dispatch, display |

---

## ⚙️ Installation

### Prerequisites

| Requirement | Details |
|---|---|
| **OS** | Windows 10 or Windows 11 |
| **Python** | 3.11.x — MediaPipe `0.10.14` does **not** support Python 3.12+ |
| **Webcam** | Any standard USB or built-in webcam |

---

### Option A — One-Click Launcher *(Recommended)*

1. Install **Python 3.11** from [python.org](https://www.python.org/downloads/release/python-3119/)
   > ⚠️ During setup, check **"Add Python to PATH"**

2. Double-click **`START.bat`**

`START.bat` automatically:
- ✅ Verifies Python 3.11 is available
- 📦 Installs all dependencies on first run (~2 minutes)
- 🚀 Launches the application

---

### Option B — Manual Install

```bash
# 1. Clone the repository
git clone https://github.com/engrmaziz/gesture-control.git
cd gesture-control

# 2. Install dependencies using Python 3.11
py -3.11 -m pip install cvzone mediapipe==0.10.14 opencv-python pyautogui numpy keyboard

# 3. Run
py -3.11 gesture_control.py
```

---

### Option C — requirements.txt

> **Note:** `cvzone` is installed explicitly before `-r requirements.txt` because it is not listed in `requirements.txt`. The command below handles both in one step.

```bash
py -3.11 -m pip install cvzone -r requirements.txt
py -3.11 gesture_control.py
```

---

## 🎮 Gesture Reference

| Gesture | Hand Shape | Action | Trigger |
|---|---|---|---|
| ☝️ **POINT** | Index finger only | Move mouse cursor | Continuous |
| 🤏 **PINCH** | Pinch thumb + index | Left click | Cooldown: 0.45s |
| ✌️ **PEACE** | Index + Middle fingers | Right click | Cooldown: 0.45s |
| 🖐️ **OPEN** | All fingers extended | Volume control (height = level) | Continuous |
| 👋 **SWIPE** | Open hand, horizontal motion | Alt+Tab / Alt+Shift+Tab | Cooldown: 1.0s |
| 🤟 **THREE** | Index + Middle + Ring | Win+D (show/hide desktop) | On gesture change |
| 🤘 **ROCK** | Index + Pinky | Win+Tab (Task View) | On gesture change |
| ✊ **FIST** | All fingers closed, hold 1.5s | Pause / Resume all controls | Hold 1.5s |

---

## 🔧 Configuration

All tunable constants are at the top of `gesture_control.py` — no config files needed:

| Variable | Default | Description |
|---|---|---|
| `CAM_W`, `CAM_H` | `960`, `540` | Camera capture resolution |
| `SMOOTH` | `5` | Mouse smoothing factor — higher = smoother but slightly more latency |
| `PINCH_PX` | `45` | Pixel distance threshold between thumb and index tip to trigger a click |
| `SWIPE_VEL` | `0.025` | Minimum normalized wrist velocity to trigger Alt+Tab |
| `SWIPE_CD` | `1.0` | Seconds between consecutive swipe actions |
| `CLICK_CD` | `0.45` | Seconds between consecutive click actions |
| `FIST_HOLD` | `1.5` | Seconds to hold a fist before toggling pause |
| `VOL_TOP` | `0.15` | Normalized Y position (top of frame) = 100% volume |
| `VOL_BOT` | `0.85` | Normalized Y position (bottom of frame) = 0% volume |
| `MARGIN` | `100` | Pixel margin for mapping hand position to screen edges |

---

## 💡 Tips for Best Results

- 💡 **Good lighting** dramatically improves landmark detection accuracy
- 📏 Position your hand **30–60 cm** from the camera
- 🎨 A **plain or neutral background** helps MediaPipe track reliably
- 🖱️ If the mouse feels jittery, increase `SMOOTH` from `5` → `8` or `10`
- 🖱️ If clicks fire too fast, increase `CLICK_CD` (e.g., `0.6`)
- ⏸️ Hold a **FIST** for 1.5 seconds any time to pause/resume all controls
- ❌ Press **Q** in the camera window to quit the application

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| [`cvzone`](https://github.com/cvzone/cvzone) | latest | High-level MediaPipe hand tracking wrapper |
| [`mediapipe`](https://mediapipe.dev/) | `0.10.14` | Google's BlazePalm + Hand Landmark model |
| [`opencv-python`](https://opencv.org/) | latest | Webcam capture, image processing, HUD rendering |
| [`pyautogui`](https://pyautogui.readthedocs.io/) | latest | Mouse movement, clicks, and keyboard shortcuts |
| [`keyboard`](https://github.com/boppreh/keyboard) | latest | System-level volume key simulation |
| [`numpy`](https://numpy.org/) | latest | Coordinate interpolation, normalization, clipping |

> All packages are free, open source, and run **100% offline** — no data ever leaves your machine.

---

## ⚡ Quick Start (TL;DR)

```bash
# 1. Install Python 3.11 from https://python.org
# 2. Clone and install
git clone https://github.com/engrmaziz/gesture-control.git
cd gesture-control
py -3.11 -m pip install cvzone mediapipe==0.10.14 opencv-python pyautogui numpy keyboard
# 3. Run
py -3.11 gesture_control.py
```

Point your hand at the webcam and start gesturing. Press **Q** to quit.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-gesture`)
3. Commit your changes (`git commit -m 'Add amazing gesture'`)
4. Push to the branch (`git push origin feature/amazing-gesture`)
5. Open a Pull Request

---

<div align="center">

**Built with** cvzone · MediaPipe · OpenCV · PyAutoGUI · keyboard · $0

⭐ Star this repo if you found it useful!

</div>
