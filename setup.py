import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MusiCore-Oui002",
    version="0.0.6.3.8",
    author="https://github.com/Oui002",
    description="Module for playing wave files in buffers. Also has a basic music player functions like playlists and stuff like that :)) ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Oui002/MusiCore",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    packages=["MusiCore", "MusiCore/Player", "MusiCore/Playlist", "MusiCore/Stream"],
    python_requires=">=3.6",
)