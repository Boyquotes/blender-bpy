https://blender.stackexchange.com/questions/230677/export-collection-and-set-fbx-file-name-as-collection-name

import bpy

C = bpy.context

# Get all mesh objects of the active collection
mesh_objects = [o for o in C.collection.objects if o.type == 'MESH']

# If mesh objects list is not empty
if mesh_objects and C.mode == 'OBJECT':
    
    # Duplicate all mesh objects and get their references
    bpy.ops.object.duplicate({'selected_objects' : mesh_objects})
    mesh_dupes = C.selected_objects
    
    # Set one object of the dupes to the active object 
    C.view_layer.objects.active = mesh_dupes[0]
    # Switch into Edit Mode
    bpy.ops.object.mode_set(mode='EDIT')
    # Select all vertices
    bpy.ops.mesh.select_all(action='SELECT')
    # Convert to tris
    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')
    # Switch back to Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Export the modified objects to FBX
    bpy.ops.export_scene.fbx(
        filepath=bpy.path.abspath("//{}.fbx".format(C.collection.name)),
        use_selection=True)
    
    # Delete all duplicates
    bpy.ops.object.delete({"selected_objects" : mesh_dupes})
