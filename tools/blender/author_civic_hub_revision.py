"""Review-only civic massing reset, run inside the existing MCP Blender."""
from pathlib import Path

# Reuse the established scene setup and primitive helpers, not the rejected layout.
helper = Path(__file__).with_name('author_massing_v2.py')
setup = helper.read_text().split('# A tapered, visibly suspended island')[0]
# Prior evidence is preserved in Git; avoid untracked binary copies on reruns.
setup = setup.replace('if not backup.exists():\n    shutil.copy2(source, backup)\n', '')
exec(compile(setup, str(helper), 'exec'))

def prism(name, outline, bottom, top, mat=stone, collection=export):
    n = len(outline)
    verts = [(x, y, z) for z in (bottom, top) for x, y in outline]
    faces = [tuple(reversed(range(n))), tuple(range(n, 2*n))]
    faces += [(i, (i+1)%n, (i+1)%n+n, i+n) for i in range(n)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    return finish(obj, name, mat, collection, 0.035)

# Compact octagonal plaza and narrow destination causeways leave four actual voids.
outline = [(-3.45,-4.75),(3.45,-4.75),(4.75,-3.45),(4.75,3.45),
           (3.45,4.75),(-3.45,4.75),(-4.75,3.45),(-4.75,-3.45)]
prism('cc_floor_primary_civic_plaza', outline, -0.18, 0.0)
for name, loc, size in [('client',(-6.3,0,-0.09),(3.4,3.2,0.18)),
                        ('hobby',(6.3,0,-0.09),(3.4,3.2,0.18)),
                        ('timeline',(0,-5.3,-0.09),(3.2,1.4,0.18)),
                        ('build',(-5,4.9,-0.09),(3,2.2,0.18)),
                        ('automation',(5,4.9,-0.09),(3,2.2,0.18))]:
    box('cc_floor_threshold_'+name,loc,size,stone,bevel=0.045)
# Non-export floating/service volumes visibly hang below separate civic pieces.
for i,(x,y,sx,sy) in enumerate(((0,0,8.5,7.5),(-6.15,-2.7,2.6,2.05),
                               (6.15,-3.05,2.2,2.4),(0,5.1,6.4,1.4))):
    for tier in range(3):
        box(f'review_service_mass_{i}_{tier}',(x,y,-0.4-tier*0.65),
            (sx-tier*0.7,sy-tier*0.4,0.65),dark,preview,0.12)
# Deep split keels create negative space under the front lip in the runtime view.
for i,x in enumerate((-2.55,2.55)):
    box(f'review_suspended_keel_{i}',(x,-3.65,-1.55),(1.5,2.1,2.5),stone,preview,0.18)

cylinder('cc_core_dais',(0,0,0.12),1.62,0.24)
cylinder('cc_core_second_tier',(0,0,0.28),1.20,0.08,dark)
cylinder('cc_core_landmark_foot',(0,0,0.56),0.62,0.46)
for i,a in enumerate((0,math.pi/2,math.pi,3*math.pi/2)):
    obj=box(f'cc_core_landmark_fin_{i}',(0.81*math.cos(a),0.81*math.sin(a),1.52),
            (0.22,0.42,1.75),dark,bevel=0.10)
    obj.rotation_euler.z=a
ring('cc_core_crown',0.94,0.20,2.35)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=0.45,location=(0,0,1.70))
finish(bpy.context.object,'cc_core_system_volume',land)

def terrace(name,x,y,sx,sy,height):
    box(f'cc_shell_{name}_retaining',(x,y,height/2),(sx,sy,height),dark,bevel=0.12)
    box(f'cc_shell_{name}_terrace',(x,y,height+0.08),(sx+0.06,sy+0.06,0.16),stone,bevel=0.07)

# Three joined but unequal civic masses build a real skyline, rather than pylons.
# All footprints begin beyond the protected 4.70 circulation radius.
terrace('archive',0,5.31,6.4,1.05,0.75)
for name,x,width,height in [('west',-2.25,1.8,5.05),('hall',0,2.4,3.4),('east',2.3,1.7,4.25)]:
    box('cc_shell_civic_'+name,(x,5.30,height/2),(width,0.85,height),stone,bevel=0.18)
    box('cc_shell_civic_'+name+'_upper',(x+0.10,5.40,height+0.05),(width*0.85,0.7,0.20),dark,bevel=0.07)
    box('cc_shell_civic_'+name+'_recess',(x,4.86,height*0.58),(width*0.72,0.035,height*0.4),dark,bevel=0.015)
    # Wide occupied frontage establishes civic building scale, not technical trim.
    for level in range(2):
        box(f'cc_shell_civic_{name}_gallery_{level}',(x,4.79,1.25+level*0.8),
            (width*0.92,0.14,0.16),stone,bevel=0.04)

# West threshold is a inhabited civic gate with flanking terraces and canopy.
terrace('client_forecourt',-6.45,-2.7,2.4,1.85,0.9)
terrace('client_upper',-7.1,2.6,1.55,1.75,1.2)
box('cc_shell_client_civic_house',(-7.1,2.6,2.5),(1.55,1.7,2.4),stone,bevel=0.16)
box('cc_shell_client_civic_gallery',(-6.45,-2.85,2.05),(2.35,1.35,1.75),stone,bevel=0.20)
box('cc_shell_client_gallery_inset',(-6.45,-3.55,2.05),(1.95,0.08,0.95),dark,bevel=0.03)
box('cc_shell_client_gate_canopy',(-7.05,0,3.05),(1.55,4.9,0.36),stone,bevel=0.12)
terrace('garden',6.5,-3.1,2.25,2.25,0.7)
terrace('operations',7.35,3.0,1.3,1.65,1.25)
box('cc_shell_operations_house',(7.35,3.15,2.55),(1.3,1.55,2.55),stone,bevel=0.16)

# Foreground terraces frame the spawn and reveal their retaining edges/voids.
for i,x in enumerate((-2.65,2.65)):
    terrace(f'foreground_{i}',x,-5.20,1.65,1.1,0.65+0.20*i)
    for step in range(5):
        box(f'cc_shell_foreground_stair_{i}_{step}',
            (x,-4.75-step*0.19,0.10+step*0.14),(1.45,0.22,0.18),stone,bevel=0.025)
    box(f'cc_console_foreground_bench_{i}',(x,-5.48,1.10+0.2*i),(1.4,0.32,0.18),dark,bevel=0.06)
    box(f'cc_shell_foreground_landscape_{i}',(x,-5.56,1.38+0.2*i),(1.6,0.35,0.45),land,bevel=0.15)
# Substantial civic access stair within a safe western terrace footprint.
for step in range(6):
    box(f'cc_shell_client_access_stair_{step}',(-5.95,-3.3+step*0.22,0.10+step*0.15),
        (1.15,0.24,0.20),stone,bevel=0.025)

def portal(name,center,width,height,orientation):
    x,y=center
    dx,dy=math.cos(orientation),math.sin(orientation)
    for side in (-1,1):
        box(f'cc_portal_{name}_pier_{side}',(x+side*width/2*dx,y+side*width/2*dy,height/2),
            (0.30,0.30,height),dark,bevel=0.08)
    beam=box('cc_arch_'+name,(x,y,height),(width+0.4,0.55,0.36),stone,bevel=0.10)
    beam.rotation_euler.z=orientation
portal('client',(-7.15,0),3.85,2.6,math.pi/2)
portal('hobby',(7.15,0),3.85,2.8,math.pi/2)
portal('timeline',(0,-5.35),3.85,2.5,0)
portal('build',(-5,5.25),3.8,3.2,0)
portal('automation',(5,5.25),3.8,3.7,0)
box('cc_ask_frame',(4.35,2.70,2.60),(1.35,0.62,0.25),land,bevel=0.10)
for i in range(3):
    box(f'cc_console_station_scale_{i}',(7.20,2.05+0.4*i,0.7),(0.25,0.3,1.3),dark,bevel=0.06)

# Broad landscape crowns at perimeter pockets provide human scale without greebles.
for i,(x,y) in enumerate(((-5.45,-3.25),(5.75,-3.45),(-2.70,-5.30),(2.70,-5.30),(-7.1,2.6))):
    cylinder(f'cc_pylon_landscape_trunk_{i}',(x,y,1.20),0.10,1.1,dark,vertices=16)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=0.55,location=(x,y,2.0))
    obj=bpy.context.object
    obj.scale=(1,0.85,1.25)
    finish(obj,f'cc_shell_landscape_crown_{i}',land)

# Review context is clearly excluded from production source validation.
for i,(start,end) in enumerate((((-7.5,0),(-12,0)),((7.5,0),(11.5,0)),
                             ((0,-5.5),(0,-9.8)),((-5,5.5),(-7,9.6)),((5,5.5),(7,9.6)))):
    a,b=Vector((*start,0)),Vector((*end,0)); mid=(a+b)/2
    angle=math.atan2(b.y-a.y,b.x-a.x); length=(b-a).length
    obj=box(f'review_bridge_{i}',(mid.x,mid.y,-0.18),(length,1.55,0.3),stone,preview,0.06)
    obj.rotation_euler.z=angle
    for side in (-1,1):
        offset=Vector((-math.sin(angle),math.cos(angle),0))*side*0.80
        obj=box(f'review_bridge_parapet_{i}_{side}',tuple(mid+offset+Vector((0,0,0.35))),
                (length,0.12,0.65),dark,preview,0.025)
        obj.rotation_euler.z=angle
    box(f'review_destination_terrace_{i}',(b.x,b.y,-0.5),(3.4,2.8,1.0),dark,preview,0.16)
    # One fully massed civic destination: broad stepped gate and paired wings.
    for side in (-1,1):
        box(f'review_destination_wing_{i}_{side}',(b.x+side*1.25,b.y,1.3+0.12*i),
                (0.85,1.4,2.6+0.24*i),stone,preview,0.16)
    box(f'review_destination_gateway_{i}',(b.x,b.y,2.8+0.2*i),(3.4,0.9,0.35),stone,preview,0.08)
cylinder('review_player_body',(0,-3.5,0.80),0.18,1.1,dark,preview,vertices=24)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=0.20,location=(0,-3.5,1.52))
finish(bpy.context.object,'review_player_head',stone,preview)

for obj in bpy.data.collections['GUIDES_DO_NOT_EXPORT'].objects:
    obj.hide_render=True
scene=bpy.context.scene
scene.render.engine=select_eevee_engine(scene.render)
scene.render.resolution_x=1600; scene.render.resolution_y=900
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'; scene.view_settings.exposure=0
camera=bpy.data.objects['PREVIEW_RUNTIME']; camera.location=(0,-21,10)
aim_object_at(camera,(0,0,1.6)); camera.data.type='PERSP'; camera.data.angle=math.radians(52)
scene.camera=camera
bpy.ops.wm.save_as_mainfile(filepath=str(source))
print('REVISED CIVIC-HUB MASSING saved')
