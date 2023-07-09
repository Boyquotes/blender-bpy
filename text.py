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

