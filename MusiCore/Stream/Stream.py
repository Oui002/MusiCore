import wave
import numpy

class FromWave():
    
    def __init__(self, wro) -> None:
        if isinstance(wro, wave.Wave_read):
            self.wro = wro
        else:
            self.wro = wave.open(wro, 'rb')

        self.params = self.wro.getparams()
        self.wro_duration = int(self.params.nframes / self.params.framerate)
    
    def read_buffer(self, buffersize: int) -> bytes:
        audio = self.wro.readframes(int(buffersize * self.params.nchannels))
        return audio
    
    def buffer_as_np_int16(self, buffersize: int):
        buffer = self.read_buffer(buffersize)
        audio = numpy.repeat(numpy.frombuffer(buffer, dtype=numpy.int16).reshape(int(len(buffer) / 2 / self.params.nchannels), self.params.nchannels), 1, axis=1)

        return audio

    def rewind(self) -> None:
        return self.wro.rewind()

    def setpos(self, position: int) -> str:
        try:
            return self.wro.setpos(position)
        except wave.Error:
            return 'EOF'

    def tell_pos(self) -> int:
        return self.wro.tell()

    def release(self):
        self.wro.close()