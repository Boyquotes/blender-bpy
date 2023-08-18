         m = ob.modifiers.get("My SubDiv") or ob.modifiers.new('My SubDiv', 'SUBSURF')
         m.levels = 1
         m.render_levels = 2
         m.quality = 3
