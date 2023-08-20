def anime_obj(obj):
    #ANIMATION
    START_FRAME = 1
    END_FRAME = 200
    obj.animation_data_create()
    obj.animation_data.action = bpy.data.actions.new(name="RotationAction")
    fcurve = obj.animation_data.action.fcurves.new(
        data_path="rotation_euler", index=2
    )
    k1 = fcurve.keyframe_points.insert(
        frame=START_FRAME,
        value=0
    )
    k1.interpolation = "LINEAR"
    k2 = fcurve.keyframe_points.insert(
        frame=END_FRAME,
        value= (1 + random.random() * 2) * pi
