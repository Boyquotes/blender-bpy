import bpy

print(C.collection.name)

def main(context):
    for ob in context.scene.objects:
        print(ob)


class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname, text=SimpleOperator.bl_label)


# Register and add to the "object" menu (required to also use F3 search "Simple Object Operator" for quick access).
def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)


def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.simple_operator()

class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Hello World Panel"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")

        row = layout.row()
        row.operator("mesh.primitive_cube_add")


def register():
    bpy.utils.register_class(HelloWorldPanel)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)


if __name__ == "__main__":
    register()


print("here")

print(bpy.context.view_layer)
print(bpy.context.view_layer.objects.active)

list(bpy.data.objects)
bpy.data.objects['Cube']
bpy.data.objects[0]

bpy.data.scenes[0].render.resolution_percentage
bpy.data.scenes[0].objects["Cube"].data.vertices[0].co.x

bpy.data.meshes.new(name="MyMesh")

bpy.context.object["MyOwnProperty"] = 42
bpy.context.object.get("MyOwnProperty")

bpy.data.scenes["Scene"]["test_prop"] = 34
bpy.data.scenes["Scene"].get("test_prop", "fallback value")

collection = bpy.data.collections.new("MyTestCollection")
collection["MySettings"] = {"foo": 10, "bar": "spam", "baz": {}}

del collection["MySettings"]

print(bpy.context.selected_objects)
print(bpy.context.object)
print(bpy.context.visible_bones)

#bpy.context.view_layer.objects.active = obj

if bpy.ops.view3d.render_border.poll():
    bpy.ops.view3d.render_border()
    
# modifies the Z axis in place.
bpy.context.object.location.z += 2.0

# location variable holds a reference to the object too.
location = bpy.context.object.location
location *= 2.0

# Copying the value drops the reference so the value can be passed to
# functions and modified without unwanted side effects.
location = bpy.context.object.location.copy()

obj = bpy.context.object
obj.location[2] = 0.0
obj.keyframe_insert(data_path="location", frame=10.0, index=2)
obj.location[2] = 1.0
obj.keyframe_insert(data_path="location", frame=20.0, index=2)

obj = bpy.context.object
obj.animation_data_create()
obj.animation_data.action = bpy.data.actions.new(name="MyAction")
fcu_z = obj.animation_data.action.fcurves.new(data_path="location", index=2)
fcu_z.keyframe_points.add(2)
fcu_z.keyframe_points[0].co = 10.0, 0.0
fcu_z.keyframe_points[1].co = 20.0, 1.0

#DEBUG
print('\nUsing dir(object) :\n')
for attr in dir(bpy.context.active_object.data):

bpy.app.debug_wm=1
print(bpy.app.debug_wm)

#PYRAMID
# Define the coordinates of the vertices. Each vertex is defined by 3 consecutive floats.
coords=[(-1.0, -1.0, -1.0), (1.0, -1.0, -1.0), (1.0, 1.0 ,-1.0), \
(-1.0, 1.0,-1.0), (0.0, 0.0, 1.0)]
 
# Define the faces by index numbers. Each faces is defined by 4 consecutive integers.
faces=[ (2,1,0), (0,1,4), (1,2,4), (2,3,4), (3,0,4)]
 
me = bpy.data.meshes.new("PyramidMesh")   # create a new mesh  
 
ob = bpy.data.objects.new("Pyramid", me)          # create an object with that mesh
ob.location = bpy.context.scene.cursor.location   # position object at 3d-cursor
bpy.context.collection.objects.link(ob)                # Link object to scene
 
# Fill the mesh with verts, edges, faces 
me.from_pydata(coords,[],faces)   # edges or faces should be [], or you ask for problems
me.update(calc_edges=True)    # Update mesh with new data
#DISPLAY VERTEX COORDS
obj = bpy.data.objects['Cube']
print('ICI')
wm = obj.matrix_world
print( wm )
for v in obj.data.vertices:
    print(v)
    world = wm @ v.co
    print(world)
    print(world.x)
    print(world.y)
    print(world.z)
    
coords = [(obj.matrix_world @ v.co) for v in obj.data.vertices]
print(coords)

#EXTRUDE
#bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 2)})
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, -2)})
#bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(-2, 0, 0)})
#bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 2, 0)})

# MATERIAL TEXTURE
#import bpy
#import bmesh
#from easybpy import *

#MATERIALS BPY
create_material('Namee')
add_material_to_object("Island-col", "Namee")

#MATERIALS
mat = bpy.data.materials.new("moveon")
#mat = bpy.context.active_object.material_slots[0].material

filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
print(directory)
#bpy.path.abspath('images/gradientPalette.png')
print(directory+bpy.path.abspath('/images/gradientPalette.png'))
imgpath = bpy.path.abspath(directory+'/images/gradientPalette.png')
img = bpy.data.images.load(imgpath)

mat.use_nodes=True
##setup the node_tree and links as you would manually on shader Editor
##to define an image texture for a material
material_output = mat.node_tree.nodes.get('Material Output')
principled_BSDF = mat.node_tree.nodes.get('Principled BSDF')
tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
tex_node.image = img
mat.node_tree.links.new(tex_node.outputs[0], principled_BSDF.inputs[0])


###
IMPORT
def importSphereFromScene(FILEPATH):
	with bpy.data.libraries.load(FILEPATH) as (data_from, data_to):
		data_to.objects = [name for name in data_from.objects]
		print('These are the objs: ', data_to.objects)

	# Objects have to be linked to show up in a scene
	for obj in data_to.objects:
		print(obj)
		obj_copy = obj.copy()
	return obj_copy

def importToScene(FILEPATH):
	with bpy.data.libraries.load(FILEPATH) as (data_from, data_to):
		data_to.objects = [name for name in data_from.objects]
		print('These are the objs: ', data_to.objects)

	# Objects have to be linked to show up in a scene
	for obj in data_to.objects:
#   	 bpy.context.scene.objects.link(obj)
#   	 bpy.context.collection.objects.link(obj)
		bpy.data.collections['collection_name'].objects.link(obj)

####
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
print(directory)
#bpy.path.abspath('images/gradientPalette.png')
print(directory+bpy.path.abspath('/images/gradientPalette.png'))
imgpath = bpy.path.abspath(directory+'/images/gradientPalette.png')
img = bpy.data.images.load(imgpath)
mat.use_nodes=True

##setup the node_tree and links as you would manually on shader Editor
##to define an image texture for a material
material_output = mat.node_tree.nodes.get('Material Output')
principled_BSDF = mat.node_tree.nodes.get('Principled BSDF')

tex_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
tex_node.image = img

mat.node_tree.links.new(tex_node.outputs[0], principled_BSDF.inputs[0])

bpy.ops.object.mode_set(mode="EDIT")
mesh = bpy.context.active_object.data
bm = bmesh.from_edit_mesh(bpy.context.object.data)
bm.faces.ensure_lookup_table()
bpy.ops.uv.unwrap()
bpy.ops.object.mode_set(mode="OBJECT")
bpy.context.active_object.data.materials.append(mat)

#TEXTURES
bpy.data.textures.new("NewTexture", type='IMAGE')

    print(str(attr), getattr(bpy.context.active_object.data, attr))

# UNWRAP
uv_layer = bm.loops.layers.uv.active
#assign the uv values for the vertices of each face. This example
#assumes the default cube
for i in range(6):

    loop_data = bm.faces[i].loops
    uv_data = loop_data[0][uv_layer].uv
    uv_data.x = 1.0
    uv_data.y = 0.0

    uv_data = loop_data[1][uv_layer].uv
    uv_data.x = 1.0
    uv_data.y = 1.0

    uv_data = loop_data[2][uv_layer].uv
    uv_data.x = 0.0
    uv_data.y = 1.0

    uv_data = loop_data[3][uv_layer].uv
    uv_data.x = 0.0
    uv_data.y = 0.0

bpy.ops.uv.unwrap()
bpy.ops.uv.smart_project()

# DIRECTORY AND PATH
filepath = bpy.data.filepath
directory = os.path.dirname(filepath)
print(directory)


