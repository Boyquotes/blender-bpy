def myremovedoubles(objectname, mergedist):
    obj = None
    try:
        obj = bpy.data.objects[objectname]
    except ( RuntimeError ):
        pass  
    if (obj != None): 
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[objectname].select = True            
            scene.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.remove_doubles(mergedist=mergedist)
            bpy.ops.object.mode_set(mode='OBJECT')
            return True
        except ( RuntimeError ):
            pass  
    return False 
