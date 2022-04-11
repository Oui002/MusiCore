from MusiCore.Stream.Stream import FromWave
from dataclasses import dataclass

@dataclass()
class _Sound():
    name: str
    path: str
    stream: FromWave

class Sound():

    def __init__(self) -> None:
        pass