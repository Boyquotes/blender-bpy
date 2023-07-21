"""
See YouTube tutorial here: https://www.youtube.com/watch?v=SHfiscO6AzY
"""
import random
import time
import bpy
import json
import math
import os
import random
import queue
from easybpy import *
import add_curve_sapling

execution_queue = queue.Queue()

DIRECTORY='~/blender/bpy/'

arrangeNode = bpy.data.texts["contexte"].as_module()

def exportFbxByName(objName):
    select_object(objName)
    directory = os.path.dirname(bpy.data.filepath)
    filepath = os.path.join(directory+'/exports', objName + ".fbx")
    bpy.ops.export_scene.fbx(filepath=filepath, use_selection=True)

def importFbx(objName, renameObj = ''):
    directory = os.path.dirname(bpy.data.filepath)
    filepath = os.path.join(directory+'/exports', objName + ".fbx")
    print(filepath)
    bpy.ops.import_scene.fbx(filepath=filepath)
    if renameObj:
        bpy.context.active_object.name = renameObj

################################################################
# helper functions BEGIN
################################################################

def purge_orphans():
    """
    Remove all orphan data blocks

    see this from more info:
    https://youtu.be/3rNqVPtbhzc?t=149
    """
    if bpy.app.version >= (3, 0, 0):
        # run this only for Blender versions 3.0 and higher
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    else:
        # run this only for Blender versions lower than 3.0
        # call purge_orphans() recursively until there are no more orphan data blocks to purge
        result = bpy.ops.outliner.orphans_purge()
        if result.pop() != "CANCELLED":
            purge_orphans()

def clean_scene():
    """
    Removing all of the objects, collection, materials, particles,
    textures, images, curves, meshes, actions, nodes, and worlds from the scene

    Checkout this video explanation with example

    "How to clean the scene with Python in Blender (with examples)"
    https://youtu.be/3rNqVPtbhzc
    """
    # make sure the active object is not in Edit Mode
    if bpy.context.active_object and bpy.context.active_object.mode == "EDIT":
        bpy.ops.object.editmode_toggle()

    # make sure non of the objects are hidden from the viewport, selection, or disabled
    for obj in bpy.data.objects:
        obj.hide_set(False)
        obj.hide_select = False
        obj.hide_viewport = False

    # select all the object and delete them (just like pressing A + X + D in the viewport)
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()

    # find all the collections and remove them
    collection_names = [col.name for col in bpy.data.collections]
    for name in collection_names:
        bpy.data.collections.remove(bpy.data.collections[name])

    # in the case when you modify the world shader
    # delete and recreate the world object
    world_names = [world.name for world in bpy.data.worlds]
    for name in world_names:
        bpy.data.worlds.remove(bpy.data.worlds[name])
    # create a new world data block
    bpy.ops.world.new()
    bpy.context.scene.world = bpy.data.worlds["World"]

    purge_orphans()

def active_object():
    """
    returns the currently active object
    """
    return bpy.context.active_object

def time_seed():
    """
    Sets the random seed based on the time
    and copies the seed into the clipboard
    """
    seed = time.time()
    print(f"seed: {seed}")
    random.seed(seed)

    # add the seed value to your clipboard
    bpy.context.window_manager.clipboard = str(seed)

    return seed

def set_fcurve_extrapolation_to_linear():
    for fc in bpy.context.active_object.animation_data.action.fcurves:
        fc.extrapolation = "LINEAR"

def create_data_animation_loop(obj, data_path, start_value, mid_value, start_frame, loop_length, linear_extrapolation=True):
    """
    To make a data property loop we need to:
    1. set the property to an initial value and add a keyframe in the beginning of the loop
    2. set the property to a middle value and add a keyframe in the middle of the loop
    3. set the property the initial value and add a keyframe at the end of the loop
    """
    # set the start value
    setattr(obj, data_path, start_value)
    # add a keyframe at the start
    obj.keyframe_insert(data_path, frame=start_frame)

    # set the middle value
    setattr(obj, data_path, mid_value)
    # add a keyframe in the middle
    mid_frame = start_frame + (loop_length) / 2
    obj.keyframe_insert(data_path, frame=mid_frame)

    # set the end value
    setattr(obj, data_path, start_value)
    # add a keyframe in the end
    end_frame = start_frame + loop_length
    obj.keyframe_insert(data_path, frame=end_frame)

    if linear_extrapolation:
        set_fcurve_extrapolation_to_linear()

def set_scene_props(fps, frame_count):
    """
    Set scene properties
    """
    scene = bpy.context.scene
    scene.frame_end = frame_count

    # set the world background to black
    world = bpy.data.worlds["World"]
    if "Background" in world.node_tree.nodes:
        world.node_tree.nodes["Background"].inputs[0].default_value = (0, 0, 0, 1)

    scene.render.fps = fps

    scene.frame_current = 1
    scene.frame_start = 1

def scene_setup():
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()

    clean_scene()

    set_scene_props(fps, frame_count)
    bpy.app.timers.unregister(scene_setup)

def context():
    bpy.ops.preferences.addon_enable(module = "node_arrange")
    for area in bpy.context.screen.areas:
        print(area)
        print(dir(area))
        print("info")
        print(area.ui_type)
        if area.type == 'NODE_EDITOR':
            for region in area.regions:
                print(region)
                print(dir(region))
                print(region.type)
                if region.type == 'WINDOW':
                    ctx = bpy.context.copy()
                    ctx['area'] = area
                    print(ctx['area'].ui_type)
                    ctx['region'] = region
                    print(ctx['region'].type)
                    bpy.ops.node.button(ctx, "INVOKE_DEFAULT")

################################################################
# helper functions END
################################################################

def link_nodes_by_mesh_socket(node_tree, from_node, to_node):
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Mesh"])

def delete_node(node_tree, type_name):
    """Delete a node of a given type.
    """
    node_tree.nodes.remove( node_tree.nodes[ type_name ] )

def create_node(node_tree, type_name, node_x_location, node_location_step_x=0):
    """Creates a node of a given type, and sets/updates the location of the node on the X axis.
    Returning the node object and the next location on the X axis for the next node.
    """
    node_obj = node_tree.nodes.new(type=type_name)
    node_obj.location.x = node_x_location
    node_x_location += node_location_step_x

    return node_obj, node_x_location

def update_geo_node_tree(node_tree):
    """
    Adding a Cube Mesh, Subdiv, Triangulate, Edge Split, and Element scale geo node into the
    geo node tree

    Geo Node type names found here
    https://docs.blender.org/api/current/bpy.types.GeometryNode.html
    """
    out_node = node_tree.nodes["Group Output"]
    
    node_x_location = 0
    node_location_step_x = 300

    mesh_plane_node, node_x_location = create_node(node_tree, "GeometryNodeMeshGrid", node_x_location, node_location_step_x)
    mesh_plane_node.inputs["Size X"].default_value = 100
    mesh_plane_node.inputs["Size Y"].default_value = 100
    mesh_plane_node.inputs["Vertices X"].default_value = 50
    mesh_plane_node.inputs["Vertices Y"].default_value = 50
    set_position_node, node_x_location = create_node(node_tree, "GeometryNodeSetPosition", node_x_location, node_location_step_x)
    subdivision_surface_node, node_x_location = create_node(node_tree, "GeometryNodeSubdivisionSurface", node_x_location, node_location_step_x)
    noise_texture_node, node_x_location = create_node(node_tree, "ShaderNodeTexNoise", node_x_location, node_location_step_x)
    noise_texture_node.inputs["Scale"].default_value = 0.05
    noise_texture_node.inputs["Detail"].default_value = 0.0
    noise_texture_node.inputs["Roughness"].default_value = 0.0
    viewer_node, node_x_location = create_node(node_tree, "GeometryNodeViewer", node_x_location, node_location_step_x)
    set_shade_smooth_node, node_x_location = create_node(node_tree, "GeometryNodeSetShadeSmooth", node_x_location, node_location_step_x)
    combine_node, node_x_location = create_node(node_tree, "ShaderNodeCombineXYZ", node_x_location, node_location_step_x)
    math_node, node_x_location = create_node(node_tree, "ShaderNodeMath", node_x_location, node_location_step_x)
    math_node.label = "Multiply"
    math_node.operation = "MULTIPLY"
    math_node.inputs[1].default_value = 9.4
    object_info_node, node_x_location = create_node(node_tree, "GeometryNodeObjectInfo", node_x_location, node_location_step_x)
    object_info_node.transform_space = "RELATIVE"
    object_info_node.inputs[0].default_value = bpy.data.objects["Circle"]
    object_info_tree_node, node_x_location = create_node(node_tree, "GeometryNodeObjectInfo", node_x_location, node_location_step_x)
    object_info_tree_node.inputs[0].default_value = bpy.data.objects["tree"]
    raycast_node, node_x_location = create_node(node_tree, "GeometryNodeRaycast", node_x_location, node_location_step_x)
    raycast_node.inputs["Ray Direction"].default_value[2] = 1
    distribute_points_on_faces_node, node_x_location = create_node(node_tree, "GeometryNodeDistributePointsOnFaces", node_x_location, node_location_step_x)
    distribute_points_on_faces_node.inputs["Density"].default_value = 0.015
    instance_on_points_node, node_x_location = create_node(node_tree, "GeometryNodeInstanceOnPoints", node_x_location, node_location_step_x)
    join_geometry_node, node_x_location = create_node(node_tree, "GeometryNodeJoinGeometry", node_x_location, node_location_step_x)

#    subdivide_mesh_node, node_x_location = create_node(node_tree, "GeometryNodeSubdivideMesh", node_x_location, node_location_step_x)
#    subdivide_mesh_node.inputs["Level"].default_value = 3

#    triangulate_node, node_x_location = create_node(node_tree, "GeometryNodeTriangulate", node_x_location, node_location_step_x)

#    split_edges_node, node_x_location = create_node(node_tree, "GeometryNodeSplitEdges", node_x_location, node_location_step_x)

#    scale_elements_node, node_x_location = create_node(node_tree, "GeometryNodeScaleElements", node_x_location, node_location_step_x)
#    scale_elements_node.inputs["Scale"].default_value = 0.8

    out_node.location.x = node_x_location

#    link_nodes_by_mesh_socket(node_tree, from_node=mesh_cube_node, to_node=out_node)
    from_node = mesh_plane_node
    to_node = set_position_node
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Geometry"])
    
    from_node = set_position_node
    to_node = subdivision_surface_node
    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Mesh"])

    from_node = subdivision_surface_node
    to_node = distribute_points_on_faces_node
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Mesh"])

    from_node = subdivision_surface_node
    to_node = join_geometry_node
    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Geometry"])

    from_node = distribute_points_on_faces_node
    to_node = instance_on_points_node
    node_tree.links.new(from_node.outputs["Points"], to_node.inputs["Points"])

    from_node = instance_on_points_node
    to_node = join_geometry_node
    node_tree.links.new(from_node.outputs["Instances"], to_node.inputs["Geometry"])

    from_node = join_geometry_node
    to_node = set_shade_smooth_node
    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Geometry"])

    from_node = set_shade_smooth_node
    to_node = out_node
    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Geometry"])

    from_node = noise_texture_node
    to_node = math_node
    node_tree.links.new(from_node.outputs["Fac"], to_node.inputs["Value"])

    from_node = math_node
    to_node = combine_node
    node_tree.links.new(from_node.outputs["Value"], to_node.inputs["Z"])

    from_node = combine_node
    to_node = set_position_node
    node_tree.links.new(from_node.outputs["Vector"], to_node.inputs["Offset"])
    
#    from_node = mesh_plane_node
#    to_node = viewer_node
#    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Geometry"])

    from_node = raycast_node
    to_node = distribute_points_on_faces_node
    node_tree.links.new(from_node.outputs["Is Hit"], to_node.inputs["Selection"])

    from_node = object_info_node
    to_node = raycast_node
    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Target Geometry"])

    from_node = object_info_tree_node
    to_node = instance_on_points_node
    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Instance"])


#    link_nodes_by_mesh_socket(node_tree, from_node=mesh_cube_node, to_node=subdivide_mesh_node)
#    link_nodes_by_mesh_socket(node_tree, from_node=subdivide_mesh_node, to_node=triangulate_node)
#    link_nodes_by_mesh_socket(node_tree, from_node=triangulate_node, to_node=split_edges_node)

#    from_node = split_edges_node
#    to_node = scale_elements_node
#    node_tree.links.new(from_node.outputs["Mesh"], to_node.inputs["Geometry"])

#    from_node = scale_elements_node
#    to_node = out_node
#    node_tree.links.new(from_node.outputs["Geometry"], to_node.inputs["Geometry"])

def make_tree():
    bpy.ops.curve.tree_add(curveRes= (8, 16, 12, 1), makeMesh= False, scaleV0= 0.0, pruneRatio= 1.0, rotate= (0.0, -120.0, -120.0, 140.0), resU= 4, levels= 2, frameRate= 1.0, ratioPower= 2.0, branches= (0, 25, 10, 300), bevel= True, rotateV= (0.0, 30.0, 30.0, 0.0), segSplits= (0.10000000149011612, 0.20000000298023224, 0.20000000298023224, 0.0), handleType= '1', shape= '3', curveV= (120.0, 90.0, 0.0, 0.0), scale= 15.0, leafShape= 'hex', showLeaves= True, ratio= 0.029999999329447746, leaves= 300, armAnim= False, leafScale= 1, leafDist= '2', useArm= False, splitAngle= (3.0, 30.0, 45.0, 0.0), lengthV= (0.0, 0.10000000149011612, 0.0, 0.0), seed= 0, scaleV= 5.0, downAngle= (0.0, 20.0, 30.0, 20.0), pruneWidth= 0.4000000059604645, baseSize= 0.05000000074505806, bevelRes= 0, length= (0.800000011920929, 0.5, 1.5, 0.10000000149011612), downAngleV= (0.0, 10.0, 10.0, 10.0), prune= False, curve= (0.0, 40.0, 0.0, 0.0), taper= (1.0, 1.0, 1.0, 1.0), prunePowerHigh= 0.5, leafScaleX= 0.20000000298023224, curveBack= (20.0, 80.0, 0.0, 0.0), bend= 0.0, scale0= 1.0, prunePowerLow= 0.0010000000474974513, splitAngleV= (0.0, 10.0, 20.0, 0.0), baseSplits= 2, pruneWidthPeak= 0.6000000238418579)
    select_object("tree")
    bpy.ops.object.convert(target='MESH')
    select_all_objects()
    bpy.ops.object.join()
    exportFbxByName("tree")
#    importFbx("tree", "treeLeave")
    move_along_y(100, get_object("tree"))

def create_centerpiece():
#    genLeafMesh(leafScale, leafScaleX, leafScaleT, leafScaleV, loc, quat,
#                offset, index, downAngle, downAngleV, rotate, rotateV, oldRot,
#                bend, leaves, leafShape, leafangle, horzLeaves):
#    bpy.ops.sapling.importdata(filename="willow.py")
#    bpy.ops.curve.tree_add(presetName="Willow")
    bpy.ops.mesh.primitive_circle_add()
    move_along_z(30, active_object())
    axis = make_vector([1,1,1])
    scale_along_axis(30, axis, active_object())
    set_edit_mode(active_object())
    bpy.ops.mesh.fill()
    set_object_mode(active_object())
    bpy.ops.mesh.primitive_plane_add()

    bpy.ops.node.new_geometry_nodes_modifier()
    node_tree = bpy.data.node_groups["Geometry Nodes"]
    delete_node(node_tree, "Group Input")
    update_geo_node_tree(node_tree)
    bpy.app.timers.unregister(create_centerpiece)

#def narrange(areas):
#    for area in areas:
#        print(area)
#        print(dir(area))
#        print("info")
#        print(area.ui_type)
#        if area.type == 'NODE_EDITOR':
#            for region in area.regions:
#                print(region)
#                print(dir(region))
#                print(region.type)
#                if region.type == 'WINDOW':
#                    ctx = bpy.context.copy()
#                    ctx['area'] = area
#                    ctx['region'] = region
#                    bpy.ops.node.button(ctx, "INVOKE_DEFAULT")

def main():
    """
    Python code to generate an animated geo nodes node tree
    that consists of a subdivided & triangulated cube with animated faces
    """
#    bpy.app.timers.register(in_5_seconds)
#    scene_setup()
#    run_in_main_thread(scene_setup)
#    run_in_main_thread(create_centerpiece)
#    run_in_main_thread(arrangeNode.narrange)
#    bpy.app.timers.register(scene_setup)
#    bpy.app.timers.register(create_centerpiece())

    bpy.app.timers.register(scene_setup, first_interval=1.0)
    bpy.app.timers.register(make_tree, first_interval=3.0)
    bpy.app.timers.register(create_centerpiece, first_interval=6.0)
    bpy.app.timers.register(arrangeNode.narrange, first_interval=9.0)  
    
#    arrangeNode.narrange()
#    if finishResult:
#        print("finish")
#        bpy.app.handlers.depsgraph_update_post.append(arrangeNode.narrange())
#    bpy.app.handlers.render_post.append(arrangeNode.narrange())

if __name__ == "__main__":
    main()

#    context()
