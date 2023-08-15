import bpy
from easybpy import *
obj = bpy.data.objects['Cube']

def deleteVertex(obj):
    if get_mode() == "OBJECT":
        set_edit_mode()
        bpy.ops.mesh.select_all(action='DESELECT')
    else:
        bpy.ops.mesh.select_all(action='DESELECT')

    mesh = obj.data
    matrix = obj.matrix_world
    verts = obj.data.vertices

    set_object_mode()
    print(get_mode())
    for v in verts:
        print(v.co[2])
#        if v.co.z
        if v.co[2] < 0.01:
#            print('yes')
#            print(v.co[0])
#            print(v.co[1])
#            print(v.co[2])
            v.select = True
#           print(mesh.vertices[0].co.z)
        
    selection = get_selected_vertices(obj)
#    print(selection)
    if selection:
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.delete(type='VERT')
    set_object_mode()
    
deleteVertex(obj)
