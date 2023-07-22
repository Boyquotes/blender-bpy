    if "Terrain" not in inputs:
        inputs.new("NodeSocketObject", "Terrain")
        bpy.context.active_object.data.update()
    if "Object" not in inputs:
        inputs.new("NodeSocketObject", "Object")
        bpy.context.active_object.data.update()
    if "Collection" not in inputs:
        inputs.new("NodeSocketCollection", "Collection")
        bpy.context.active_object.data.update()
