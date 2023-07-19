import bpy
import json
import math
import os
import random

FILEPATH = '~/blender/bpy/sphere.blend'
FILEPATHJSON = '~/blender/bpy/save.json'
DIRECTORY='~/blender/bpy/'

def importToScene(FILEPATH):
    with bpy.data.libraries.load(FILEPATH) as (data_from, data_to):
        data_to.objects = [name for name in data_from.objects]
        print('These are the objs: ', data_to.objects)

    # Objects have to be linked to show up in a scene
    for obj in data_to.objects:
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
