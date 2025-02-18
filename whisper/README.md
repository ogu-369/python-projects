# Whisper Audio Transcription Script

A simple Python script to split a large audio file into 10-minute chunks and transcribe each chunk using [OpenAI Whisper](https://github.com/openai/whisper). The transcribed text is then saved into a single output file.

---

## Overview

1. **Audio Splitting**  
   - Splits a long audio file into 10-minute segments (default setting) using [pydub](https://github.com/jiaaro/pydub).  
   - Each segment is exported as an MP3 file in the same directory.

2. **Transcription**  
   - Uses the [OpenAI Whisper](https://github.com/openai/whisper) model (`medium` by default) to transcribe each chunk.  
   - Automatically detects and utilizes a GPU if available (`device = "cuda"`), otherwise runs on CPU.  

3. **Output**  
   - Appends all transcription segments to a single text file named `[OUTPUT_FILE_PATH]_transcription.txt`.  

---

## Prerequisites

- **Python 3.7+** (tested on Python 3.7 or above).
- **FFmpeg**  
  - Required by pydub for audio file handling.  
  - Installable on most systems via package managers (e.g., `brew install ffmpeg` on macOS, `apt-get install ffmpeg` on Ubuntu, etc.).
- **PyTorch**  
  - Required for running Whisper models.  
  - Install with GPU support if you have a compatible GPU; otherwise, CPU version will suffice.
- **OpenAI Whisper** (`whisper`), **pydub**, **torch**  
  - Install these via pip (see below).

---

## Installation

1. **Clone or download** this repository.
2. **Install dependencies**:
   ```bash
   pip install torch pydub openai-whisper
   ```
   > Alternatively, you can install from a `requirements.txt` if provided.

3. **Verify FFmpeg** is installed and accessible in your system path.

---

## Usage

1. **Prepare your audio file**  
   - Place your audio (or video) file in the `audio/` directory.  
   - Update `AUDIO_FILE_PATH` in the script to match the exact file name if needed.  
   - By default, the script looks for `audio/` and splits the file found there.

2. **Optional: Adjust parameters**  
   - **Chunk Length**: Change `CHUNK_LENGTH_MS` to modify the default splitting duration (in milliseconds).  
   - **Whisper Model**: In the script, you can change `whisper.load_model("medium")` to other sizes (`tiny`, `base`, `small`, `large`) depending on your needs and system resources.

3. **Run the script**  
   ```bash
   python your_script_name.py
   ```
   - The script will:
     1. Check if `AUDIO_FILE_PATH` exists.
     2. Split the file into 10-minute segments.
     3. Transcribe each chunk with Whisper.
     4. Save the combined transcription to `[OUTPUT_FILE_PATH]_transcription.txt`.

4. **Check output**  
   - The MP3 chunks will appear in the same directory as the original file, named with `_part1.mp3`, `_part2.mp3`, etc.  
   - The transcription file is saved in the `outputs/` directory with `_transcription.txt` appended to its name.

---

## Script Details

- **split_audio(file_path, chunk_length_ms)**  
  Splits the given audio file into smaller segments of length `chunk_length_ms` (default = 10 minutes). Exports each chunk as an MP3 file.

- **transcribe_audio(audio_path, model)**  
  Transcribes a given MP3 file using Whisper and returns the text.

- **Main execution flow**  
  1. Verifies that the audio file path exists.  
  2. Calls `split_audio()` to break the file into chunks.  
  3. Loads the Whisper model (`medium`) onto GPU if available.  
  4. Transcribes each chunk in sequence, appending the results to a single output text file.  

---

## Notes and Tips

- If you run out of memory with the `medium` model, try using a smaller model (e.g., `"small"` or `"tiny"`).
- If you face slow processing or want better accuracy, you can choose bigger models like `"large"`, but keep in mind they may require more GPU VRAM.
- For longer audio files, consider adjusting `CHUNK_LENGTH_MS` if you need different segmentation.

---

## License

This script is provided under the **MIT License**. Refer to the [LICENSE](https://opensource.org/licenses/MIT) for more details.  
Please note that [OpenAI Whisper](https://github.com/openai/whisper) and [pydub](https://github.com/jiaaro/pydub) are distributed under their own licenses.

---

## Contact

For any issues or improvements, please create an issue or submit a pull request.