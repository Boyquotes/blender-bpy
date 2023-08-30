import bpy
import bmesh
import random
import time
import json
import math
import os
import random
import queue
import functools
from datetime import datetime
from bpy_extras import object_utils
import math
import random

import mathutils
from mathutils import Euler
from mathutils import Quaternion
from mathutils import Vector
from math import radians
from random import randrange
from random import gauss
from easybpy import *
from scattering import *
import ant_landscape
import add_curve_sapling

bpy.ops.object.mode_set(mode='OBJECT') 
clean_scene()
#cub = create_cube()
#select_object(cub)

spher = create_uv_sphere()
select_object(spher)

def context_override():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        return {'window': window, 'screen': screen, 'area': area, 'region': region, 'scene': bpy.context.scene} 

def sculpt(coordinates, brush = 'DRAW', strength=1):
    bpy.ops.paint.brush_select(sculpt_tool=brush, toggle=False)
    
    brush = bpy.data.brushes["SculptDraw"]
    brush.strength = strength

    bpy.context.tool_settings.sculpt.brush = brush
    bpy.context.tool_settings.unified_paint_settings.unprojected_radius = 0.2
    
    
    strokes = []
    for i, coordinate in enumerate(coordinates):
        stroke = {
            "name": "stroke",
            "mouse": (0,0),
            "mouse_event": (0,0),
            "x_tilt": 0,
            "y_tilt": 0,
            "pen_flip" : False,
            "is_start": True if i==0 else False,
            "location": coordinate,
            "size": 100,
            "pressure": 1,
            "time": float(i)
        }
        strokes.append(stroke)

    bpy.ops.sculpt.brush_stroke(context_override(), stroke=strokes)

points = [(0,1,0),(0,0,1)]
#points = [(0,0,1)]
bpy.ops.object.mode_set(mode='SCULPT') 
#bpy.data.objects['An Object'].select_set(True)
sculpt(points, 'DRAW', 3)
