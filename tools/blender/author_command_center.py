"""Editable first art pass. Run sections in the existing Blender MCP session.

This is a source-authoring recipe, never an export or bootstrap replacement.
"""
import math
import bpy
from mathutils import Vector

COLLECTION = bpy.data.collections['EXPORT_COMMAND_CENTER']


def material(name, color, metallic, roughness, emission=0):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Metallic'].default_value = metallic
    bsdf.inputs['Roughness'].default_value = roughness
    bsdf.inputs['Emission Color'].default_value = (*color, 1)
    bsdf.inputs['Emission Strength'].default_value = emission
    return mat


def finish(obj, name, mat, bevel=0):
    obj.name = name
    for collection in list(obj.users_collection):
        collection.objects.unlink(obj)
    COLLECTION.objects.link(obj)
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new('Authored edge radius', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        bpy.ops.object.modifier_apply(modifier=mod.name)
    for face in obj.data.polygons:
        face.use_smooth = True
    return obj


def box(name, xyz, size, mat, bevel=0.04, angle=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=xyz)
    obj = bpy.context.object
    obj.scale = size
    obj.rotation_euler.z = angle
    return finish(obj, name, mat, bevel)


def cylinder(name, xyz, radius, depth, mat, vertices=64, bevel=0.025):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=xyz)
    return finish(bpy.context.object, name, mat, bevel)


def tube(name, xyz, radius, minor, mat, rotation=(0, 0, 0)):
    bpy.ops.mesh.primitive_torus_add(major_segments=72, minor_segments=10,
        location=xyz, major_radius=radius, minor_radius=minor, rotation=rotation)
    return finish(bpy.context.object, name, mat)


def beam(name, a, b, width, mat):
    a, b = Vector(a), Vector(b)
    obj = box(name, (a+b)/2, (width, width, (b-a).length), mat, width*.18)
    obj.rotation_euler = (b-a).to_track_quat('Z', 'Y').to_euler()
    return obj


def sector(name, inner, outer, a0, a1, z0, z1, mat, steps=24):
    verts = []
    for z in (z0, z1):
        for r in (inner, outer):
            verts.extend([(r*math.cos(a0+(a1-a0)*i/steps), r*math.sin(a0+(a1-a0)*i/steps), z) for i in range(steps+1)])
    n = steps+1
    faces = []
    for i in range(steps):
        faces += [(i,i+1,n+i+1,n+i), (2*n+i,3*n+i,3*n+i+1,2*n+i+1),
                  (i,2*n+i,2*n+i+1,i+1), (n+i,n+i+1,3*n+i+1,3*n+i)]
    faces += [(0,n,3*n,2*n),(n-1,3*n-1,4*n-1,2*n-1)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    COLLECTION.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    return finish(obj, name, mat, .015)


def palette():
    global graphite, gunmetal, stone, cyan, teal, violet, glass
    graphite = material('CC_Graphite', (.026,.045,.075), .5,.36)
    gunmetal = material('CC_Gunmetal', (.10,.17,.23), .7,.29)
    stone = material('CC_SoftMetal', (.48,.57,.60), .4,.38)
    cyan = material('CC_Cyan', (.17,.67,.91), .15,.3, 1.6)
    teal = material('CC_Teal', (.11,.43,.24), .0,.6)
    violet = material('CC_Violet', (.40,.28,.60), .2,.4,.3)
    glass = material('CC_DarkGlass', (.045,.17,.22), .08,.14)


def plaza():
    # Rounded civic platform, with a shallow visible floating lip.
    box('cc_floor_foundation', (0,0,-.085), (15.6,11.6,.19), gunmetal,.085)
    box('cc_floor_surface', (0,0,.025), (15.35,11.35,.07), stone,.034)
    for i in range(16):
        a = i*math.tau/16
        sector(f'cc_floor_radial_{i:02}',1.7,4.65,a+.016,a+math.tau/16-.016,.066,.082,
               stone if i%2 else gunmetal)
        sector(f'cc_floor_guidance_{i:02}',4.45,4.49,a+.05,a+math.tau/16-.05,.085,.094,cyan)
    cylinder('cc_core_dais',(0,0,.135),1.62,.25,stone,96,.035)
    cylinder('cc_core_dais_second',(0,0,.27),1.22,.09,gunmetal,96,.025)
    tube('cc_core_dais_inlay',(0,0,.319),1.13,.016,cyan)
    for name,x,y,w,d in [('client',-6.4,0,2.6,2.9),('hobby',6.4,0,2.6,2.9),
                         ('timeline',0,-4.8,2.9,1.9),('build',-5,4.9,2.7,1.7),('automation',5,4.9,2.7,1.7)]:
        box('cc_floor_bridge_'+name,(x,y,.10),(w,d,.10),stone,.045)
        for side in (-1,1):
            if name in ('client','hobby'):
                box('cc_floor_lane_'+name+str(side),(x,side*1.25,.157),(w,.035,.015),cyan,.007)
            else:
                box('cc_floor_lane_'+name+str(side),(x+side*1.15,y,.157),(.035,d,.015),cyan,.007)


def core():
    # A faceted suspended globe inside an open meridian instrument.
    cylinder('cc_core_instrument_base',(0,0,.48),.61,.30,graphite,48,.04)
    for i in range(12):
        a=i*math.tau/12
        box(f'cc_core_base_fin_{i:02}',(.64*math.cos(a),.64*math.sin(a),.53),(.15,.07,.36),stone,.02,a)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3,radius=.56,location=(0,0,1.73))
    globe=finish(bpy.context.object,'cc_core_globe',cyan)
    wire=globe.modifiers.new('Geodesic lattice','WIREFRAME'); wire.thickness=.014
    bpy.ops.object.modifier_apply(modifier=wire.name)
    tube('cc_core_equator',(0,0,1.73),.64,.014,cyan)
    for i in range(3):
        tube(f'cc_core_meridian_{i}',(0,0,1.73),.64,.012,cyan,(math.pi/2,0,i*math.pi/3))
    for i,a in enumerate((.2,2.3,4.4)):
        # An incomplete orbit is deliberately open on its camera-facing side.
        ring=sector(f'cc_core_orbit_{i}',.88,1.00,a,a+2.35,-.045,.045,stone,44)
        ring.location.z=1.64
        ring.rotation_euler=(.45+i*.3,.25,i*.7)
    for i in range(4):
        a=i*math.pi/2+.45
        beam(f'cc_core_support_{i}',(.47*math.cos(a),.47*math.sin(a),.58),
             (.78*math.cos(a),.78*math.sin(a),1.16),.07,gunmetal)
    cylinder('cc_core_emitter',(0,0,.79),.20,.18,cyan,48,.02)
    tube('cc_core_crown',(0,0,2.55),.31,.024,cyan)


def tower(name,x,y,h,angle=0):
    # Stepped buttresses and recessed glazing make each silhouette architectural.
    box('cc_shell_'+name+'_plinth',(x,y,.23),(1.14,1.16,.34),gunmetal,.08,angle)
    box('cc_pylon_'+name,(x,y,h/2+.35),(.78,.84,h),stone,.09,angle)
    box('cc_shell_'+name+'_recess',(x,y-.443,h/2+.38),(.48,.045,h-.46),glass,.02)
    for k in range(6):
        z=.65+k*(h-.6)/6
        box('cc_shell_'+name+f'_louver_{k}',(x,y-.49,z),(.57,.13,.052),gunmetal,.02)
    box('cc_shell_'+name+'_cap',(x,y,h+.43),(1.01,1.06,.16),gunmetal,.055)
    box('cc_shell_'+name+'_light',(x,y-.55,h+.43),(.58,.03,.07),cyan,.012)


def architecture():
    for name,x,y,h in [('west',-7,2.8,3.5),('east',7,2.8,3.5),
                       ('northwest',-2.65,4.98,4.5),('northeast',2.65,4.98,4.5),
                       ('nearwest',-4.5,-4.8,1.95),('neareast',4.5,-4.8,1.95)]:
        tower(name,x,y,h)
    # Five canopy lintels sit wholly above walk clearance, preserving exits.
    arches=[('client',(-7.15,-1.5,3),(-7.15,1.5,3)),
            ('hobby',(7.15,-1.5,3),(7.15,1.5,3)),
            ('timeline',(-1.5,-5.2,2.8),(1.5,-5.2,2.8)),
            ('build',(-6.25,5.25,3.1),(-3.75,5.25,3.1)),
            ('automation',(3.75,5.25,3.1),(6.25,5.25,3.1))]
    for name,a,b in arches:
        beam('cc_arch_'+name,a,b,.26,stone)
        beam('cc_portal_'+name+'_light',(a[0],a[1],a[2]-.15),(b[0],b[1],b[2]-.15),.035,cyan)
        beam('cc_portal_'+name+'_crown',(a[0],a[1],a[2]+.30),(b[0],b[1],b[2]+.30),.11,gunmetal)
    # Open shell ribs occupy isolated perimeter pockets, never the walking ring.
    for side in (-1,1):
        for i in range(4):
            x=side*(5.35+i*.40); y=-3.65
            box(f'cc_shell_arcade_{side}_{i}',(x,y,1.1),(.18,.42,2.1),stone,.06)
            box(f'cc_shell_arcade_roof_{side}_{i}',(x,y,2.40),(.45,1.05,.18),gunmetal,.04)
    # Ask frame floats overhead, leaving the entire certified approach unobstructed.
    box('cc_ask_frame',(4.35,2.70,2.57),(1.55,.25,.30),cyan,.07)
    box('cc_console_ask_canopy',(4.35,2.70,2.81),(1.80,.80,.12),gunmetal,.04)


def tree(name,x,y,height=2.1):
    cylinder('cc_shell_planter_'+name,(x,y,.31),.38,.40,stone,48,.05)
    cylinder('cc_shell_soil_'+name,(x,y,.53),.32,.04,graphite,48,.006)
    cylinder('cc_shell_trunk_'+name,(x,y,.98),.07,.90,gunmetal,12,.01)
    for i,(dx,dy,dz,scale) in enumerate([(-.14,0,0,.36),(.13,.12,.18,.40),(.05,-.16,.39,.35),(-.08,.07,.60,.29)]):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=scale,location=(x+dx,y+dy,height-.6+dz))
        obj=bpy.context.object; obj.scale=(1,.85,1.10)
        finish(obj,'cc_shell_foliage_'+name+str(i),teal)


def props():
    for i,(x,y) in enumerate([(-6.75,-2.25),(6.75,-2.25),(-7.25,4.45),(7.25,4.45),
                            (-2.0,5.3),(2.0,5.3),(-3.0,-5.0),(3.0,-5.0)]):
        tree(str(i),x,y)
    for side in (-1,1):
        x=side*6.0; y=-4.55
        box('cc_console_bench_'+str(side),(x,y,.55),(1.25,.36,.13),stone,.055)
        box('cc_console_bench_back_'+str(side),(x,y+.16,.83),(1.25,.10,.43),gunmetal,.035)
        for dx in (-.45,.45):
            box('cc_console_bench_leg_'+str(side)+str(dx),(x+dx,y,.30),(.12,.30,.43),gunmetal,.025)
    for i,(x,y) in enumerate([(-7.45,-3.9),(7.45,-3.9),(-1.9,5.2),(1.9,5.2)]):
        cylinder('cc_pylon_lamp_'+str(i),(x,y,1.15),.045,2.2,gunmetal,16,.01)
        box('cc_console_lamp_'+str(i),(x,y,2.29),(.30,.22,.15),stone,.035)
        box('cc_console_lamp_lens_'+str(i),(x,y,2.19),(.23,.17,.035),cyan,.008)
    for i,(x,y) in enumerate([(-5.1,-4.45),(5.1,-4.45),(-3.0,4.5)]):
        box('cc_console_kiosk_'+str(i),(x,y,.70),(.36,.34,1.2),gunmetal,.055)
        screen=box('cc_console_screen_'+str(i),(x,y-.20,1.13),(.38,.065,.28),cyan,.02)
        screen.rotation_euler.x=math.radians(12)


def lighting():
    scene=bpy.context.scene
    scene.world.use_nodes=True
    bg=scene.world.node_tree.nodes.get('Background')
    bg.inputs['Color'].default_value=(.20,.30,.42,1)
    bg.inputs['Strength'].default_value=.55
    key=bpy.data.objects['PREVIEW_Key']; key.data.type='AREA'; key.data.energy=1900
    key.data.color=(1,.69,.43); key.data.shape='DISK'; key.data.size=9
    key.location=(-6,-4,10)
    key.rotation_euler=(Vector((0,0,0))-key.location).to_track_quat('-Z','Y').to_euler()
    for name,energy,color in [('PREVIEW_Cyan',1100,(.43,.68,1)),('PREVIEW_Teal',900,(.68,.83,1))]:
        lamp=bpy.data.objects[name]; lamp.data.type='AREA'; lamp.data.energy=energy; lamp.data.color=color; lamp.data.size=7
        lamp.rotation_euler=(Vector((0,0,0))-lamp.location).to_track_quat('-Z','Y').to_euler()
    scene.view_settings.view_transform='AgX'; scene.view_settings.exposure=0
