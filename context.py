import bpy
from easybpy import *

for area in bpy.context.screen.areas:
    print(area)
    print(dir(area))
    print("info")
    print(area.ui_type)
    if area.type == 'NODE_EDITOR':
        for region in area.regions:
            print(region)
            print(dir(region))
            print(region.type)
            if region.type == 'WINDOW':
                ctx = bpy.context.copy()
                ctx['area'] = area
                ctx['region'] = region
                bpy.ops.node.button(ctx, "INVOKE_DEFAULT")
