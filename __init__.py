import platform
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

