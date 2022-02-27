# LiveGuard

**Made by [Frederic Jarjour](https://github.com/fredjarjour), [Eduard Anton](https://github.com/persosireduard), [ChengYue Li](https://github.com/MrCheng11), and [Mandy Huang](https://github.com/crisscrossapplesauce02)**

**This project was built for the [Code.Jam(XI)](https://code-jam-xi.devpost.com/) hackathon. [Check out its Devpost page!](https://devpost.com/software/mmhhh)**

## Requirements
To run the program on your device, you need:
- [Python](https://www.python.org/downloads/)
- [Mediapipe](https://google.github.io/mediapipe/getting_started/install.html)
- [OpenCV-Python](https://pypi.org/project/opencv-python/)
- [pyvirtualcam](https://pypi.org/project/pyvirtualcam/)
- [NumPy](https://numpy.org/install/)
- [pandas](https://pypi.org/project/pandas/)
- [PyAudio](https://pypi.org/project/PyAudio/)
- [VB-CABLE Virtual Audio Device](https://vb-audio.com/Cable/)

## Inspiration

Watching people talking on a screen has become more and more present in our lives. Whether it be on YouTube, Twitch, or even in a Zoom meeting, live virtual interactions are at an all-time high. One issue that persists in this environment, however, is that anyone can slip up and swear or make an obscene gesture to their webcam in the heat of the moment.

## What it does

LiveGuard can pixelate any vulgar gesture that the neural network model detects on your webcam, as well as censor any detected swear words from your microphone input, allowing for a stress-free environment while streaming or in a work meeting.

## How we built it

- Video input: OpenCV
- Hand tracking: Mediapipe Hands
- Hand gesture model: sklearn & pandas
- Webcam Image Processing: NumPy
- Webcam output: pyvirtualcam
- Microphone input: PyAudio
- Speech-to-Text: Google Cloud Speech API
- Application: Python

## Challenges we ran into

- Processing audio and video input, and outputting them to virtual drivers
- Synchronizing text-to-speech with censoring overlay on the microphone
- Building the external ML model to recognize new signs

## Accomplishments that we're proud of

We are very proud of the final project and the time and effort we put into it. While we encountered several problems, we overcame them or worked around them to produce a functional product. We are also proud of processing the video and audio outputs, since modifying them was no easy task.

## What we learned

- How to construct a virtual microphone device
- How to implement live censoring of audio input
- How to track hand gestures through Mediapipe's hand landmarks
- How to create pandas dataframes to build an sklearn ML model

## What's next for LiveGuard

LiveGuard is still in its very early development, we envision many new features that could be added, such as:
- Implementing more toggleable features with a GUI
- Live DMCA protection for streamers
- More camera gesture controls
