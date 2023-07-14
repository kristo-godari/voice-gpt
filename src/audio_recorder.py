import pyaudio
import wave
from retry import retry
import os
import threading


class AudioRecorder:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 5

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

        print("Recording finished.")
        self.stream.stop_stream()
        self.stream.close()

        wave_file = wave.open(self.config.get_record_audio_output_file(), 'wb')
        wave_file.setnchannels(self.CHANNELS)
        wave_file.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        wave_file.setframerate(self.RATE)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

        self.stream = None
        self.stop_recording.clear()

        if not os.path.isfile(self.config.get_record_audio_output_file()) or os.stat(
                self.config.get_record_audio_output_file()).st_size < 100:
            print(f"Text to Speech file does not exist or is too small.")
            raise Exception('Text to Speech file does not exist or is too small.')