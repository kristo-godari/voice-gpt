import tempfile
import whisper


class SpeechToTextConverter:

    def __init__(self, config):
        self.config = config
        self.model = whisper.load_model("base")

    def speech_to_text(self, recording_bytes: bytes):
        print(f"Started convert speech to text.")

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
            tmp_filename = tmp_file.name
            tmp_file.write(recording_bytes)

        result = self.model.transcribe(tmp_filename, fp16=False)
        print(f"Text result is {result['text']}.")

        return result["text"]
