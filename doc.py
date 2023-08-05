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

def deSelectAll():
    if bpy.context.object.mode == 'EDIT':
        setObjMode()
    bpy.ops.object.select_all(action='DESELECT')

def duplicate(obj, data=True, actions=True, collection=None):
    obj_copy = obj.copy()
    if data:
        obj_copy.data = obj_copy.data.copy()
    if actions and obj_copy.animation_data:
        obj_copy.animation_data.action = obj_copy.animation_data.action.copy()
    bpy.context.collection.objects.link(obj_copy)
    return obj_copy

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
def newMaterial(id):
    mat = bpy.data.materials.get(id)
    if mat is None:
        mat = bpy.data.materials.new(name=id)
    mat.use_nodes = True
    if mat.node_tree:
        mat.node_tree.links.clear()
        mat.node_tree.nodes.clear()
    return mat
	
def newShader(id, type, r, g, b):
	mat = newMaterial(id)
	nodes = mat.node_tree.nodes
	links = mat.node_tree.links
	output = nodes.new(type='ShaderNodeOutputMaterial')

	if type == "diffuse":
		shader = nodes.new(type='ShaderNodeBsdfDiffuse')
		nodes["Diffuse BSDF"].inputs[0].default_value = (r, g, b, 1)

	elif type == "emission":
		shader = nodes.new(type='ShaderNodeEmission')
		nodes["Emission"].inputs[0].default_value = (r, g, b, 1)
		nodes["Emission"].inputs[1].default_value = 1

	elif type == "glossy":
		shader = nodes.new(type='ShaderNodeBsdfGlossy')
		nodes["Glossy BSDF"].inputs[0].default_value = (r, g, b, 1)
		nodes["Glossy BSDF"].inputs[1].default_value = 0

	links.new(shader.outputs[0], output.inputs[0])

	return mat
	
def drawObject():

	mat = newShader("Shader1", "diffuse", 0.1, 1, 0.1)
	bpy.ops.mesh.primitive_cube_add(size=2, align='WORLD', location=(5, 0, 0))
	bpy.context.active_object.data.materials.append(mat)

matGreen = newShader("Green", "diffuse", 0.1, 1, 0.1)
print(matGreen)
matBrown = newShader("Brown", "diffuse", 0.157, 0.048, 0.013)
print(matBrown)
matBrown = newShader("Grey", "diffuse", 0.051, 0.051, 0.051)
print(matBrown)

###TEXTURES
def displace():
    bpy.ops.object.modifier_add(type='DISPLACE')
    texture_set = set(bpy.data.textures.keys())
    bpy.ops.texture.new()
    new_texture_set = set(bpy.data.textures.keys()) - texture_set
    texture_name = new_texture_set.pop()
    texture = bpy.data.textures[texture_name]
    texture.type = 'VORONOI'
    bpy.context.active_object.modifiers[-1].texture = texture
    
displace()

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
###
#SAVE / OPEN
def saveScene(filepath=''):
    if filepath != '':
        bpy.ops.wm.save_as_mainfile(filepath=DIRECTORY+filepath)
    else:
        bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
        
def openScene():
    bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath)
	
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

###
JSON
def open_json():
    i = 0
    with open(r'/Users/nicolasvilla/blender/bpy/save.json','r') as f: 
        data=json.load(f)
        print(data)
        print(len(data))
        floorIsland(len(data))
        for token in data.items():
            print(token)
            print(data[str(i)])
            print(data[str(i)]['symbol'])
            print(data[str(i)]['cs'])
            print(data[str(i)]['mc'])
            #print(data['0']['symbol'])
            i += 1
        return data
    f.close()

### DELETE
def deleteFloor():
	for obj in bpy.context.scene.objects:
		print(obj)
		print(obj.type)
		if obj.type == 'MESH' and obj.name.lower().startswith("n"):
			print('MESH')
			bpy.data.objects[obj.name].select_set(True)
			bpy.ops.object.delete()
			#obj.name = "newName"

### DRAW
spacing = 2.2
nbCubeMax = 5
def floor(nbCubeMax):
	# Iterate over each grid 'cell' we want a cube at
	for x in range(nbCubeMax):
		for y in range(nbCubeMax):
			# calculate the location of the current grid cell, generate a random height
			location = (x * spacing, y * spacing, random.random() * 2)

			# add the cube
			bpy.ops.mesh.primitive_cube_add(
				size=2,
				enter_editmode=False,
				align='WORLD',
				location=location,
				scale=(1, 1, 1))
			bpy.context.active_object.name = 'new_name'+str(x)+str(y)
			# set the cube's material (color in this case)
			item = bpy.context.object
			if random.random() < 0.1:
				item.data.materials.append(bpy.data.materials['Material.Red'])
				item.name = item.name+"-col"
				item.data.name = item.name+"-col"
			else:
				item.data.materials.append(bpy.data.materials['Material.Black'])
				item.name = item.name+"-col"
				item.data.name = item.name+"-col"

### MODIFIER
def displace():
    bpy.ops.object.modifier_add(type='DISPLACE')
    texture_set = set(bpy.data.textures.keys())
    bpy.ops.texture.new()
    new_texture_set = set(bpy.data.textures.keys()) - texture_set
    texture_name = new_texture_set.pop()
    texture = bpy.data.textures[texture_name]
    texture.type = 'VORONOI'
    bpy.context.active_object.modifiers[-1].texture = texture
    bpy.context.active_object.modifiers[-1].name = "Texture1"
    texture = bpy.data.textures[texture_name]
    texture.name = "Texture1"
    texture.use_fake_user = 1
    texture.type= "MUSGRAVE"
    
displace()

def addMoodifierSubSurf():
    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.active_object.modifiers[-1].levels = 6
    
addMoodifierSubSurf()

>>> bpy.data.node_groups["Geometry Nodes.019"].name
'Geometry Nodes.019'

>>> bpy.data.objects["Landscape"].modifiers["GeometryNodes"].name
'GeometryNodes'

# DELETE
import bpy

#Get the material you want (replace the name below)
mat = bpy.data.materials['Material']

#Get the node in its node tree (replace the name below)
node_to_delete =  mat.node_tree.nodes['Principled BSDF']

#Remove it
mat.node_tree.nodes.remove( node_to_delete )

# ADDONS
bpy.ops.preferences.addon_enable(module = "node_arrange")

# VERSION
    print(bpy.app.version_string)
    print(bpy.app.version)
    if (2, 76, 0) < bpy.app.version:
        print("Your Blender version is up to date!")

# DELETE MESH
bpy.ops.mesh.delete(type='VERT')

#TIMER
    bpy.app.timers.register(scene_setup, first_interval=1.0)
    bpy.app.timers.register(create_centerpiece, first_interval=3.0)
    bpy.app.timers.register(arrangeNode.narrange, first_interval=6.0)

# TIMER QUEUE
# This function can safely be called in another thread.
# The function will be executed when the timer runs the next time.
def run_in_main_thread(function):
    print("register")
    execution_queue.put(function)

def execute_queued_functions():
    while not execution_queue.empty():
        function = execution_queue.get()
        print("execute")
        function()
    return 5.0

    run_in_main_thread(scene_setup)
    run_in_main_thread(create_centerpiece)
    run_in_main_thread(arrangeNode.narrange)
    bpy.app.timers.register(execute_queued_functions)

def getChildren(myObject): 
    children = [] 
    for ob in bpy.data.objects: 
        if ob.parent == myObject: 
            children.append(ob) 
    return children 

# SEARCH AND MOVE
objs = get_objects_including('rock', case_sensitive = True)
print(objs)

col = "ROCKS"
move_objects_to_collection(objs, col)
