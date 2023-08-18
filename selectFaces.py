import bpy, bmesh, random

obj = bpy.context.edit_object
if bpy.context.object.mode == 'EDIT':
    me = obj.data

    bm = bmesh.from_edit_mesh(me)

SEL_AMOUNT = .001

NB_TREE=10
NB_CUTS=int(NB_TREE/4)

def selection_scatter_faces(bm, total_selection=0):
    nb_select=0
    selfaces =[]
#    bpy.ops.object.mode_set(mode='OBJECT')
    print(len(bm.faces))
    bm.faces[0].select=True
    for f in bm.faces:
        if nb_select < total_selection:
            num_choice_face=random.randint(0,63)
            print(num_choice_face)
            print(f.index)
            bm.faces[num_choice_face].select=True
            selfaces.append(f)
            nb_select = nb_select+1

def deSelectAll():
    if bpy.context.object.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='DESELECT')

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

select_face_normal_z_amount(bm, 0.92)

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

selfaces =[]

def select_ramdom_faces_in_selection(total_selection=0):
    nb_select=0
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

select_ramdom_faces_in_selection(5)
#select_ramdom_faces_in_selection()

#deSelectVertex()

def add_object_in_selection():
    select_ramdom_faces_in_selection(4)
    selfaces =[]
    selpositions =[]
#    bpy.ops.object.mode_set(mode='OBJECT')
    print(len(bm.faces))
    for f in bm.faces:
        if f.select:
            print(f.index)
            selfaces.append(f)
            my_location=f.calc_center_median()
            print(my_location)
            selpositions.append(my_location)
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
    for fokposition in selpositions:
        print(fokposition)
        bpy.ops.mesh.primitive_cone_add(location=fokposition)

if bpy.context.object.mode == 'EDIT':
    bmesh.update_edit_mesh(me)
