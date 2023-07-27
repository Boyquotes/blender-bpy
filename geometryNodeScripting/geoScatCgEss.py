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
import functools
from easybpy import *
import add_curve_sapling

execution_queue = queue.Queue()
DIRECTORY='~/blender/bpy/'
arrangeNode = bpy.data.texts["contexte"].as_module()

obj_scatter = "tree"
scatter_reception = "Plane"

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

def scene_setup(clean = 1):
    fps = 30
    loop_seconds = 12
    frame_count = fps * loop_seconds

    seed = 0
    if seed:
        random.seed(seed)
    else:
        time_seed()
    if clean:
        clean_scene()

    set_scene_props(fps, frame_count)
#    bpy.app.timers.unregister(scene_setup)

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

def getChildren(myObject): 
    children = [] 
    for ob in bpy.data.objects: 
        if ob.parent == myObject: 
            children.append(ob) 
    return children 

def scale(scaleSize):
    axis = make_vector([1,1,0])
    scale_along_axis(scaleSize, axis, active_object())

def new_plane(mylocation, mysize, myname):
    bpy.ops.mesh.primitive_plane_add(
        size=mysize,
        calc_uvs=True,
        enter_editmode=False,
        align='WORLD',
        location=mylocation,
        rotation=(0, 0, 0),
        scale=(0, 0, 0))
    current_name = bpy.context.selected_objects[0].name
    plane = bpy.data.objects[current_name]
    plane.name = myname
    plane.data.name = myname + "_mesh"
    return
    
def make_tree():
    bpy.ops.curve.tree_add(curveRes= (8, 16, 12, 1), makeMesh= False, scaleV0= 0.0, pruneRatio= 1.0, rotate= (0.0, -120.0, -120.0, 140.0), resU= 4, levels= 2, frameRate= 1.0, ratioPower= 2.0, branches= (0, 25, 10, 300), bevel= True, rotateV= (0.0, 30.0, 30.0, 0.0), segSplits= (0.10000000149011612, 0.20000000298023224, 0.20000000298023224, 0.0), handleType= '1', shape= '3', curveV= (120.0, 90.0, 0.0, 0.0), scale= 15.0, leafShape= 'hex', showLeaves= True, ratio= 0.029999999329447746, leaves= 300, armAnim= False, leafScale= 1, leafDist= '2', useArm= False, splitAngle= (3.0, 30.0, 45.0, 0.0), lengthV= (0.0, 0.10000000149011612, 0.0, 0.0), seed= 0, scaleV= 5.0, downAngle= (0.0, 20.0, 30.0, 20.0), pruneWidth= 0.4000000059604645, baseSize= 0.05000000074505806, bevelRes= 0, length= (0.800000011920929, 0.5, 1.5, 0.10000000149011612), downAngleV= (0.0, 10.0, 10.0, 10.0), prune= False, curve= (0.0, 40.0, 0.0, 0.0), taper= (1.0, 1.0, 1.0, 1.0), prunePowerHigh= 0.5, leafScaleX= 0.20000000298023224, curveBack= (20.0, 80.0, 0.0, 0.0), bend= 0.0, scale0= 1.0, prunePowerLow= 0.0010000000474974513, splitAngleV= (0.0, 10.0, 20.0, 0.0), baseSplits= 2, pruneWidthPeak= 0.6000000238418579)
    select_object("tree")
    tree = get_object("tree")
    if tree.type == 'CURVE' and tree.name.lower().startswith("tr"):
        children = getChildren(tree)
        print(children)
        for c in children: 
            print(c.name)
        bpy.data.objects[tree.name].select_set(True)
        bpy.data.objects[c.name].select_set(True)
    bpy.ops.object.convert(target='MESH')
#    select_all_objects()
    bpy.ops.object.join()
    return

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
# helper functions END
################################################################

def update_geo_node_tree(node_tree):
    """
    Adding a Cube Mesh, Subdiv, Triangulate, Edge Split, and Element scale geo node into the
    geo node tree

    Geo Node type names found here
    https://docs.blender.org/api/current/bpy.types.GeometryNode.html
    """
    node_x_location = 0
    node_location_step_x = 300
    
    in_node = node_tree.nodes["Group Input"]
    md = bpy.context.active_object.modifiers[-1]
    print(md)
    ng = md.node_group
    print(ng)
    inputs = ng.inputs
    print(inputs)
    out_node = node_tree.nodes["Group Output"]

    if "Density" not in inputs:
        inputs.new("NodeSocketFloat", "Density")
        bpy.context.active_object.modifiers["GeometryNodes"]["Input_2"] = 0.005
        bpy.context.active_object.data.update()
    if "Seed" not in inputs:
        inputs.new("NodeSocketInt", "Seed")
        bpy.context.active_object.modifiers["GeometryNodes"]["Input_3"] = 42
        bpy.context.active_object.data.update()
    if "Terrain" not in inputs:
        inputs.new("NodeSocketObject", "Terrain")
        bpy.context.active_object.data.update()
    if "Object" not in inputs:
        inputs.new("NodeSocketObject", "Object")
        bpy.context.active_object.data.update()
    if "Collection" not in inputs:
        inputs.new("NodeSocketCollection", "Collection")

    distribute_points_on_faces_node, node_x_location = create_node(node_tree, "GeometryNodeDistributePointsOnFaces", node_x_location, node_location_step_x)
    join_geometry_node, node_x_location = create_node(node_tree, "GeometryNodeJoinGeometry", node_x_location, node_location_step_x)
    instance_on_points_node, node_x_location = create_node(node_tree, "GeometryNodeInstanceOnPoints", node_x_location, node_location_step_x)
    object_info_tree_node, node_x_location = create_node(node_tree, "GeometryNodeObjectInfo", node_x_location, node_location_step_x)

    node_tree.links.new(in_node.outputs["Density"], distribute_points_on_faces_node.inputs["Density"])
    node_tree.links.new(in_node.outputs["Seed"], distribute_points_on_faces_node.inputs["Seed"])
    node_tree.links.new(in_node.outputs["Object"], object_info_tree_node.inputs["Object"]) 
    node_tree.links.new(in_node.outputs["Geometry"], join_geometry_node.inputs["Geometry"])
    node_tree.links.new(in_node.outputs["Geometry"], distribute_points_on_faces_node.inputs["Mesh"])
    node_tree.links.new(distribute_points_on_faces_node.outputs["Points"], instance_on_points_node.inputs["Points"])
    node_tree.links.new(object_info_tree_node.outputs["Geometry"], instance_on_points_node.inputs["Instance"])
    node_tree.links.new(instance_on_points_node.outputs["Instances"], join_geometry_node.inputs["Geometry"])
    node_tree.links.new(join_geometry_node.outputs["Geometry"], out_node.inputs["Geometry"])
    
def create_centerpiece():
    new_plane((0,0,-1), 400, "MyFloor")
    bpy.ops.node.new_geometry_nodes_modifier()
    node_tree = bpy.data.node_groups["Geometry Nodes"]
    update_geo_node_tree(node_tree)
#    bpy.app.timers.unregister(create_centerpiece)

def main():
    """
    Python code to generate an geo nodes node tree
    """
    bpy.app.timers.register(functools.partial(scene_setup, 1), first_interval=1.0)
    bpy.app.timers.register(make_tree, first_interval=3.0)
    bpy.app.timers.register(create_centerpiece, first_interval=6.0)
    bpy.app.timers.register(arrangeNode.narrange, first_interval=9.0)  


if __name__ == "__main__":
    main()
