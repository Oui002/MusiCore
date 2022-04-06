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
        return self.wro.readframes(int(buffersize))
    
    def buffer_as_np_int16(self, buffersize: int):
        return numpy.repeat(numpy.frombuffer(self.read_buffer(buffersize), dtype=numpy.int16).reshape(int(buffersize), self.params.nchannels), 1, axis=1)
    
    def rewind(self) -> None:
        return self.wro.rewind()

    def setpos(self, position: int) -> None:
        return self.wro.setpos(position)

    def tell_pos(self) -> int:
        return self.wro.tell()

    def release(self):
        self.wro.close()