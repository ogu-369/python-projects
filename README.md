# Python Portfolio

This repository contains Python projects showcasing my work.

## Repository Information
- **HTTPS URL:** [https://github.com/ogu-369/python-projects.git](https://github.com/ogu-369/python-projects.git)
- **SSH URL:** `git@github.com:ogu-369/python-projects.git`

## Projects
### Face Verifier
A Python application that performs real-time face verification using OpenCV and DeepFace.

#### Features
- Uses OpenCV for video capture and face detection.
- Employs DeepFace for face verification with the ArcFace model.
- Supports asynchronous face verification with threading and ThreadPoolExecutor.
- Displays real-time match results on the video feed.

#### Installation
- It is recommended to set up a virtual environment before installing dependencies:
  ```sh
  python -m venv venv
  source venv/bin/activate  # On Windows use: venv\Scripts\activate
  ```

1. Clone the repository:
   ```sh
   git clone https://github.com/ogu-369/python-projects.git
   ```
2. Navigate into the project directory:
   ```sh
   cd python-projects
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

#### Usage
- Ensure `reference.jpg` is placed inside the `img` directory before running the script.

Run the face verification script:
```sh
python face_verifier.py
```
Press 'q' to exit the program.

## License
MIT License.

