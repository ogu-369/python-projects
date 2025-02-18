# Face Verifier

A Python application that performs real-time face verification using **OpenCV** and **DeepFace**. This README integrates details from both the existing and newly created documentation, providing a comprehensive overview of the project.

---

## Overview

- Real-time face detection via OpenCV Haar Cascades.  
- Face verification using DeepFace (ArcFace model by default).  
- Asynchronous face verification leveraging threads and `ThreadPoolExecutor`.  
- Real-time results displayed on the video feed: shows "MATCH" or "NO MATCH" depending on whether the detected face matches the reference image.

---

## Features

1. **OpenCV for Video Capture**  
   - Grabs frames from the camera (webcam).
   - Converts them to a proper format (BGR → RGB) for DeepFace processing.
   - Detects faces via the OpenCV Haar Cascade classifier.

2. **DeepFace for Face Verification**  
   - Compares the captured face with a reference image.
   - Uses the `ArcFace` model by default (customizable to other models like "Facenet", "Facenet512", "VGG-Face", "OpenFace", etc.).

3. **Asynchronous Processing**  
   - Uses Python's `ThreadPoolExecutor` for parallel (non-blocking) face verification.
   - Main loop continues to display frames while background threads handle the verification.

4. **Real-time Match Feedback**  
   - Overlays "MATCH" or "NO MATCH" on the video feed.

---

## Directory Structure

```
.
├── img
│   └── reference.jpg       # Reference image used for face verification
├── face_verifier.py        # Main script (file name can be customized)
├── requirements.txt        # List of Python dependencies
└── README.md               # This file
```

> **Note**: Make sure you have your reference image placed in the `img` directory as `reference.jpg` (or change the path in the script accordingly).

---

## Requirements

1. **Python 3.7+**  
   - Recommended version for compatibility with DeepFace and OpenCV.

2. **OpenCV**  
   - Required for video capture and face detection.  
   - Install via:  
     ```bash
     pip install opencv-python
     ```

3. **DeepFace**  
   - Required for face verification.  
   - Install via:  
     ```bash
     pip install deepface
     ```
   - DeepFace may also require additional libraries like **TensorFlow** or **PyTorch** (depending on your environment).

4. **Haar Cascade (OpenCV)**  
   - The script expects `haarcascade_frontalface_default.xml` which is typically included with OpenCV installations.
   - If you face issues with finding this file, make sure your environment includes the OpenCV data directory or manually download the cascade file.

5. **Webcam**  
   - A built-in or external camera is required for real-time face detection.

---

## Installation

It is recommended to set up a virtual environment before installing dependencies:

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

1. **Clone the repository** (example URL; adjust if different):
   ```sh
   git clone https://github.com/ogu-369/python-projects.git
   ```

2. **Navigate into the project directory**:
   ```sh
   cd python-projects/face-verifier
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

---

## Usage

1. **Place the Reference Image**  
   - Ensure a reference image named `reference.jpg` is located in the `img` directory:
     ```sh
     mkdir -p img/
     # Place your reference.jpg into img/
     ```

2. **Run the Script**  
   - Execute the face verification script:
     ```sh
     python face_verifier.py
     ```
   - A window will open displaying the camera feed and real-time verification results.

3. **Exit**  
   - Press **'q'** while the video window is active to quit the program.

---

## How It Works

1. **Initialization (`FaceVerifier` class)**
   - Loads the reference image and converts it from BGR to RGB (DeepFace uses RGB).
   - Initializes the Haar Cascade classifier for face detection.
   - Prepares a `ThreadPoolExecutor` to handle verification asynchronously.

2. **Face Detection (`detect_face_opencv`)**
   - Converts each frame to grayscale.
   - Uses Haar Cascade to detect if at least one face is present in the frame.

3. **Face Verification (`check_face`)**
   - If a face is detected by OpenCV, DeepFace’s `verify` method compares it with the reference image.
   - A lock (`threading.Lock`) ensures thread-safe updates to the `face_match` flag.

4. **Asynchronous Verification (`async_check_face`)**
   - Submits the `check_face` task to the thread pool so that the main loop remains responsive.

5. **Main Loop (`main_loop`)**
   - Continuously captures frames from the webcam.
   - Every 30 frames (configurable), triggers the asynchronous `check_face`.
   - Displays "MATCH" or "NO MATCH" on the live feed depending on the latest verification result.

---

## Customization

1. **Reference Image Path**  
   - Update the path in the constructor:  
     ```python
     face_verifier = FaceVerifier("img/your_custom_reference.jpg")
     ```

2. **Frame Resolution**  
   - Modify camera properties:
     ```python
     cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
     ```

3. **Verification Frequency**  
   - Change `if counter % 30 == 0:` to a different modulus for more or fewer verifications per second.

4. **DeepFace Model**  
   - Switch `model_name="ArcFace"` to other supported models like `"Facenet"`, `"Facenet512"`, `"VGG-Face"`, `"OpenFace"`, or `"DeepFace"`.

5. **Thread Pool Size**  
   - Adjust `max_threads` in `FaceVerifier` to control parallelism:
     ```python
     face_verifier = FaceVerifier("img/reference.jpg", max_threads=2)
     ```

---

## Troubleshooting

1. **Haar Cascade File Not Found**  
   - Ensure `haarcascade_frontalface_default.xml` exists in your OpenCV data folder or manually specify its path:
     ```python
     cascade_path = "/path/to/haarcascade_frontalface_default.xml"
     ```

2. **DeepFace or Backend Issues**  
   - DeepFace may require **TensorFlow** or **PyTorch**.  
   - Install or update these libraries if you see backend errors.

3. **Camera Not Recognized**  
   - Try changing the capture initialization to:
     ```python
     cv2.VideoCapture(0)
     ```
   - Or use a different camera index instead of `0`.

4. **Performance Bottlenecks**  
   - Face verification with DeepFace can be CPU/GPU intensive.  
   - Lower the verification frequency (e.g., check every 60 frames).  
   - Consider GPU-accelerated frameworks if available.

---

## License

This project is provided under the **MIT License**. For details, see [LICENSE](https://opensource.org/licenses/MIT).  
Please note that OpenCV, DeepFace, and other dependencies each come with their own licenses.

---

## Contact / Contributions

For issues or suggestions, please open an issue or submit a pull request in the repository. Contributions are always welcome.