import whisper
import os
from pydub import AudioSegment
import torch

# 音声ファイルのパスを指定
AUDIO_FILE_PATH = "audio/" # audio/ の後に動画ファイル名を追加
OUTPUT_FILE_PATH = "outputs/"
CHUNK_LENGTH_MS = 10 * 60 * 1000  # 10分（600,000ミリ秒）

def split_audio(file_path, chunk_length_ms=CHUNK_LENGTH_MS):
    """音声ファイルを指定した長さ（ミリ秒単位）で分割"""
    audio = AudioSegment.from_file(file_path)
    chunks = [audio[i:i + chunk_length_ms] for i in range(0, len(audio), chunk_length_ms)]

    chunk_files = []
    for i, chunk in enumerate(chunks):
        chunk_filename = f"{os.path.splitext(file_path)[0]}_part{i+1}.mp3"
        chunk.export(chunk_filename, format="mp3")
        chunk_files.append(chunk_filename)

    return chunk_files

def transcribe_audio(audio_path, model):
    """Whisperで音声を文字起こし"""
    result = model.transcribe(audio_path)
    return result["text"]

if __name__ == "__main__":
    if not os.path.exists(AUDIO_FILE_PATH):
        print(f"エラー: 指定されたファイル '{AUDIO_FILE_PATH}' が見つかりません。")
        exit(1)

    print("音声ファイルを分割しています...")
    chunk_files = split_audio(AUDIO_FILE_PATH)
    print(f"{len(chunk_files)} 個のファイルに分割されました。")

    # 出力ファイルのパス（元のファイル名 + _transcription.txt）
    output_filename = os.path.splitext(OUTPUT_FILE_PATH)[0] + "_transcription.txt"

    # デバイスの選択（GPU が使えるなら CUDA、なければ CPU）
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = whisper.load_model("medium").to(device)  # CPUでは FP16 を無効化

    with open(output_filename, "w", encoding="utf-8") as output_file:
        for i, chunk_file in enumerate(chunk_files):
            print(f"文字起こし中: {chunk_file} ...")
            transcription = transcribe_audio(chunk_file, model)

            # 各部分の結果を追記
            output_file.write(f"\n--- {i+1} 部分目 ---\n")
            output_file.write(transcription + "\n")

            print(f"文字起こし完了: {chunk_file}")

    print(f"\nすべての文字起こしが完了しました! 結果は '{output_filename}' に保存されました。")
