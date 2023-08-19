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

SEL_AMOUNT = .001
NB_TREE=40
NB_CUTS=int(NB_TREE/4)
TOTAL_CUTS=int(NB_CUTS*NB_CUTS)-1

def deleteAll():
    if bpy.data.objects:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=True)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
deleteAll()

#obj = bpy.context.edit_object
bpy.ops.mesh.primitive_plane_add(enter_editmode=False, align='WORLD', location=(0, 0, 0))
select_object("Plane")
#obj = bpy.context.edit_object
obj = get_object("Plane")
print(obj)


if bpy.context.object.mode == 'EDIT':
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bmesh.update_edit_mesh(me)
else:
    bpy.ops.object.mode_set(mode='EDIT')
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    bmesh.update_edit_mesh(me)

print(me)
print(bm)

def choice(array_selected):
    num_choice_face=random.randint(0,TOTAL_CUTS)
#    print(num_choice_face)
#    print(array_selected)
    if num_choice_face in array_selected:
        print("deja")
        choice(array_selected)
    else:
        print("ok")
        array_selected.append(num_choice_face)
    return array_selected, num_choice_face

def selection_scatter_faces(bm, total_selection=0):
    bpy.ops.object.mode_set(mode='OBJECT')
     
    for polygon in bpy.context.active_object.data.polygons:
        polygon.select = False
    for edge in bpy.context.active_object.data.edges:
        edge.select = False
    for vertex in bpy.context.active_object.data.vertices:
        vertex.select = False
    if bpy.context.object.mode == 'EDIT':
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bmesh.update_edit_mesh(me)
    else:
        bpy.ops.object.mode_set(mode='EDIT')
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        bmesh.update_edit_mesh(me)

     
    bpy.ops.object.mode_set(mode='EDIT')
    nb_select=0
    selfaces =[]
    bm.faces.ensure_lookup_table()
#    bpy.ops.object.mode_set(mode='OBJECT')
    print("len {}".format(len(bm.faces)))
    print(len(bm.faces))
#    bm.faces[0].select=True
    for f in bm.faces:
        if len(selfaces) < total_selection:
            selfaces, num_choice_face=choice(selfaces)
#            print(f.index)
#            bm.faces[num_choice_face].select=True
            nb_select = nb_select+1
    print(selfaces)
    print("total_selection {} ".format(total_selection))
    print("len selfaces {} ".format(len(selfaces)))
    bm.faces.ensure_lookup_table()
    for fok in selfaces:
        print("select")
        bm.faces[fok].select=True
#    selfaces[0].select=True
#    selfaces[8].select=True
#    selfaces[16].select=True
#    selfaces[24].select=True
#    selfaces[32].select=True
#    selfaces[40].select=True
#    selfaces[48].select=True
#    

#    selfaces[7].select=True
#    selfaces[6].select=True
#    selfaces[5].select=True
#    selfaces[4].select=True
#    selfaces[3].select=True
#    selfaces[2].select=True
#    selfaces[1].select=True
#    
#    selfaces[9].select=True
#    selfaces[10].select=True
#    for fok in selfaces:
#        if ( ( nb_select < total_selection and nb_select !=5) or total_selection == 0 ) :
#            fok.select = True
#            nb_select = nb_select+1
#        else:
#            fok.select = False

def deSelectAll():
    if bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

print(bm)
#bm.subdivide(number_cuts=NB_CUTS)
bmesh.ops.subdivide_edges(bm,
                          edges=bm.edges,
                          cuts=NB_CUTS,
                          use_grid_fill=True,
                          )
#deSelectAll()
selection_scatter_faces(bm, NB_TREE)


def selectAll():
    if bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')

def selectAllVertices():
    if bpy.context.object.mode == 'EDIT':
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'SELECT')

def deSelectVertex():
    bm.select_mode = {'VERT'}
    for v in bm.verts:
        v.select = False
#        v.select = ( v.co.x > 0 )
    bm.select_flush_mode()   
    me.update()

def select_face_amount_under(amount):
    for VERTS in bm.verts:  	 
        VERTS.select = False	  
        if VERTS.co.x < SEL_AMOUNT :
            VERTS.select = True  	 
 
#select_face_amount_under(SEL_AMOUNT)

def select_face_amount_over(amount):
    for VERTS in bm.verts:  	 
        VERTS.select = False	  
        if VERTS.co.x > SEL_AMOUNT:
            VERTS.select = True  	 
 
#select_face_amount_over(SEL_AMOUNT)


def select_face_normal_x(mesh):
    for f in mesh.faces:
        if f.normal.x == 1.0:
            f.select = True

#select_face_normal_x(bm)

def select_face_normal_y(mesh):
    for f in mesh.faces:
        if f.normal.y == 1.0:
            f.select = True

#select_face_normal_y(bm)

def select_face_normal_z(mesh):
    for f in mesh.faces:
        if f.normal.z == 1.0:
            f.select = True

#select_face_normal_z(bm)

def select_face_normal_z_amount(mesh, amount):
    deSelectVertex()
    for f in mesh.faces:
        if f.normal.z > amount:
            f.select = True

#select_face_normal_z_amount(bm, 0.92)

def select_ramdom_vertices():
    bpy.ops.mesh.select_random(percent=10, extend=False)

#select_ramdom_vertices()

def select_random():
    bpy.ops.object.mode_set()
    bpy.context.tool_settings.mesh_select_mode=[False,False,True]
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_random()

#select_random()

def select_ramdom_faces():
#    bpy.ops.object.mode_set(mode='OBJECT')
    for f in bm.faces:
        if random.random() > .5:
            f.select = True
        else:
            f.select = False

#select_ramdom_faces()

def select_ramdom_faces_in_selection(total_selection=0):
    nb_select=0
    selfaces =[]
#    bpy.ops.object.mode_set(mode='OBJECT')
    print(len(bm.faces))
    for f in bm.faces:
        if f.select:
            print(f.index)
            selfaces.append(f)
    print(selfaces)
    print(len(selfaces))
    for fok in selfaces:
        if random.random() > .5 and ( nb_select < total_selection or total_selection == 0 ):
            fok.select = True
            nb_select = nb_select+1
        else:
            fok.select = False

def select_ramdom_faces(total_selection=0):
    selectAllVertices()
    nb_select=0
    selfaces =[]
#    bpy.ops.object.mode_set(mode='OBJECT')
    print(len(bm.faces))
    for f in bm.faces:
        if f.select:
            print(f.index)
            selfaces.append(f)
    print(selfaces)
    print(len(selfaces))
    for fok in selfaces:
        if random.random() > .5 and ( nb_select < total_selection or total_selection == 0 ):
            fok.select = True
            nb_select = nb_select+1
        else:
            fok.select = False

#select_ramdom_faces(4)
#select_ramdom_faces_in_selection(5)
#select_ramdom_faces_in_selection()

#deSelectVertex()

def duplicate(obj, data=True, actions=True, collection=None):
    obj_copy = obj.copy()
    if data:
        obj_copy.data = obj_copy.data.copy()
    if actions and obj_copy.animation_data:
        obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
    collection=get_collection(collection)
    collection.objects.link(obj_copy)
    return obj_copy

def add_object_in_selection(nb_selection=4):
    bpy.context.scene.transform_orientation_slots[0].type = 'GLOBAL'
    select_ramdom_faces(nb_selection)
    selfaces =[]
    selpositions =[]
#    bpy.ops.object.mode_set(mode='OBJECT')
    print(len(bm.faces))
    obMat = obj.matrix_world
    print(obMat)
    for f in bm.faces:
        if f.select:
            print(f.index)
            selfaces.append(f)
            print(f.normal)
            face_location = f.calc_center_median()
            loc_world_space = obMat @ face_location
            print(loc_world_space)
            x = face_location[0]
            y = face_location[1]
            z = face_location[2]
            print('index: '+str(f.index), x, y, z)
#            print(f.x)
            my_location=f.calc_center_median()
            print(my_location)
            selpositions.append(loc_world_space)
#            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
#            bpy.ops.mesh.primitive_cone_add(location=my_location)
#            cone=bpy.context.object
#            cone.rotation_mode='QUATERNION'
#            cone.rotation_quaternion*=Qrot.inverted()
#            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    print(selfaces)
    print(len(selfaces))
    print(selpositions)
    print(len(selpositions))
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    obj_tree=get_object("tree_BTC")
    tab_tree_copy=[]
    for fokposition in range(nb_selection):
        obj_copy=duplicate(obj_tree, data=True, actions=True, collection="ISLAND_BTC")
        print(obj_copy)
        tab_tree_copy.append(obj_copy)
    print(tab_tree_copy)
    i=0
    for fokposition in selpositions:
        print(fokposition)
        print(tab_tree_copy[i])
        newTree=tab_tree_copy[i]
        newTree.location=fokposition
        i += 1
#        bpy.ops.mesh.primitive_cone_add(location=fokposition)

        
#add_object_in_selection(6)
#bpy.ops.object.editmode_toggle()

if bpy.context.object.mode == 'EDIT':
    bmesh.update_edit_mesh(me)
