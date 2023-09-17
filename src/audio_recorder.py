import io
import wave
import pyaudio
from retry import retry
import threading


class AudioRecorder:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024

    def __init__(self, config):
        self.config = config
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []
        self.stop_recording = threading.Event()

    def startRecording(self):
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                      rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK)
        self.frames = []
        print("Microphone open. Recording started...")

        while not self.stop_recording.is_set():
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    @retry(Exception, tries=3, delay=0)
    def stopRecording(self):
        print(f"Started Stopping recording")
        self.stop_recording.set()
        if self.stream is None:
            print("No active recording.")
            return

        self.stream.stop_stream()
        self.stream.close()
        self.stop_recording.clear()
        print("Recording finished.")

        # Create a BytesIO object to store audio data in memory
        audio_file = io.BytesIO()

        # Create a wave file writer with the same format as the input audio
        with wave.open(audio_file, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)

            # Write the audio frames to the wave file
            wf.writeframes(b''.join(self.frames))

        # Get the file bytes from the BytesIO object
        audio_bytes = audio_file.getvalue()

        return audio_bytes