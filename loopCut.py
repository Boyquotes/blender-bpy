import bpy
import bmesh
import math
import mathutils

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0))

def bmesh_loopcut(bm,face_list,direction_axis,center='auto'):
    for f in bm.faces:
        f.select = False
    bm.faces.ensure_lookup_table()  
    for f in face_list:
        bm.faces[f].select = True

    edges = [e for e in bm.edges if e.select == True]
    faces = [f for f in bm.faces if f.select == True]
    
    if center=='auto':    
        weights = [f.calc_area() for f in faces]
        weighted_centres = [f.calc_area() * f.calc_center_median() for f in faces]
        cutting_point = sum(weighted_centres, mathutils.Vector()) / sum(weights)
    else:
        cutting_point = bpy.context.scene.cursor.location
    geom = []
    geom.extend(edges)
    geom.extend(faces) 

    result = bmesh.ops.bisect_plane(bm,dist=0.01,geom=geom,plane_co=cutting_point,plane_no=direction_axis)



# Make a new BMesh
bm = bmesh.new()

obj = bpy.context.object

ob = obj
me = ob.data 
bm = bmesh.new() 
bm.from_mesh(me)


face_cut=([0])
bmesh_loopcut(bm,face_cut,[1,0,0])
    
bm.to_mesh(me)
bm.free()
me.update()
