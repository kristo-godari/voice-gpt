import pyaudio
import wave


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
        self.stop_recording = False

    def startRecording(self):
        self.stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                                      rate=self.RATE, input=True,
                                      frames_per_buffer=self.CHUNK)
        self.frames = []
        print("Microphone open. Recording started...")

        while not self.stop_recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)

    def stopRecording(self):

        self.stop_recording = True
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
        self.stop_recording = False
