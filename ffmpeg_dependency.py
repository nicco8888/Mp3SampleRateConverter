import os
import platform
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

FFMPEG_WINDOWS_ZIP_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
TOOLS_PATH = Path(__file__).resolve().parent / ".tools"
FFMPEG_INSTALL_PATH = TOOLS_PATH / "ffmpeg"


def _find_ffmpeg_exe(search_root: Path) -> Path | None:
    """Locate ffmpeg.exe inside an extracted FFmpeg folder tree."""
    if not search_root.exists():
        return None

    for candidate in search_root.rglob("ffmpeg.exe"):
        if candidate.name.lower() == "ffmpeg.exe":
            return candidate
    return None


def _add_binary_folder_to_path(binary_path: Path) -> None:
    """Add the ffmpeg binary folder to the current process PATH."""
    os.environ["PATH"] = f"{binary_path.parent}{os.pathsep}" + os.environ.get("PATH", "")


def ensure_ffmpeg_installed() -> Path:
    """Use system FFmpeg if available; otherwise use/download a local Windows copy."""
    existing = shutil.which("ffmpeg")
    if existing:
        return Path(existing)

    # Reuse a prior local install before downloading again.
    local_ffmpeg = _find_ffmpeg_exe(FFMPEG_INSTALL_PATH)
    if local_ffmpeg is not None:
        _add_binary_folder_to_path(local_ffmpeg)
        return local_ffmpeg

    if platform.system() != "Windows":
        raise RuntimeError("FFmpeg is not installed. Install it and ensure `ffmpeg` is on PATH.")

    TOOLS_PATH.mkdir(parents=True, exist_ok=True)
    FFMPEG_INSTALL_PATH.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        zip_path = Path(tmp_dir) / "ffmpeg.zip"
        print("FFmpeg not found. Downloading FFmpeg for Windows...")
        urllib.request.urlretrieve(FFMPEG_WINDOWS_ZIP_URL, zip_path)
        with zipfile.ZipFile(zip_path, "r") as archive:
            archive.extractall(FFMPEG_INSTALL_PATH)

    ffmpeg_exe = _find_ffmpeg_exe(FFMPEG_INSTALL_PATH)
    if ffmpeg_exe is None:
        raise RuntimeError("FFmpeg download completed, but ffmpeg.exe was not found.")

    _add_binary_folder_to_path(ffmpeg_exe)
    return ffmpeg_exe
