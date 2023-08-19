import bpy
import bmesh
context = bpy.context

obj = context.edit_object
me = obj.data
bm = bmesh.from_edit_mesh(me)
bm.select_mode = {'VERT'}
for v in bm.verts:
    v.select = ( v.co.x > 0 )
bm.select_flush_mode()   
me.update()
