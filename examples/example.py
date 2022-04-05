import MusiCore

import wave
import pynput

chunk_size = 8192
queue_size=40

def on_press(key):
    if key == pynput.keyboard.Key.pause:
        player.toggle_pause()

if __name__ == '__main__':
    player = MusiCore.StreamPlayer(MusiCore.Stream.FromWave(wave.open('../music/2.wav', 'rb')), chunk_size=chunk_size, queue_size=queue_size)
    player.play(blocking=False)

    with pynput.keyboard.Listener(
        on_press=on_press
    ) as listener:
        listener.join()
