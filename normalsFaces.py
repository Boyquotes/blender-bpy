import bpy
import bmesh
import mathutils

# Get the active mesh (assumes starting in edit mode)
obj = bpy.context.edit_object
me = obj.data
coneradius=1     # Im not sure how you plan to scale the cone.
Up=mathutils.Vector((0,0,1))

# Get a BMesh representation
bm = bmesh.from_edit_mesh(me)
selected_faces=[face for face in bm.faces if face.select]
if len(selected_faces)>0:
    norm=selected_faces[0].normal
    print("norm")
    print(norm)
    my_location=selected_faces[0].calc_center_median()
    print(my_location)
    # convert this to a rotation quaternion    
    Qrot=norm.rotation_difference(Up)

    #Add the cone in object mode
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_cone_add(location=my_location)
    cone=bpy.context.object
    cone.rotation_mode='QUATERNION'
    cone.rotation_quaternion*=Qrot.inverted()
