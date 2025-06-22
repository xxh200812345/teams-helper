from cx_Freeze import setup, Executable

setup(
    name="TeamsRealTimeTranslator",
    version="1.0",
    description="Real-time subtitle translator for Microsoft Teams using ChatGPT",
    executables=[Executable("main.py")],
    options={
        "build_exe": {
            "include_files": ["settings.yaml"],
        }
    }
)
