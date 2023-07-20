import bpy
import json
import math
import os
import random

FILEPATH = '~/blender/bpy/sphere.blend'
FILEPATHJSON = '~/blender/bpy/save.json'
DIRECTORY='~/blender/bpy/'

def exportObj():
    print(bpy.data.objects)
    directory = os.path.dirname(bpy.data.filepath)
    filepath = os.path.join(directory+'/exports', bpy.context.active_object.name + ".obj")
    bpy.ops.export_scene.obj(filepath=filepath, use_selection=True)
