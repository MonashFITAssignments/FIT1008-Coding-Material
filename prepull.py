import subprocess
import sys

if __name__ == '__main__':
    subprocess.run([
        sys.executable, #python or python3
        "-m",
        "flake8", 
        # "--count", 
        "--select=E9,F63,F7,F82", 
        "--show-source", 
        "--statistics",
    ]).returncode or subprocess.run([
        sys.executable, 
        "-m",
        "unittest",
    ])

