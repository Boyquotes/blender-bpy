import bpy
import json
import math
import os
import random

FILEPATH = '~/blender/bpy/sphere.blend'
FILEPATHJSON = '~/blender/bpy/save.json'
DIRECTORY='~/blender/bpy/'

#myModule = bpy.data.texts[0].as_module().importFbx("Cube")
def importFbx(objName):
    print(bpy.data.objects)
    directory = os.path.dirname(bpy.data.filepath)
    filepath = os.path.join(directory+'/exports', objName + ".fbx")
    print(filepath)
    bpy.ops.import_scene.fbx(filepath=filepath)                                                   

def importToScene(FILEPATH):
    with bpy.data.libraries.load(FILEPATH) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]
        print('These are the objs: ', data_to.objects)

    # Objects have to be linked to show up in a scene
    for obj in data_to.objects:
        bpy.data.collections['collection_name'].objects.link(obj)

def importObjToScene(FILEPATH, objName):
    with bpy.data.libraries.load(FILEPATH) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]
        print('These are the objs: ', data_to.objects)

    # Objects have to be linked to show up in a scene
    for obj in data_to.objects:
        if obj.name == objName:
            bpy.data.collections['collection_name'].objects.link(obj)

def importSphereFromScene(FILEPATH):
    with bpy.data.libraries.load(FILEPATH) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]
        print('These are the objs: ', data_to.objects)

    # Objects have to be linked to show up in a scene
    for obj in data_to.objects:
        print(obj)
        obj_copy = obj.copy()
    return obj_copy

import os
import bpy
# put the location to the folder where the FBXs are located here in this fashion
# this line will only work on windows ie C:\objects
path_to_obj_dir = os.path.join('C:\\', 'objects')
# get list of all files in directory
file_list = sorted(os.listdir(path_to_obj_dir))
# get a list of files ending in 'fbx'
obj_list = [item for item in file_list if item.endswith('.fbx')]
# loop through the strings in obj_list and add the files to the scene
for item in obj_list:
    path_to_file = os.path.join(path_to_obj_dir, item)
    bpy.ops.import_scene.fbx(filepath = path_to_file)
    # if heavy importing is expected 
    # you may want use saving to main file after every import 
    bpy.ops.wm.save_mainfile(filepath = "File.blend")
