import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["sys", "pygame", "pygame.midi"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Pypad",
        version = "0.1",
        description = "A free music maker",
        options = {"build_exe": build_exe_options},
        executables = [Executable("pypad.py", base=base)])
