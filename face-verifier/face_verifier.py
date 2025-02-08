import cv2
from deepface import DeepFace
from concurrent.futures import ThreadPoolExecutor
import threading
import traceback
import os


class FaceVerifier:
    def __init__(self, reference_image_path, max_threads=1):
        """顔認証を管理するクラス"""
        self.reference_img = cv2.imread(reference_image_path)

        if self.reference_img is None:
            raise FileNotFoundError(f"Error: {reference_image_path} が見つからないか、正しく読み込めません。")

        # 参照画像を (BGR -> RGB) に変換
        self.reference_img = cv2.cvtColor(self.reference_img, cv2.COLOR_BGR2RGB)

        # OpenCV の顔検出器 (Haar Cascade)
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        if not os.path.exists(cascade_path):
            raise FileNotFoundError(f"Haar cascade file not found: {cascade_path}")
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

        self.face_match = False
        self.lock = threading.Lock()  # スレッド安全性のためのロック
        self.executor = ThreadPoolExecutor(max_workers=max_threads)

    def detect_face_opencv(self, frame):
        """OpenCV の Haar Cascade を使って顔を検出"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # グレースケール変換
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        return len(faces) > 0  # 顔が 1 つ以上検出されたら True

    def check_face(self, frame):
        """顔認識をスレッドで処理"""
        try:
            # まず OpenCV で顔を検出
            if not self.detect_face_opencv(frame):
                print("顔が検出されませんでした。")
                with self.lock:
                    self.face_match = False
                return  # 顔がない場合はスキップ

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 顔認証を実行
            result = DeepFace.verify(frame_rgb, self.reference_img.copy(), model_name="ArcFace")
            with self.lock:
                self.face_match = result.get('verified', False)

        except Exception as e:
            print(f"Face verification error:", traceback.format_exc())
            with self.lock:
                self.face_match = False

    def async_check_face(self, frame):
        """スレッドプールを使って非同期で顔認証を実行"""
        self.executor.submit(self.check_face, frame.copy())


def main_loop():
    """メイン処理ループ"""
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    face_verifier = FaceVerifier("img/reference.jpg")
    counter = 0

    try:
        while True:
            ret, frame = cap.read()

            if ret:
                if counter % 30 == 0:
                    face_verifier.async_check_face(frame)
                counter += 1

            if face_verifier.face_match:
                cv2.putText(frame, "MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            else:
                cv2.putText(frame, "NO MATCH", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

            cv2.imshow('video', frame)

            # 'q'を押下で終了
            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main_loop()
