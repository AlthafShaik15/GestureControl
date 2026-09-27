# 🖐️ GestureControl

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/OpenCV-Computer%20Vision-red?logo=opencv&logoColor=white">
  <img src="https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange?logo=google&logoColor=white">
  <img src="https://img.shields.io/badge/NumPy-Numerical%20Computing-blue?logo=numpy&logoColor=white">
  <img src="https://img.shields.io/github/stars/AlthafShaik15/GestureControl?style=flat&logo=github">
</p>

<p align="center">
  <b>Control your computer using simple hand gestures ✋</b>
</p>

---

## 📌 What is GestureControl?

**GestureControl** is a computer vision project that lets you control different parts of your computer using your **hand gestures**.

Instead of always using a mouse and keyboard, you can use your webcam and move your hand in front of it.

For example:

* ☝️ Point with your finger → Move the mouse
* 🤏 Pinch your fingers → Left click
* ✊ Make a fist → Right click
* ✌️ Show two fingers → Scroll
* 👍 Thumbs up → Increase volume
* 👎 Thumbs down → Decrease volume
* 🤟 Show three fingers → Take a screenshot
* 🖐️ Show an open palm → Pause/stop interaction
* 🖐️ Show four fingers → Play/Pause media

The project uses **MediaPipe** to understand where your fingers are and then converts those gestures into normal computer actions.

So the basic idea is:

```text
Your Hand
    ↓
Webcam
    ↓
MediaPipe detects your hand
    ↓
GestureControl understands the gesture
    ↓
Computer performs an action
```

---

# ✨ Features

### 🖱️ Mouse Control

You can move your mouse without touching it.

Point your index finger toward the camera and move it around.

```text
☝️ Point
   ↓
Move your finger
   ↓
Move the mouse cursor
```

---

### 🖱️ Left Click

Bring your thumb and index finger together to make a pinch.

```text
🤏 Pinch
   ↓
Left Click
```

---

### 🖱️ Right Click

Make a fist.

```text
✊ Fist
   ↓
Right Click
```

---

### 📜 Scrolling

Show two fingers and move your hand up or down.

```text
✌️ Two Fingers
      ↓
Move Hand
      ↓
Scroll
```

---

### 🔊 Volume Control

Use your thumb to control the computer volume.

```text
👍 Thumbs Up
      ↓
Volume Up

👎 Thumbs Down
      ↓
Volume Down
```

---

### 💡 Brightness Control

Use an L-shaped gesture with your thumb and index finger.

```text
L Gesture
    ↓
Increase Screen Brightness
```

---

### 📸 Screenshot

Show three fingers.

```text
🖐️ Three Fingers
       ↓
Take Screenshot
```

The screenshot is automatically saved as a PNG file.

---

### 🎵 Media Control

Show four fingers to play or pause media.

```text
🖐️ Four Fingers
       ↓
Play / Pause Media
```

---

# 🎮 Gesture Controls

Here is the complete list of gestures currently supported by the project:

| Gesture           | Action              |
| ----------------- | ------------------- |
| ☝️ Point          | Move mouse cursor   |
| 🤏 Pinch          | Left click          |
| ✌️ Two fingers    | Scroll              |
| ✊ Fist            | Right click         |
| 🖐️ Open palm     | Pause / neutral     |
| 👍 Thumbs up      | Increase volume     |
| 👎 Thumbs down    | Decrease volume     |
| 🤟 L-shape        | Increase brightness |
| 🖐️ Three fingers | Take screenshot     |
| 🖐️ Four fingers  | Play / pause media  |

These mappings are implemented in `controller.py`, while the gesture names are identified by `gesture_classifier.py`.

---

# 🧠 How Does It Work?

Don't worry if you don't know anything about computer vision.

The project basically follows **four simple steps**.

### Step 1 — Camera

Your webcam continuously captures video.

```text
📷 Webcam
   ↓
Live Video
```

OpenCV is used to access the webcam and process the video frames.

---

### Step 2 — Find Your Hand

MediaPipe looks at the camera image and tries to find your hand.

It identifies important points on your hand.

For example:

```text
        ☝️
        ●  ← Finger
        |
     ●──●──●
        |
        ●
        |
       Wrist
```

The project uses MediaPipe's hand tracking system to obtain **21 hand landmark points** for the detected hand.

You don't need to manually tell the program where your fingers are.

MediaPipe does that automatically.

---

### Step 3 — Understand the Gesture

After finding your hand, the program checks the positions of your fingers.

For example:

```text
Index Finger Up
Middle Finger Down
Ring Finger Down
Pinky Down
        ↓
     POINT
```

Or:

```text
Index + Middle Up
Ring + Pinky Down
        ↓
    TWO FINGERS
```

The `gesture_classifier.py` file is responsible for turning these hand positions into recognizable gesture names.

---

### Step 4 — Perform the Action

Once the gesture is recognized, the program performs the corresponding computer action.

For example:

```text
☝️ Point
   ↓
Recognized as "point"
   ↓
Mouse cursor moves
```

```text
🤏 Pinch
   ↓
Recognized as "pinch"
   ↓
Computer performs left click
```

The `controller.py` file handles these actions using libraries such as PyAutoGUI and other Windows controls.

---

# 🏗️ Simple Architecture

```text
                  📷 Webcam
                     │
                     ▼
              ┌──────────────┐
              │    OpenCV    │
              │ Video Capture│
              └───────┬──────┘
                      │
                      ▼
              ┌──────────────┐
              │   MediaPipe  │
              │ Hand Tracking│
              └───────┬──────┘
                      │
                      ▼
              ┌──────────────┐
              │    Gesture   │
              │  Classifier  │
              └───────┬──────┘
                      │
                      ▼
              ┌──────────────┐
              │   Gesture    │
              │  Controller  │
              └───────┬──────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
      🖱️ Mouse      🔊 Volume     💡 Brightness
        │
        ├────────── 📜 Scroll
        ├────────── 📸 Screenshot
        └────────── 🎵 Media
```

---

# 🛠️ Technologies Used

| Technology                   | What it does                        |
| ---------------------------- | ----------------------------------- |
| 🐍 Python                    | Main programming language           |
| 👁️ OpenCV                   | Captures and processes webcam video |
| ✋ MediaPipe                  | Detects and tracks the hand         |
| 🔢 NumPy                     | Works with hand landmark data       |
| 🖱️ PyAutoGUI                | Controls mouse and screenshots      |
| ⌨️ Pynput / Keyboard         | Helps control computer input        |
| 🔊 Pycaw                     | Controls Windows system volume      |
| 💡 Screen Brightness Control | Controls screen brightness          |

The current `requirements.txt` includes OpenCV, MediaPipe, PyAutoGUI, Pynput, and NumPy; the controller additionally uses Windows-specific packages for volume and brightness control.

---

# 📂 Project Structure

```text
GestureControl/
│
├── 📄 main.py
│   └── Starts the application
│
├── 📄 gesture_detector.py
│   └── Finds and tracks your hand
│
├── 📄 gesture_classifier.py
│   └── Understands which gesture you are making
│
├── 📄 controller.py
│   └── Converts gestures into computer actions
│
├── 📄 config.py
│   └── Contains project settings
│
├── 📄 requirements.txt
│   └── Required Python libraries
│
├── 🖼️ screenshot_*.png
│   └── Screenshots created by the application
│
└── 📄 .gitignore
```

The repository currently contains these main Python modules plus `requirements.txt` and a project screenshot.

---

# 🚀 Getting Started

## 1️⃣ Clone the Project

Open your terminal and run:

```bash
git clone https://github.com/AlthafShaik15/GestureControl.git
```

Then enter the project folder:

```bash
cd GestureControl
```

---

## 2️⃣ Create a Virtual Environment

A virtual environment keeps this project's Python libraries separate from other projects.

On Windows:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

You should now see something similar to:

```text
(venv) C:\YourFolder\GestureControl>
```

---

## 3️⃣ Install the Required Libraries

Run:

```bash
pip install -r requirements.txt
```

Your project already provides a `requirements.txt` containing the main dependencies needed for the application.

---

# ▶️ Run the Project

After installing everything, run:

```bash
python main.py
```

Your webcam window should open.

You should see:

* Your camera feed
* Hand landmarks
* Detected gesture
* Current action
* FPS
* Gesture guide

The application starts with the webcam and uses `Q` to quit or `P` to pause.

---

# ⌨️ Keyboard Controls

You don't have to control everything with your hand.

The application also provides two keyboard controls:

| Key | Action                         |
| --- | ------------------------------ |
| `Q` | Quit the application           |
| `P` | Pause / Resume gesture control |

These controls are handled directly inside `main.py`.

---

# ⚙️ Configuration

You can change some project settings inside:

```text
config.py
```

For example:

```python
CAMERA_INDEX = 0

FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

SMOOTHING = 0.25

SCROLL_SPEED = 15
```

These settings control things such as:

* 📷 Which camera is used
* 🖥️ Camera resolution
* 🖱️ Cursor smoothness
* 📜 Scroll speed
* ✋ Gesture detection sensitivity

The current configuration uses a 1280×720 camera frame and includes settings for smoothing, scrolling, gesture thresholds, and tracking area.

---

# 🖱️ How Mouse Control Works

One of the most interesting parts of the project is controlling the mouse without touching it.

When you point your index finger:

```text
☝️
```

the program finds the position of your index fingertip.

It then converts that position from the camera screen into a position on your computer screen.

```text
Camera Position
       ↓
Convert Position
       ↓
Computer Screen Position
       ↓
🖱️ Mouse Moves
```

The cursor movement is also smoothed so that small hand movements don't make the mouse jump around.

---

# 🤏 How Clicking Works

### Left Click

Make a pinch:

```text
Thumb + Index Finger
        ↓
      🤏
        ↓
   Left Click
```

The program also waits for the gesture to remain stable for a few frames before triggering the click. This helps prevent accidental clicks caused by small movements.

### Right Click

Make a fist:

```text
✊
↓
Right Click
```

A short cooldown is also used to prevent repeated clicks from happening too quickly.

---

# 🔊 How Volume Control Works

### Increase Volume

```text
👍
↓
Volume +10%
```

### Decrease Volume

```text
👎
↓
Volume -10%
```

The project reads the current Windows speaker volume and adjusts it in small steps.

---

# 💡 Brightness Control

Make an **L-shaped gesture**:

```text
☝️
  ──
```

The application increases the display brightness by a fixed amount.

```text
L Gesture
    ↓
Brightness +10%
```

This part uses the `screen_brightness_control` package and is intended for Windows systems.

---

# 📸 Taking Screenshots

Show three fingers:

```text
🤟
↓
Screenshot
```

The application automatically creates a PNG image with a timestamp-based filename.

Example:

```text
screenshot_1774970122.png
```

The screenshot functionality is implemented using PyAutoGUI.

---

# 🎵 Media Control

Show four fingers:

```text
🖐️
↓
Play / Pause
```

The application sends a media play/pause command to the computer.

---

# 🛡️ Stability & Safety Features

The project doesn't immediately trigger every action the moment a gesture is detected.

For some actions, the gesture needs to remain stable for several frames.

For example:

```text
Gesture detected
      ↓
Check stability
      ↓
Gesture remains stable?
      ↓
     YES
      ↓
Perform action
```

This helps reduce accidental clicks and unwanted actions.

The project also uses cooldown periods for actions such as clicking, volume changes, brightness changes, screenshots, and media control.

---

# 💻 System Requirements

You will need:

* 🖥️ Windows PC
* 📷 Working webcam
* 🐍 Python
* ✋ Good camera visibility of your hand
* 🌐 Internet connection for installing Python packages

The volume and brightness controls in the current implementation use Windows-specific libraries/APIs, so those features are not designed as cross-platform functionality.

---

# ⚠️ Tips for Better Results

For better gesture detection:

### 💡 Use good lighting

Make sure your hand is clearly visible.

### 📷 Keep your hand inside the camera frame

Don't move your hand too far outside the camera view.

### 🖐️ Use one hand

The current application initializes the detector for a maximum of one hand.

### 🐌 Move slowly when needed

Very fast movements can make gestures harder to recognize.

### 🖥️ Keep the camera stable

A stable camera generally gives more consistent results.

---

# 🎯 Why I Built This

I built **GestureControl** to explore how computer vision can make human-computer interaction more natural.

Instead of:

```text
Hand → Mouse → Computer
```

the goal is to create:

```text
Hand → Camera → AI → Computer
```

It is a practical project that combines **computer vision, hand tracking, gesture recognition, and computer automation** into one application.

---

# 🔮 Future Improvements

Some improvements that could make the project even more useful:

* ✋ Support two hands at the same time
* 🎮 Add more custom gestures
* ⚙️ Allow users to customize gesture actions
* 🖱️ Improve cursor movement accuracy
* 📜 Improve scrolling control
* 🔊 Add volume down/up customization
* 💡 Add brightness down gesture
* 🎵 Add more media controls
* 🖥️ Add a graphical settings interface
* 📱 Explore mobile support
* 🌐 Add a web-based control interface
* 🤖 Add machine-learning-based custom gesture recognition

---

# 📚 What You Can Learn From This Project

If you're a beginner, this project is a good example of how several technologies can work together.

You can learn:

```text
Python
  ↓
OpenCV
  ↓
Camera Processing
  ↓
MediaPipe
  ↓
Hand Tracking
  ↓
Gesture Recognition
  ↓
Computer Automation
```

You don't need to understand everything at once.

Start with:

1. How OpenCV reads the webcam
2. How MediaPipe finds the hand
3. What hand landmarks are
4. How the program identifies gestures
5. How a gesture becomes a computer action

---

# 👨‍💻 Author

## Althaf Shaik

[![GitHub](https://img.shields.io/badge/GitHub-AlthafShaik15-black?logo=github)](https://github.com/AlthafShaik15)

🔗 **Repository:**
https://github.com/AlthafShaik15/GestureControl

---

# ⭐ Support

If you found this project interesting, consider giving the repository a ⭐ on GitHub.

It helps support the project and makes it easier for others to discover it.

---

<p align="center">

## 🖐️ GestureControl

### **Control your computer. Just use your hands.**

</p>
