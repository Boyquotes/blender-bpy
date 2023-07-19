import bpy
import json
import math
import os
import random

FILEPATH = '~/blender/bpy/sphere.blend'
FILEPATHJSON = '~/blender/bpy/save.json'
DIRECTORY='~/blender/bpy/'

def saveScene(filepath=''):
    if filepath != '':
        bpy.ops.wm.save_as_mainfile(filepath=DIRECTORY+filepath)
    else:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
