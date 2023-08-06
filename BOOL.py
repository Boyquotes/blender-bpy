import bpy

context = bpy.context

#Small Cube
bpy.ops.mesh.primitive_cube_add(size=1, location=(3, -1, 0))
small_cube = context.object

#Large Cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(3, 0, 0))
large_cube = context.object

mod = large_cube.modifiers.new("Boolean", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = small_cube

# large cube has context.
bpy.ops.object.modifier_apply(modifier=mod.name)

#bpy.context.scene.objects.unlink(small_cube)
bpy.data.objects.remove(small_cube)

#Small Cube
bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.5, location=(0, 0, -0.25))
sphere = context.object

#Large Cube
bpy.ops.mesh.primitive_plane_add(size=2, location=(0, 0, 0))
large_plane = context.object

mod = large_plane.modifiers.new("Boolean", type='BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = sphere

# large cube has context.
bpy.ops.object.modifier_apply(modifier=mod.name)

#bpy.context.scene.objects.unlink(small_cube)
bpy.data.objects.remove(sphere)
