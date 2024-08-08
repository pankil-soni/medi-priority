import speech_recognition as sr
import os
from moviepy.editor import VideoFileClip
import shutil

# Extract audio from video and save it as a wav file
def speech_to_text(audio_path):
    recognizer = sr.Recognizer()
    audio_file = sr.AudioFile(audio_path)
    with audio_file as source:
        audio_data = recognizer.record(source)

    text = ""
    try:
        text = recognizer.recognize_google(audio_data)
        # print("Text: "+text)
    except Exception as e:
        print("error:", e)

    return text

# Convert speech to text from an audio file
def extract_audio(video_path, output_folder):
    video = VideoFileClip(video_path)
    audio_path = os.path.join(output_folder, "audio.wav")
    video.audio.write_audiofile(audio_path)
    return audio_path

def extract_video_to_text(video_path):
    audio_path = extract_audio(video_path, "./tmp")
    print(speech_to_text(audio_path))

# Main runner function
extract_video_to_text("../intro.mp4")
extract_audio("")