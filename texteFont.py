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

clean_scene()

def add_text_curve(body_text, collection=bpy.context.collection):
    font_curve = bpy.data.curves.new(type="FONT", name="Font Curve")
    font_curve.body = body_text
    font_obj = bpy.data.objects.new(name="Font Object", object_data=font_curve)
    bpy.context.scene.collection.objects.link(font_obj)
    
    return font_obj

def add_text(body_text, collection=bpy.context.collection):
    temp3 = 'nr 3. '
    bpy.ops.object.text_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    font_obj = bpy.context.object
    font_obj.data.body = temp3
    
    return font_obj


obj_text = add_text('nr 3. ')
rotate_around_x(90, obj_text)

font_obj = add_text_curve("my text")
rotate_around_x(90, font_obj)

easy_text = create_text()
easy_text.data.body = 'EASY'
easy_text_object = create_text_object()
easy_text_object.data.body = 'EASY BPY'
