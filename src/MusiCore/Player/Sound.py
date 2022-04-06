from MusiCore.Stream import FromWave
from dataclasses import dataclass

@dataclass()
class Sound():
    name: str
    path: str
    stream: FromWave