from __future__ import division
import re
import sys
from google.cloud import speech
import pyaudio
import os
import numpy as np
from six.moves import queue

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks audio size

banList = ["fuk", "beach", "holyshit"]

class MicrophoneStream(object):

    def getOutputDeviceIndex(self):
        # Get all output devices
        for i in range(self._audio_interface.get_device_count()):
            device = self._audio_interface.get_device_info_by_index(i)
            # print(device['name'], device['index'])
            if device['name'] == "CABLE Input (VB-Audio Virtual C": return device['index']


    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk
        self._buff = queue.Queue()
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(format=pyaudio.paInt16, channels=1, rate=self._rate, input=True, frames_per_buffer=self._chunk, stream_callback=self._fill_buffer)
        self.closed = False
        self._output_audio_interface = pyaudio.PyAudio()
        self._output_audio_stream = self._output_audio_interface.open(format=pyaudio.paInt16, channels=1, rate=self._rate, output=True, output_device_index=self.getOutputDeviceIndex())
        self.audio_history = []
        self.transcript = ""
        self.previous_transcript = ""
        self.clean_transcript = ""


    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            self.data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    self.data.append(chunk)
                except queue.Empty:
                    break
            

            if len(self.audio_history) > 0:
                audio = self.audio_history[0]
                
                if not '*' in self.transcript:
                    self._output_audio_stream.write(audio)

            self.audio_history.append(b"".join(self.data))

            if len(self.audio_history) > 10:
                self.audio_history = self.audio_history[1:]

            yield b"".join(self.data)

def main():
    language_code = "en-US"

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './google_credentials.json'

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        profanity_filter=True)

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True)

    stream = MicrophoneStream(RATE, CHUNK)
    audio_generator = stream.generator()

    requests = (
        speech.StreamingRecognizeRequest(audio_content=content)
        for content in audio_generator)

    responses = client.streaming_recognize(streaming_config, requests)

    # output.write(b"".join(stream.data), len(stream.data))

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        # Get current chunk of audio
        # Current timestamps = []
        
        transcript = result.alternatives[0].transcript

        newTranscript = transcript
        for (i, word) in enumerate(stream.previous_transcript.split(" ")):

            if word in banList: 
                newTranscript = newTranscript.replace(word, "*")

            if not '*' in word:
                newTranscript = newTranscript.replace(word, "", 1)

        stream.previous_transcript = transcript

        if len(newTranscript.strip()) == 0:
            stream.transcript = transcript
            # print(transcript)
        else:
            stream.transcript = newTranscript
            # print(newTranscript)

        stream.clean_transcript = transcript
        print(transcript)

        if result.is_final:
            stream.transcript = ""

# if __name__  == '__main__':
#     main()