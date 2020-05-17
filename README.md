# About DPS Converter

This is a tool currently designed to simply take a donjon TSV file and convert it into a Dungeon Painter Studio file.

I may end up doing some dungeon generation with it natively at some point, but for now this works.

# setup

Setup a python3 venv

```
python3 -m venv venv
```

Activate the venv (windows)

```
.\venv\Scripts\activate.bat
```

install the package into the venv

```
pip install -e .
```

run the tool

```
dps-converter INPUT OUTPUT
```

where INPUT is a donjon format TSV map file and OUTPUT is the name of a .dps file you want to create.

You need to have the FA dungeon tilesets loaded for it to work; you could use something else but it's currently specific to that tileset.