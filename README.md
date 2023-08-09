Launch script in blender console :  
```
myModule = bpy.data.texts[0].as_module()
```
```
myModule = bpy.data.texts['JSON'].as_module()
```

Call function :
```
myModule = bpy.data.texts['JSON'].as_module().open_json()
```

Launch in command line
```
blender --background --python export-layer.py
```
