import whisper


class SpeechToTextConverter:

    def __init__(self, config):
        self.config = config

    def speech_to_text(self):
        model = whisper.load_model("base")
        result = model.transcribe(self.config.get_record_audio_output_file(), fp16=False)
        return result["text"]
