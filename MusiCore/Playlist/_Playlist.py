import os

class Path():

    def __init__(self, path: str) -> None:
        if not os.path.isdir(path): raise Exception("The path passed to MusiCore.PlayList.Path isn't a directory.")
        self.__path__ = path

    def glob(self, include: list):
        if not isinstance(include, list):
            include = [include]

        ucl = [filename for filename in os.listdir(self.path)]
        ulwe = list()
        cl = list()

        for filename in ucl:
            if os.path.isdir(f"{self.path}/{filename}"): pass
            
            for e in include:
                if filename.endswith(e):
                    fnwe = filename[:-len(e)]

                    if fnwe in ulwe:
                        print(f"Skipping double file name: {fnwe}")
                    else:
                        cl.append(filename)
                        ulwe.append(fnwe)
        
        return cl


from MusiCore.Stream.Stream import FromWave
from MusiCore.Player.Sound import _Sound

class Playlist():

    def __init__(self, path: str) -> None:
        if path.endswith('/'):
            path = path[:-1]
        self.path: Path = Path(path)

        self.sounds = [_Sound(name=filename, path=f"{self.path.__path__}/{filename}", stream=FromWave(f"{self.path.__path__}/{filename}")) for filename in self.path.glob(['.wav'])]

    def get(self, index: int) -> _Sound:
        if index > self.sounds.__len__(): return None
        elif index < 0: index = 0

        return self.sounds[index] if isinstance(self.sounds[index], _Sound) else None 