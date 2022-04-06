from MusiCore.Stream import FromWave
from MusiCore.Player.Sound import Sound
from MusiCore import Path

class Playlist():

    def __init__(self, path: str) -> None:
        if path.endswith('/'):
            path = path[:-1]
        self.path: Path = Path(path)

        self.sounds = [Sound(name=filename, path=f"{self.path.path}/{filename}", stream=FromWave(f"{self.path.path}/{filename}")) for filename in self.path.glob(['.wav', '.mp3'])]
        print(self.sounds)

    