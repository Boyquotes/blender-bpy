 print(bpy.data.texts[1].name)  

name="easyPBI"
bpy.data.texts[name]
bpy.data.texts[name].clear()  

name = "metarig.py"

if name in bpy.data.texts:
    text_block = bpy.data.texts[name]
    text_block.clear()
else:
    text_block = bpy.data.texts.new(name)

===
import bpy
from pathlib import Path
for text in bpy.data.texts:
    # internal
    if text.is_in_memory:
        print(text.is_in_memory)
        print(Path(bpy.path.abspath(text.filepath)))
        continue
    path = Path(bpy.path.abspath(text.filepath))
    print(path)

