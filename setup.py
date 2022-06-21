from cx_Freeze import setup, Executable
import sys

setup(
    name="PCC Classes Program",
    version="0.1",
    description="Philippine Coding Camp Classes Program",
    options={
        "build_exe": {
            "packages":["os"],
            "excludes":["tkinter", "./cfg/.gitignore", "./cfg/rc.cfg"],
            "includes":[
                "PyQt5",
                "sqlalchemy",
                "sqlalchemy.sql.default_comparator",
                "sqlalchemy.dialects.sqlite"
            ],
            "include_files":[
                ("./cfg/app.cfg", "./cfg/app.cfg"),
                ("./logs/app.log", "./logs/app.log")
            ],
            "optimize": 2
        }
    },
    executables=[
        Executable(
            script="main.py",
            target_name="pcc.exe",
            base="Win32GUI" if sys.platform == "win32" else None,
            icon="img/app_icon.ico"
        )
    ]
)