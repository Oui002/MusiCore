import MusiCore

import pynput
from asyncio import run

chunk_size = 8192
queue_size = 20

async def on_press(key):
    if key == pynput.keyboard.Key.pause:
        player.toggle_pause()
    
    elif key == pynput.keyboard.Key.esc:
        player.quit()

    elif key == pynput.keyboard.Key.f7:
        player.offset_pos(5)
    elif key == pynput.keyboard.Key.f6:
        player.offset_pos(-5)

    elif key == pynput.keyboard.Key.f3:
        player.increase_volume(by=player.max_vol_boost / 10)
    elif key == pynput.keyboard.Key.f2:
        player.increase_volume(by=-player.max_vol_boost / 10)

def run_on_press(key):
    run(on_press(key))

if __name__ == '__main__':
    sound = MusiCore.Sound(name="Pastel Rain - Sangatsu no Phantasia", 
    path='../music/Pastel Rain - Sangatsu no Phantasia.wav', 
    stream=MusiCore.Stream.FromWave('../music/Pastel Rain - Sangatsu no Phantasia.wav'))
    
    player = MusiCore.SoundPlayer(sound, chunk_size=chunk_size, queue_size=queue_size, max_vol_boost=100)
    player.play(blocking=False) 

    with pynput.keyboard.Listener(
        on_press=run_on_press
    ) as listener:
        listener.join()
