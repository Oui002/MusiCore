import MusiCore

import wave
import pynput
from asyncio import run
from sys import exit

chunk_size = 8192
queue_size = 10

async def on_press(key):
    if key == pynput.keyboard.Key.pause:
        player.toggle_pause()
    
    elif key == pynput.keyboard.Key.esc:
        player.quit()
        exit()

    elif key == pynput.keyboard.Key.f7:
        player.offset_pos(5)
    elif key == pynput.keyboard.Key.f6:
        player.offset_pos(-5)

    elif key == pynput.keyboard.Key.f3:
        print("Hi")
        player.increase_volume(by=player.max_vol_boost / 10)
    elif key == pynput.keyboard.Key.f2:
        print("Hi")
        player.increase_volume(by=-player.max_vol_boost / 10)

def run_on_press(key):
    run(on_press(key))

if __name__ == '__main__':
    player = MusiCore.StreamPlayer(MusiCore.Stream.FromWave(wave.open('../music/4.wav', 'rb')), chunk_size=chunk_size, queue_size=queue_size)
    player.play(blocking=False)

    with pynput.keyboard.Listener(
        on_press=run_on_press
    ) as listener:
        listener.join()
