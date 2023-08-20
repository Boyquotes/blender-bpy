
def delete_object(name):
    # try to find the object by name
    if name in bpy.data.objects:
        # if it exists, select it and delete it
        obj = bpy.data.objects[name]
        obj.select_set(True)
        bpy.ops.object.delete(use_global=False)


delete_object("Sun")
for n in range(N_PLANETS):
    delete_object("Planet-{:02d}".format(n))
    delete_object("Radius-{:02d}".format(n))
for m in bpy.data.materials:
    bpy.data.materials.remove(m)
