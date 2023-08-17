import bpy, bmesh

obj = bpy.context.edit_object
me = obj.data

bm = bmesh.from_edit_mesh(me)

SEL_AMOUNT = .001

def select_face_amount_under(amount):
    for VERTS in bm.verts:  	 
        VERTS.select = False	  
        if -SEL_AMOUNT < VERTS.co.x:
            VERTS.select = True  	 
 
select_face_amount_under(SEL_AMOUNT)

def select_face_normal_x(mesh):
    for f in mesh.faces:
        if f.normal.x == 1.0:
            f.select = True

select_face_normal_x(bm)

def select_face_normal_y(mesh):
    for f in mesh.faces:
        if f.normal.y == 1.0:
            f.select = True

select_face_normal_y(bm)

def select_face_normal_z(mesh):
    for f in mesh.faces:
        if f.normal.z == 1.0:
            f.select = True

select_face_normal_z(bm)

bmesh.update_edit_mesh(me)
