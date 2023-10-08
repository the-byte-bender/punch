import os
import cyal
import pyogg


class Pool:
    """A pool of cyal buffers from a sound folder. This pool caches any buffer on first request and returns the same buffer for subsequent requests. Only works with ogg vorbis files"""

    def __init__(self, context: cyal.Context, base_sound_path: str = "sounds/"):
        if not os.path.isdir(base_sound_path):
            raise ValueError(f"{base_sound_path} is not a directory")
        self.context = context
        self.base_sound_path = base_sound_path
        if not self.base_sound_path.endswith("/"):
            self.base_sound_path += "/"
        self.cache = {}

    def get(self, file: str) -> cyal.Buffer:
        """Returns a buffer for that file's audio content. The buffer is either retrieved from cache, or first loaded from the file if its not already cached"""
        if file not in self.cache:
            self.cache[file] = self.get_buffer_from_file(file)
        return self.cache[file]

    def get_buffer_from_file(self, file: str) -> cyal.Buffer:
        """create a new buffer with that file's audio content. Always creates a new buffer and loads the file from disk every time. File is relative to [self.base_sound_path]"""
        file = self.base_sound_path + file
        temp = pyogg.VorbisFile(file)
        format = (
            cyal.BufferFormat.MONO16
            if temp.channels == 1
            else cyal.BufferFormat.STEREO16
        )
        buffer = self.context.gen_buffer()
        buffer.set_data(temp.buffer, sample_rate=temp.frequency, format=format)
        return buffer

    def clear(self):
        self.cache.clear()