import platform
from io import BytesIO
from pathlib import Path
import os


PLATFORM_NAME = platform.system()
SCRIPT_DIR = Path(__file__).parent

if PLATFORM_NAME == 'Windows':
    FFMPEG_PATH_EXE = str(Path(SCRIPT_DIR, "win", "ffmpeg", "ffmpeg.exe"))
    os.environ["PATH"] += os.pathsep + str(Path(FFMPEG_PATH_EXE).parent)
elif PLATFORM_NAME == 'Darwin':
    FFMPEG_PATH_EXE = str(Path(SCRIPT_DIR, "mac", "ffmpeg", "ffmpeg"))
    os.environ["LD_LIBRARY_PATH"] += ":" + str(Path(FFMPEG_PATH_EXE).parent)
else:
    FFMPEG_PATH_EXE = str(Path(SCRIPT_DIR, "linux", "ffmpeg", "ffmpeg"))
    os.environ["LD_LIBRARY_PATH"] += ":" + str(Path(FFMPEG_PATH_EXE).parent)

os.environ["FFMPEG_PATH_EXE"] = FFMPEG_PATH_EXE
os.environ["TEMP"] = f"{SCRIPT_DIR}\\Temp"


from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
import glob


def get_speech_from_text(text: str) -> BytesIO:
    """
    Получить речь из текста

    :param text: Текст для преобразования в речь
    :return: Речь в «сыром» формате
    """
    bytes_speech = BytesIO()
    tts = gTTS(text=text, lang="ru")
    tts.write_to_fp(bytes_speech)
    bytes_speech.seek(0)
    return bytes_speech


def play_speech(bytes_speech: BytesIO) -> None:
    """
    Воспроизвести речь

    :param bytes_speech: Речь в «сыром» формате
    """
    song = AudioSegment.from_file(bytes_speech, format="mp3")
    bytes_speech.seek(0)
    play(song)


def get_text_from_speech():
    """
    Получить текст с микрофона

    :return: Текст, записанный с микрофона
    """

    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print('Recording...')
    with mic as source:
        audio = recognizer.listen(source)
    return recognizer.recognize_google(audio, language="ru-RU")


t = get_text_from_speech()  # get text from microphone
speech = get_speech_from_text(t)  # get speech from text -> BytesIO
play_speech(speech)  # play speech


# DELETE ./Temp files
files = glob.glob(f'{os.environ["TEMP"]}/*')
for f in files:
    os.remove(f)

