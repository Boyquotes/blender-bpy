import bpy
from bpy import context
# add a cube
bpy.ops.mesh.primitive_cube_add()
ob = context.active_object
me = ob.data
# add two array modifiers
count = 32
arrays = {"x": (1.5, 0, 0),
          "y": (0, 1.5, 0)}

for axis, displace in arrays.items():          
    mod = ob.modifiers.new(axis, 'ARRAY')
    mod.count = count
    mod.relative_offset_displace = displace
    bpy.ops.object.modifier_apply(modifier=mod.name)

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i+n]

material_index = 0
for cube in chunks(me.polygons, 6):
    mat = bpy.data.materials.new("Mat%d" % material_index)

    mat.diffuse_color[0] = material_index / 100
    me.materials.append(mat)
    for f in cube:

        f.material_index = material_index
    material_index += 1
