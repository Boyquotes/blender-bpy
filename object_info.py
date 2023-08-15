import bpy

lx = [] # list of objects x locations
ly = [] # list of objects y locations
lz = [] # list of objects z locations

for obj in bpy.data.objects:
    if obj.name.startswith('star'):
        lx.append(obj.location.x)
        ly.append(obj.location.y)
        lz.append(obj.location.z)

def centre(points):
    return min(points) + (max(points) - min(points))/2

focus_centre = (centre(lx), centre(ly), centre(lz))
