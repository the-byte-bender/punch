from cytolk import tolk
tolk.try_sapi(True)
tolk.load("__compiled__" not in globals())  # For compatibility with nuitka
def speak(text: str, interupt = True):
    """Speak [text]. [interupt] specifies whether any currently spoken text should be interupted"""
    tolk.output(text, interupt)