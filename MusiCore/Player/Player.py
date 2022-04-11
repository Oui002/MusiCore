from numpy import clip
from MusiCore.Stream.Stream import FromWave

from sounddevice import OutputStream, CallbackAbort, CallbackStop, sleep
from queue import Queue

import threading
import time

class StreamPlayer():
    
    def __init__(self, stream: FromWave, chunk_size: int, queue_size: int, max_vol_boost: int = 100):
        self.wave_stream = stream

        self.volume = 100
        self.max_vol_boost = max_vol_boost

        self.paused = False
        self.queue_size = queue_size
        self.chunk_size = chunk_size # / (self.wave_stream.params.sampwidth + self.wave_stream.params.nchannels)

        self.cc = False

        self.output_stream = OutputStream(
            samplerate=self.wave_stream.params.framerate,
            blocksize=int(self.chunk_size * self.wave_stream.params.nchannels),
            channels=self.wave_stream.params.nchannels,
            dtype="int16",
            callback=self.callback,
            finished_callback=self.finished_callback
            )

        self.queue = Queue(self.queue_size)
        self.init_queue()

    def increase_volume(self, by: int):
        volume = self.volume + by
        
        if volume > self.max_vol_boost:
            volume = self.max_vol_boost
        elif volume < 0:
            volume = 0

        self.volume = volume
        
    def play(self, blocking: bool = False):
        self.output_stream.start()
        self.paused = False

        if blocking:
            sleep(self.wave_stream.wro_duration * 1000)

    def toggle_pause(self):
        self.paused = True
        if not self.output_stream.stopped:
            self.paused_timestamp = self.wave_stream.tell_pos() - self.chunk_size * self.queue_size
            self.output_stream.stop(ignore_errors=True)
            return

        self.play(blocking=False)
        self.paused = False

    def offset_pos(self, seconds: float):
        if self.cc: return

        pos_in_frames = int((self.wave_stream.tell_pos() - self.chunk_size * self.queue_size) + seconds * self.wave_stream.params.framerate)
        if pos_in_frames <= 0:
            pos_in_frames = 0

        if self.wave_stream.setpos(pos_in_frames) == "EOF":
            self.finished_callback()

        self.queue = Queue(maxsize=self.queue_size)
        self.init_queue()

        threading.Thread(target=self.run_cc).start()

        self.play()
    
    def pos(self) -> float:
        return ((self.wave_stream.tell_pos() - self.chunk_size * self.queue_size) / 100000) * 2

    def init_queue(self):
        for i in range(self.queue_size):
            self.queue.put_nowait(self.wave_stream.buffer_as_np_int16(self.chunk_size))

    def callback(self, outdata, frames: int, time, status=None):
        if status.output_underflow:
            print('Output underflow')
            raise CallbackAbort
        assert not status

        try:
            out = clip((self.queue.get_nowait() / 100 * self.volume), -25000, 25000)
        except:
            return
        
        if len(out) < len(outdata):
            outdata[:len(out)] = out
            outdata[len(out):].fill(0)
            raise CallbackStop
        else:
            outdata[:] = out
            self.queue.put_nowait(self.wave_stream.buffer_as_np_int16(self.chunk_size))
    
    def finished_callback(self):
        if not self.paused:
            self.quit()

    def run_cc(self, duration: float = 0.05):
        self.cc = True
        time.sleep(duration)
        self.cc = False

    def quit(self):
        self.queue = Queue()
        self.output_stream.abort()
        self.wave_stream.release()
        quit()
