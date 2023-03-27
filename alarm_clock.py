import sys; print(sys.executable, sys.prefix)
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import pyaudio
import wave
import sys
import os
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# this is just to make the output look nice
formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")
# this logs to stdout and I think it is flushed immediately
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info('Set volume for DAC card to 99%')
logger.info('Set volume for DAC card to 99%')

# Shell out command to set volume to 100%

os.system("amixer -c 2 set Digital 99%")




"""PyAudio Example: Play a wave file (callback version)."""

wave_file="/usr/local/alarm-clock/rainsounds01.wav"
# https://people.csail.mit.edu/hubert/pyaudio/docs/
if len(sys.argv) > 1:
    wave_file=sys.argv[1]

wf = wave.open(wave_file, 'rb')

# instantiate PyAudio (1)
p = pyaudio.PyAudio()

info = p.get_host_api_info_by_index(0)
print("Info is")
print(info)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))


# define callback (2)
def pyaudio_callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)


def open_stream():
    s = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=pyaudio_callback)
    # It's starts playing automatically... so i just immediately stop it
    s.stop_stream()
    return s

stream = open_stream()
started = 0
play_or_pause = "pause"

def playTrack():
    global stream
    print("Playing track")
    stream.start_stream()

def pauseTrack():
    print("Pausing track")
    stream.stop_stream()


def button_callback(channel):
    global play_or_pause
    print("Button was pushed!")
    if play_or_pause == "play":
        play_or_pause = "pause"
        pauseTrack()
    else:
        play_or_pause = "play"
        playTrack()

#GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(36, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled high (off)

GPIO.add_event_detect(36,GPIO.FALLING,callback=button_callback, bouncetime=800) # Setup event on pin 36 falling edge

while True:
    while stream.is_active():
        time.sleep(0.500)

    if play_or_pause == "play":
        # Reset (so we can loop the track)
        wf.rewind()
        stream.close()
        stream = open_stream()
        playTrack()

    time.sleep(0.200)


GPIO.cleanup() # Clean up
print("Stopping stream")
# stop stream (6)
stream.close()
wf.close()
# close PyAudio (7)
p.terminate()
