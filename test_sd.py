try:
    print("Importing sounddevice...")
    import sounddevice
    print("sounddevice imported.")
except Exception:
    import traceback
    traceback.print_exc()
