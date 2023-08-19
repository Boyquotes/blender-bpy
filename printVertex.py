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


def print_vert_details(selected_verts):
    num_verts = len(selected_verts)                     # how many verts are selected?
    print("number of verts: {}".format(num_verts))  
    
    vert_indices = [id.index for id in selected_verts]  # list of indices for every selected vertex
    print("vert indices: {}".format(vert_indices))


    # for every selected vertex, execute this
    for item in vert_indices:

######## This is where I need help #########

        # Finding vertex's coord Vector

        # n = bpy.ops.transform.rotation_normal()
        # bpy.ops.mesh.normals_tools(mode='COPY')
        # print(bpy.ops.mesh.normals_tools())

######################################

        print("Vector Normal: ")


        v = obj.data.vertices[item]                    # which vertex? Using index nr
        co_final = obj.matrix_world @ v.co      # co_final is the global location of the vertex
        print("Vector: ")
        print(co_final)
        x_offset = co_final.x      # taking only X value from vector
        print(x_offset)


def get_vertex_data(current_obj):
    bpy.ops.object.mode_set(mode='EDIT')
    bm = bmesh.from_edit_mesh(current_obj.data)
    selected_verts = [vert for vert in bm.verts if vert.select]
    print_vert_details(selected_verts)

def polygonsInfo():
    p = obj.data.polygons[0]
    print(p)
    print(p.select) #Indicates if the face is selected
    print(p.normal) #The face normal
    print(p.vertices) #The vertices indexes
    vIndex = p.vertices[0]
    print(vIndex)
    v=obj.data.vertices[vIndex]
    print(v)
    print(v.co)


def infoVertex():
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
#            print(v.co.x)
#            print(v.co.y)
#            print(v.co.z)
#            print(v.co[0])
#            print(v.co[1])
#            print(v.co[2])
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
print("vertex info")
#infoVertex()

print("infos")
#polygonsInfo()

print("vertex_data")
get_vertex_data(obj)
