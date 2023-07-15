import ffmpeg
import whisper
import numpy as np


class SpeechToTextConverter:

    def __init__(self, config):
        self.config = config
        self.model = whisper.load_model("base")

    def speech_to_text(self, recording_bytes):
        print(f"Started convert speech to text.")

        file_bytes = b''.join(recording_bytes)
        audio = self.load_audio2(file_bytes)

        result = self.model.transcribe(file_bytes, fp16=False)
        print(f"Text result is {result['text']}.")

        return result["text"]

    def load_audio2(self, bytes, sr: int = 44100):
        """
        Open an audio file and read as mono waveform, resampling as necessary

        Parameters
        ----------
        file: (str, bytes)
            The audio file to open or bytes of audio file

        sr: int
            The sample rate to resample the audio if necessary

        Returns
        -------
        A NumPy array containing the audio waveform, in float32 dtype.
        """


        try:
            # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
            # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
            out, _ = (
                ffmpeg.input('pipe:', threads=0)
                .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
                .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=bytes)
            )
        except ffmpeg.Error as e:
            raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

        return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0
