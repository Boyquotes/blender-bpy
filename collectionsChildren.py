import bpy

def traverse_tree(t):
    yield t
    for child in t.children:
        yield from traverse_tree(child)

def parent_lookup(coll):
    parent_lookup = {}
    for coll in traverse_tree(coll):
        for c in coll.children.keys():
            parent_lookup.setdefault(c, coll)
    return parent_lookup


C = bpy.context

# Get all collections of the scene and their parents in a dict
coll_scene = C.scene.collection
coll_parents = parent_lookup(coll_scene)

print("coll_scene {}".format(coll_scene))
print("coll_parents {}".format(coll_parents))

# Get collection references
coll_target = coll_scene.children.get("Collection")
active_coll = C.view_layer.active_layer_collection.collection

print("coll_target {}".format(coll_target))
print("active_coll {}".format(active_coll))

# Get parent of *active_coll*
active_coll_parent = coll_parents.get(active_coll.name)

print("active_coll_parent {}".format(active_coll_parent))

#if active_coll_parent:
    # Unlink *active_coll*
#    active_coll_parent.children.unlink(active_coll)

    # Link *active_coll* to *coll_target*
#    coll_target.children.link(active_coll)
