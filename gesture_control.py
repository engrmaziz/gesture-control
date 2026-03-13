"""
GESTURE CONTROL - Windows Edition
Mouse / Volume / Window Switcher / Shortcuts
$0 - No API - Runs 100% offline

GESTURES:
  Index finger only    -> Mouse cursor
  Pinch thumb+index    -> Left click
  Index + Middle       -> Right click
  Open hand            -> Volume (move hand up/down)
  Open hand + swipe    -> Alt+Tab
  3 fingers            -> Win+D (show desktop)
  Index + Pinky        -> Win+Tab (task view)
  Fist hold 1.5s       -> Pause / Resume
"""

import cv2
import pyautogui
import numpy as np
import time
import math
import sys
import keyboard
from cvzone.HandTrackingModule import HandDetector

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

# ── Config ─────────────────────────────────────────────────────────────────
CAM_W, CAM_H       = 960, 540
SCREEN_W, SCREEN_H = pyautogui.size()
SMOOTH             = 5
MARGIN             = 100
PINCH_PX           = 45
SWIPE_VEL          = 0.025
SWIPE_CD           = 1.0
VOL_TOP            = 0.15
VOL_BOT            = 0.85
CLICK_CD           = 0.45
FIST_HOLD          = 1.5

# ── Colors BGR ─────────────────────────────────────────────────────────────
CYAN   = (0, 245, 255)
GREEN  = (80, 250, 123)
RED    = (85, 85, 255)
YELLOW = (140, 250, 241)
PINK   = (198, 121, 255)
DIM    = (70, 80, 95)
WHITE  = (210, 210, 210)
DARK   = (12, 16, 22)

# ── State ──────────────────────────────────────────────────────────────────
paused        = False
smooth_x      = float(SCREEN_W // 2)
smooth_y      = float(SCREEN_H // 2)
last_click    = 0
last_rclick   = 0
last_swipe    = 0
swipe_label   = ""
swipe_label_t = 0
prev_wrist_x  = None
prev_palm_y   = None
vol_display   = 0.5
vol_cd        = 0
fist_start    = None
log_entries   = []
fps           = 0
fps_count     = 0
fps_t         = time.time()

# ── Helpers ────────────────────────────────────────────────────────────────
def dist(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def push_log(txt, col=WHITE):
    global log_entries
    log_entries.insert(0, (txt, time.time(), col))
    log_entries = log_entries[:6]

def get_gesture(fingers, lm):
    _, idx, mid, ring, pink = fingers
    pd = dist(lm[4][:2], lm[8][:2])
    if pd < PINCH_PX:
        return "PINCH"
    if idx==0 and mid==0 and ring==0 and pink==0:
        return "FIST"
    if idx==1 and mid==1 and ring==1 and pink==1:
        return "OPEN"
    if idx==1 and mid==0 and ring==0 and pink==1:
        return "ROCK"
    if idx==1 and mid==1 and ring==1 and pink==0:
        return "THREE"
    if idx==1 and mid==1 and ring==0 and pink==0:
        return "PEACE"
    if idx==1 and mid==0 and ring==0 and pink==0:
        return "POINT"
    return "NONE"

# ── Actions ────────────────────────────────────────────────────────────────
def action_mouse(lm):
    global smooth_x, smooth_y
    raw_x = lm[8][0]
    raw_y = lm[8][1]
    mx = np.interp(raw_x, [MARGIN, CAM_W-MARGIN], [0, SCREEN_W])
    my = np.interp(raw_y, [MARGIN, CAM_H-MARGIN], [0, SCREEN_H])
    smooth_x += (mx - smooth_x) / SMOOTH
    smooth_y += (my - smooth_y) / SMOOTH
    sx = int(np.clip(smooth_x, 0, SCREEN_W-1))
    sy = int(np.clip(smooth_y, 0, SCREEN_H-1))
    pyautogui.moveTo(sx, sy, _pause=False)

def action_click():
    global last_click
    now = time.time()
    if now - last_click > CLICK_CD:
        pyautogui.click(_pause=False)
        last_click = now
        push_log("LEFT CLICK", GREEN)

def action_rclick():
    global last_rclick
    now = time.time()
    if now - last_rclick > CLICK_CD:
        pyautogui.rightClick(_pause=False)
        last_rclick = now
        push_log("RIGHT CLICK", YELLOW)

def action_volume(lm):
    global prev_palm_y, vol_display, vol_cd
    palm_y = lm[0][1] / CAM_H
    vol_display = float(np.clip(1.0 - np.interp(palm_y, [VOL_TOP, VOL_BOT], [0.0, 1.0]), 0.0, 1.0))
    now = time.time()
    if prev_palm_y is None:
        prev_palm_y = palm_y
        return
    delta = prev_palm_y - palm_y
    prev_palm_y = palm_y
    if now - vol_cd < 0.07:
        return
    steps = min(int(abs(delta) / 0.015), 3)
    if steps > 0:
        if delta > 0:
            for _ in range(steps): keyboard.send("volume up")
            push_log(f"VOL UP x{steps}", PINK)
        else:
            for _ in range(steps): keyboard.send("volume down")
            push_log(f"VOL DOWN x{steps}", PINK)
        vol_cd = now

def action_swipe(lm):
    global prev_wrist_x, last_swipe, swipe_label, swipe_label_t
    wx = lm[0][0] / CAM_W
    now = time.time()
    if prev_wrist_x is not None and now - last_swipe > SWIPE_CD:
        vel = prev_wrist_x - wx
        if vel > SWIPE_VEL:
            pyautogui.hotkey("alt", "tab", _pause=False)
            last_swipe = now; swipe_label = ">>> ALT+TAB"; swipe_label_t = now
            push_log("SWIPE ALT+TAB", PINK)
        elif vel < -SWIPE_VEL:
            pyautogui.hotkey("alt", "shift", "tab", _pause=False)
            last_swipe = now; swipe_label = "ALT+SHIFT+TAB <<<"; swipe_label_t = now
            push_log("SWIPE ALT+SHIFT+TAB", PINK)
    prev_wrist_x = wx

def action_win_d(gesture, pg):
    if gesture != pg:
        pyautogui.hotkey("win", "d", _pause=False)
        push_log("WIN + D  (DESKTOP)", CYAN)

def action_win_tab(gesture, pg):
    if gesture != pg:
        pyautogui.hotkey("win", "tab", _pause=False)
        push_log("WIN + TAB  (TASKS)", CYAN)

def action_fist(lm):
    global fist_start, paused
    now = time.time()
    if fist_start is None:
        fist_start = now
    elif now - fist_start >= FIST_HOLD:
        paused = not paused
        fist_start = None
        push_log("PAUSED" if paused else "RESUMED", RED if paused else GREEN)

# ── HUD ────────────────────────────────────────────────────────────────────
def draw_hud(frame, gesture):
    global fps, fps_count, fps_t
    h, w = frame.shape[:2]
    now = time.time()

    fps_count += 1
    if now - fps_t >= 1.0:
        fps = fps_count; fps_count = 0; fps_t = now

    if paused:
        ov = frame.copy()
        cv2.rectangle(ov, (0,0), (w,h), (0,0,0), -1)
        cv2.addWeighted(ov, 0.5, frame, 0.5, 0, frame)
        cv2.putText(frame, "PAUSED - HOLD FIST TO RESUME",
                    (w//2-220, h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.9, RED, 2)
        return

    ov = frame.copy()
    cv2.rectangle(ov, (0,0), (w,50), DARK, -1)
    cv2.addWeighted(ov, 0.75, frame, 0.25, 0, frame)

    cv2.putText(frame, "GESTURE CONTROL", (14,34), cv2.FONT_HERSHEY_SIMPLEX, 0.75, CYAN, 2)
    cv2.putText(frame, f"FPS {fps}", (w-100,34), cv2.FONT_HERSHEY_SIMPLEX, 0.5, DIM, 1)

    colors = {"POINT":CYAN,"PINCH":GREEN,"PEACE":YELLOW,
              "OPEN":PINK,"THREE":CYAN,"ROCK":CYAN,"FIST":RED,"NONE":DIM}
    labels = {"POINT":"MOUSE","PINCH":"CLICK","PEACE":"R-CLICK",
              "OPEN":"VOLUME","THREE":"WIN+D","ROCK":"WIN+TAB","FIST":"PAUSE","NONE":"---"}
    mc = colors.get(gesture, DIM)
    ml = labels.get(gesture, "---")
    bx = w//2-65
    ov2 = frame.copy()
    cv2.rectangle(ov2, (bx,8), (bx+130,44), mc, -1)
    cv2.addWeighted(ov2, 0.15, frame, 0.85, 0, frame)
    cv2.rectangle(frame, (bx,8), (bx+130,44), mc, 1)
    cv2.putText(frame, ml, (bx+14,32), cv2.FONT_HERSHEY_SIMPLEX, 0.7, mc, 2)

    vbx = w-22; vby1 = 60; vby2 = h-60; bh = vby2-vby1
    fy = int(vby2 - vol_display*bh)
    cv2.rectangle(frame, (vbx-8,vby1), (vbx,vby2), DIM, 1)
    cv2.rectangle(frame, (vbx-8,fy), (vbx,vby2), PINK, -1)
    cv2.putText(frame, f"{int(vol_display*100)}%", (vbx-32,fy-5), cv2.FONT_HERSHEY_SIMPLEX, 0.38, PINK, 1)
    cv2.putText(frame, "VOL", (vbx-20,vby2+16), cv2.FONT_HERSHEY_SIMPLEX, 0.35, DIM, 1)

    if gesture == "OPEN":
        cv2.line(frame, (0,int(VOL_TOP*h)), (w-30,int(VOL_TOP*h)), PINK, 1)
        cv2.line(frame, (0,int(VOL_BOT*h)), (w-30,int(VOL_BOT*h)), PINK, 1)
        cv2.putText(frame, "MAX", (6,int(VOL_TOP*h)-4), cv2.FONT_HERSHEY_SIMPLEX, 0.38, PINK, 1)
        cv2.putText(frame, "MIN", (6,int(VOL_BOT*h)+14), cv2.FONT_HERSHEY_SIMPLEX, 0.38, PINK, 1)

    if swipe_label and now - swipe_label_t < 0.8:
        cv2.putText(frame, swipe_label, (w//2-100,h-28), cv2.FONT_HERSHEY_SIMPLEX, 1.0, PINK, 2)

    if gesture == "FIST" and fist_start:
        prog = min((now-fist_start)/FIST_HOLD, 1.0)
        cv2.ellipse(frame, (w//2,h//2), (52,52), -90, 0, int(prog*360), RED, 3)
        cv2.putText(frame, "HOLD TO PAUSE", (w//2-82,h//2+72), cv2.FONT_HERSHEY_SIMPLEX, 0.52, RED, 1)

    for i,(txt,ts,col) in enumerate(log_entries):
        age = now - ts
        if age > 3.0: continue
        fc = tuple(int(c*max(0.0,1.0-age/3.0)) for c in col)
        cv2.putText(frame, f"> {txt}", (12,h-10-i*22), cv2.FONT_HERSHEY_SIMPLEX, 0.48, fc, 1)

    sheet = [("POINT","Mouse"),("PINCH","Click"),("PEACE","R-Click"),
             ("OPEN","Volume"),("THREE","Win+D"),("ROCK","Win+Tab"),
             ("SWIPE","Alt+Tab"),("FIST","Pause")]
    for i,(g,a) in enumerate(sheet):
        y = 68+i*22
        cv2.putText(frame, g, (14,y), cv2.FONT_HERSHEY_SIMPLEX, 0.36, DIM, 1)
        cv2.putText(frame, a, (110,y), cv2.FONT_HERSHEY_SIMPLEX, 0.36, WHITE, 1)

# ── Main ───────────────────────────────────────────────────────────────────
def main():
    global paused, fist_start, prev_wrist_x, prev_palm_y

    print("\n" + "="*50)
    print("   GESTURE CONTROL  -  Windows Edition")
    print("="*50)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  CAM_W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)
    cap.set(cv2.CAP_PROP_FPS, 30)

    if not cap.isOpened():
        print("ERROR: Cannot open webcam.")
        sys.exit(1)

    detector = HandDetector(detectionCon=0.75, maxHands=1)

    print("  Camera ready")
    print(f"  Screen: {SCREEN_W} x {SCREEN_H}")
    print("  Press Q to quit")
    print("="*50 + "\n")

    prev_gesture = ""

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        hands, frame = detector.findHands(frame, draw=True, flipType=False)

        gesture = "NONE"

        if hands:
            hand    = hands[0]
            lm      = hand["lmList"]
            fingers = detector.fingersUp(hand)
            gesture = get_gesture(fingers, lm)

            if not paused:
                if gesture == "POINT":
                    action_mouse(lm)
                elif gesture == "PINCH":
                    action_mouse(lm)
                    action_click()
                elif gesture == "PEACE":
                    action_rclick()
                elif gesture == "OPEN":
                    action_volume(lm)
                    action_swipe(lm)
                elif gesture == "THREE":
                    action_win_d(gesture, prev_gesture)
                elif gesture == "ROCK":
                    action_win_tab(gesture, prev_gesture)
                elif gesture == "FIST":
                    action_fist(lm)
                    action_swipe(lm)

                if gesture != "FIST":    fist_start = None
                if gesture != "OPEN":    prev_palm_y = None
                if gesture not in ("OPEN","FIST"): prev_wrist_x = None
            else:
                if gesture == "FIST":   action_fist(lm)
                else:                   fist_start = None
        else:
            prev_wrist_x = None
            prev_palm_y  = None
            fist_start   = None

        draw_hud(frame, gesture)
        prev_gesture = gesture

        cv2.imshow("GESTURE CONTROL  |  Q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("\n  Closed. Goodbye!\n")

if __name__ == "__main__":
    main()
