import json
from pathlib import Path
import subprocess

from ffmpeg_dependency import ensure_ffmpeg_installed

# Path to the folder that this code will look in to find audio files
audioSourcePath = Path(r"C:\Users\nick.vernon\OneDrive - RoviSys\Documents\Programming\Mp3SampleRateConverter\Audio_Files")
# Path to the folder that this code will dump new audio files to
audioDumpPath = Path(r"C:\Users\nick.vernon\OneDrive - RoviSys\Documents\Programming\Mp3SampleRateConverter\Dump_Folder")
# Desired samplerate for your audio files
samplerateGoal = 44100


def loopAllFiles() -> None:
    # Loop through all mp3 files in source folder and check sample rate
    audioPaths = audioSourcePath.rglob("*.mp3")

    count = 0
    for path in audioPaths:
        count += 1
        if hasSampleRateGoal(path):
            print(f"{path} has the correct sample rate")
        else:
            print(f"{path} has the wrong sample rate")
        break
    print(f"Processed {count} file(s)")


def hasSampleRateGoal(audio_path: Path) -> bool:
    output = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=sample_rate",
            "-of",
            "json",
            str(audio_path),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if output.returncode != 0:
        print(f"ffprobe failed for {audio_path}: {output.stderr.strip()}")
        return False

    data = json.loads(output.stdout)
    streams = data.get("streams", [])
    if not streams:
        return False

    sample_rate = int(streams[0].get("sample_rate", 0))
    print(sample_rate)
    return sample_rate == samplerateGoal


#def modifySamplerate():
#    # Function that modifies the sample rate of an audio file

#def saveToFolder():
#    # Takes an audio file that has the correct samplerate and simply saves a copy to the new folder

if __name__ == "__main__":
    ffmpeg_path = ensure_ffmpeg_installed()
    print(f"Using FFmpeg at: {ffmpeg_path}")
    loopAllFiles()
