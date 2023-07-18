import whisper
import numpy as np


class SpeechToTextConverter:

    def __init__(self, config):
        self.config = config
        self.model = whisper.load_model("base")

    def speech_to_text(self, recording_bytes):
        print(f"Started convert speech to text.")

        audio = np.frombuffer(recording_bytes, np.int16).flatten().astype(np.float32) / 32768.0

        result = self.model.transcribe(audio, fp16=False)
        print(f"Text result is {result['text']}.")

        return result["text"]
