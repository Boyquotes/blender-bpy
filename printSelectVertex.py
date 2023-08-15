import bpy, bmesh
from easybpy import *

#obj = bpy.data.objects['Cube']
obj = bpy.context.active_object
mesh = obj.data
if obj and obj.type == 'MESH':
    uv_layer = mesh.uv_layers.active.data
matrix = obj.matrix_world

def centre(points):
    return min(points) + (max(points) - min(points))/2

def selectPointsUnder(obj, height):
    if obj and obj.type == 'MESH':
        verts = mesh.vertices
        for v in verts:
            print("v2")
            print(v)
            print(v.co.x)
            print(v.co.y)
            print(v.co.z)
            if v.co[2] < height:
                v.select = True
        selection = get_selected_vertices(obj)
    return selection

def selectPointsOver(obj, height):
    if obj and obj.type == 'MESH':
        verts = mesh.vertices
        for v in verts:
            print("v2")
            print(v)
            print(v.co.x)
            print(v.co.y)
            print(v.co.z)
            if v.co[2] > height:
                v.select = True
        selection = get_selected_vertices(obj)
    return selection

print(obj.matrix_world.to_translation())
print(obj.matrix_world.to_euler('XYZ'))
#Euler((0.0, -0.0, 0.0), 'XYZ')
print(obj.matrix_world.to_quaternion())

coords = [(obj.matrix_world @ v.co) for v in obj.data.vertices]
print(coords)

print(obj.location)
print(obj.rotation_euler)
print(obj.scale)

if obj.mode == 'EDIT':
    # this works only in edit mode,
    bm = bmesh.from_edit_mesh(obj.data)
    verts = [vert.co for vert in bm.verts]
    vcount = len(verts)
    print("vcount")
    print(vcount)
    for vert in bm.verts:
        print(vert.co)
else:
    # this works only in object mode,
    verts = [vert.co for vert in obj.data.vertices]
    vcount = len(verts)
    print("vcount")
    print(vcount)
    for vert in verts:
        print(vert.x)
        print(vert.y)
        print(vert.z)

# coordinates as tuples
plain_verts = [vert.to_tuple() for vert in verts]
print(plain_verts)

#for poly in mesh.polygons:
#    print("Polygon index: %d, length: %d" % (poly.index, poly.loop_total))
#    for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
#        print("    Vertex: %d" % mesh.loops[loop_index].vertex_index)
#        print("    UV: %r" % uv_layer[loop_index].uv)
        
if obj and obj.type == 'MESH':
    verts = mesh.vertices
#    bpy.ops.object.mode_set(mode='EDIT')
#    bpy.ops.mesh.select_all(action='DESELECT')
#    bpy.ops.object.editmode_toggle()
    for v in verts:
        print("v111")
        print(v)
        print(v.co.x)
        print(v.co.y)
        print(v.co.z)
        print(v.co[0])
        print(v.co[1])
        print(v.co[2])
#        selection = selectPointsUnder(obj, 0.01)
        selection = selectPointsOver(obj, 0.01)
#        if v.co.z < 0.01:
#            v.select = True

#    selection = get_selected_vertices(obj)
#    print(selection)
    if selection:
        bpy.ops.object.mode_set(mode='EDIT')

#        print(mesh.vertices[0].co.z)
#        loc = matrix @ v
#        print(loc)
#        dir(v)
#        v.select = True
#        for element in v:
#            print(element)
#    bpy.ops.object.editmode_toggle()
