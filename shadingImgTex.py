            # Import the OBJ file
            bpy.ops.import_scene.obj(filepath=file_path)

            # Get the imported object
            obj = bpy.context.selected_objects[0]

            # Add a new material to the object
            mat = bpy.data.materials.new(name="Material")
            obj.data.materials.append(mat)

            # Set the material to use the Principled BSDF shader
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            principled_bsdf = nodes.get("Principled BSDF")
            if principled_bsdf is None:
                principled_bsdf = nodes.new(type="ShaderNodeBsdfPrincipled")
            material_output = nodes.get("Material Output")
            if material_output is None:
                material_output = nodes.new(type="ShaderNodeOutputMaterial")
            links = mat.node_tree.links
            links.new(principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"])

            # Add an image texture to the material and connect it to the Base Color of the Principled BSDF
            texture_path = os.path.join(subdir, "texture.jpg")
            if os.path.exists(texture_path):
                image = bpy.data.images.load(texture_path)
                texture = bpy.data.textures.new(name="Texture", type='IMAGE')
                texture.image = image
                texture_node = nodes.new(type="ShaderNodeTexImage")
                texture_node.image = image
                texture_node.texture_mapping.scale[0] = 2.0
                texture_node.texture_mapping.scale[1] = 2.0
                links.new(texture_node.outputs["Color"], principled_bsdf.inputs["Base Color"])


            # Export the object as a GLB file
            glb_path = os.path.splitext(file_path)[0] + ".glb"
            bpy.ops.export_scene.gltf(filepath=glb_path, export_format='GLB', export_image_format='AUTO', export_materials='EXPORT')

            # Delete the imported object
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            bpy.ops.object.delete(use_global=False, confirm=False)
