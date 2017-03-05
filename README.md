Villager-Sim
============

A project we have been working on for a while. The end goal is to create a
civilization that can grow and explore on it's own though artificial intelligence
by setting goals for itself, learning what it needs to do to accomplish those goals.

Start
-----

To run this you must Install PyGame - http://www.pygame.org/download.shtml

Start with ```python UpdatingVillagerSim.py```

Additional start flags:

```python UpdatingVillagerSim.py [fullscreen] [world size] [hard shadow]```

```fullscreen``` is a boolean value (0 / 1) that controls if the game will start fullscreen or not. WARNING: If running on linux, if the program crashes while in fullscreen mode it is difficult to close.

```world size``` is an integer (preferably an order of magnitude of 2) that controls the dimensions of the tile map of the game world. The game world is a square so you only need to supply the value of one side (e.g. 64).

```hard shadow``` is a boolean value (0 / 1) that controls if the shadow from elevation is rendered on the game world or just the minimap.

Note, you cannot just select ```hard shadow``` without the other two, nor ```world size``` without ```fullscreen```.

Licence
-------

GNU GENERAL PUBLIC LICENSE Version 2
