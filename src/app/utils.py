import os
import platform
import stat
import subprocess
import sys
from pathlib import Path


def get_binary_path(binary_name):
    """
    Get the absolute path to a binary file, considering PyInstaller packaging.

    Args:
        binary_name (str): Name of the binary file.

    Returns:
        str: Absolute path to the binary file.
    """
    if hasattr(sys, "_MEIPASS"):
        # Running from PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running from source
        base_path = str(Path(__file__).parents[2])

    cpu = "arm" if "arm" in platform.machine().lower() else "amd"
    system = platform.system().lower()
    postfix = ".exe" if cpu == "amd" and system == "windows" else ""

    return os.path.join(
        base_path,
        "binaries",
        f"{binary_name}-{system}-{cpu}64{postfix}",
    )


def make_executable(file_path):
    """
    Ensure a file has executable permissions.

    Args:
        file_path (str): Path to the binary file.
    """
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC)


def run_binary(binary_name, *args):
    """
    Run a binary file with subprocess after ensuring it is executable.

    Args:
        binary_name (str): Name of the binary file.
        args (list): List of arguments to pass to the binary.
    """
    binary_path = get_binary_path(binary_name)

    # Ensure the binary is executable
    make_executable(binary_path)

    # Run the binary using subprocess
    result = subprocess.run(
        (binary_path,) + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    return result.stdout.decode(), result.stderr.decode()
