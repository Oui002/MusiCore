from MusiCore.Stream import FromWave

from sounddevice import OutputStream, CallbackAbort, CallbackStop, sleep
from queue import Queue

class StreamPlayer():
    
    def __init__(self, stream: FromWave, chunk_size: int, queue_size: int):
        self.wave_stream = stream

        self.queue_size = queue_size
        self.chunk_size = chunk_size / (self.wave_stream.params.sampwidth + self.wave_stream.params.nchannels)

        self.output_stream = OutputStream(
            samplerate=self.wave_stream.params.framerate,
            blocksize=int(self.chunk_size),
            channels=self.wave_stream.params.nchannels,
            dtype="int16",
            callback=self.callback,
            finished_callback=self.finished_callback
            )

        self.queue = Queue(self.queue_size)
        self.init_queue()

    def play(self, blocking: bool = False):
        self.output_stream.start()

        if blocking:
            sleep(self.wave_stream.wro_duration * 1000)

    def toggle_pause(self):
        self.paused = True

        if not self.output_stream.stopped:
            self.paused_timestamp = self.wave_stream.tell_pos() - self.chunk_size * self.queue_size
            self.output_stream.stop(ignore_errors=True)
            return

        self.output_stream.start()
        self.paused = True
        # timestamp in seconds print(((self.wave_stream.tell_pos() - self.chunk_size * self.queue_size) / 100000) * 2)

    def init_queue(self):
        for i in range(self.queue_size):
            self.queue.put_nowait(self.wave_stream.buffer_as_np_int16(self.chunk_size))

    def callback(self, outdata, frames: int, time, status=None):
        if status.output_underflow:
            print('Output underflow')
            raise CallbackAbort
        assert not status

        try:
            out = self.queue.get_nowait()
        except self.queue.Empty as e:
            print("Buffer queue is empty")
            raise CallbackAbort from e
        
        if len(out) < len(outdata):
            outdata[:len(out)] = out
            outdata[len(out):].fill(0)
            raise CallbackStop
        else:
            outdata[:] = out
            self.queue.put_nowait(self.wave_stream.buffer_as_np_int16(self.chunk_size))
    
    def finished_callback(self):
        if not self.paused:
            self.wave_stream.release()
