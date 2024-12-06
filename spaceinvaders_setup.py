import sys

from cx_Freeze import *

includefiles = ['icon.ico']
base = None
if sys.platform == "win32":
    base = "win32GUI"

shortcuttable = [
    ("DesktopShortcut",  # shortcut
     "DesktopFolder",
     "Space Invaders",
     "TARGETDIR",
     "[TARGETDIR]\main.exe",
     None,
     None,
     None,
     None,
     None,
     None,
     "TARGETDIR",
     )
]
msi_data = {"Shortcut": shortcuttable}

bdist_msi_options = {'data': msi_data}

setup(
    version="0.1",
    description="Space Invaders",
    author="Darshan Solanki",
    name="Space Invaders",
    options={'build_exe': {'include_files': includefiles}, "bdist_msi": bdist_msi_options, },
    executables=[
        Executable(
            script="main.py",
            base=base,
            icon='icon.ico',
        )
    ]
)
