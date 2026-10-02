"""Review-only composition reset; execute in the existing MCP Blender application."""
import math
import shutil
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / 'art/blender/command-center'
sys.path.insert(0, str(Path(__file__).resolve().parent))
from command_center_common import aim_object_at, select_eevee_engine

source = ART / 'source/command-center.blend'
backup = ART / 'source/command-center-failed-pass-02.blend'
if not backup.exists():
    shutil.copy2(source, backup)
export = bpy.data.collections['EXPORT_COMMAND_CENTER']
preview = bpy.data.collections['PREVIEW_DO_NOT_EXPORT']
for obj in list(export.objects):
    bpy.data.objects.remove(obj, do_unlink=True)
for obj in list(preview.objects):
    if obj.type == 'MESH':
        bpy.data.objects.remove(obj, do_unlink=True)
for mat in list(bpy.data.materials):
    if mat.users == 0:
        bpy.data.materials.remove(mat)

def material(name, color):
    mat = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Metallic'].default_value = 0
    bsdf.inputs['Roughness'].default_value = 0.7
    bsdf.inputs['Emission Strength'].default_value = 0
    mat.diffuse_color = (*color, 1)
    return mat

stone = material('CC_SoftMetal', (0.48, 0.53, 0.56))
dark = material('CC_Graphite', (0.15, 0.20, 0.23))
land = material('CC_Teal', (0.30, 0.40, 0.35))

def finish(obj, name, mat=stone, collection=export, bevel=0):
    obj.name = name
    for coll in list(obj.users_collection):
        coll.objects.unlink(obj)
    collection.objects.link(obj)
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        modifier = obj.modifiers.new('Massing chamfer', 'BEVEL')
        modifier.width = bevel
        modifier.segments = 3
        bpy.ops.object.modifier_apply(modifier=modifier.name)
    obj.select_set(False)
    return obj

def box(name, loc, size, mat=stone, collection=export, bevel=0.08):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.scale = size
    return finish(obj, name, mat, collection, bevel)

def cylinder(name, loc, radius, depth, mat=stone, collection=export, vertices=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    return finish(bpy.context.object, name, mat, collection, 0.04)

def ring(name, radius, width, z, mat=stone, collection=export, sx=1, sy=1):
    vertices=[]
    faces=[]
    count=64
    for zz in (z-0.05,z+0.05):
        for rr in (radius-width/2,radius+width/2):
            vertices.extend((rr*math.cos(i*math.tau/count)*sx,rr*math.sin(i*math.tau/count)*sy,zz) for i in range(count))
    for i in range(count):
        j=(i+1)%count
        faces.extend(((i,j,count+j,count+i),(2*count+i,3*count+i,3*count+j,2*count+j),
                      (i,2*count+i,2*count+j,j),(count+i,count+j,3*count+j,3*count+i)))
    mesh=bpy.data.meshes.new(name)
    mesh.from_pydata(vertices,[],faces)
    obj=bpy.data.objects.new(name,mesh)
    collection.objects.link(obj)
    return finish(obj,name,mat,collection)

# A tapered, visibly suspended island; lower mass is explicitly review-only.
bpy.ops.mesh.primitive_cylinder_add(vertices=16, radius=1, depth=0.18, location=(0,0,-0.09))
obj=bpy.context.object
obj.scale=(7.75,5.75,1)
finish(obj,'cc_floor_civic_island',stone,bevel=0.04)
for index,(z,sx,sy,depth) in enumerate(((-0.40,7.5,5.5,0.42),(-0.95,6.6,4.9,0.7),(-1.75,5.7,4.1,0.9),(-2.45,4.8,3.4,0.6))):
    bpy.ops.mesh.primitive_cone_add(vertices=16,radius1=0.87,radius2=1,depth=depth,location=(0,0,z))
    obj=bpy.context.object
    obj.scale=(sx,sy,1)
    finish(obj,f'review_island_underside_{index}',dark,preview,0.08)
for index,(radius,width,z) in enumerate(((1.62,0.1,0.14),(2.0,0.10,0.03),(3.15,0.07,0.03),(4.60,0.12,0.04))):
    ring(f'cc_floor_circulation_{index}',radius,width,z,dark)
for index,angle in enumerate((0,math.pi,math.pi/2,-math.pi/2,math.pi/4,3*math.pi/4)):
    obj=box(f'cc_floor_radial_seam_{index}',(3.0*math.cos(angle),3.0*math.sin(angle),0.035),(2.1,0.05,0.06),dark,bevel=0.015)
    obj.rotation_euler.z=angle

cylinder('cc_core_dais',(0,0,0.12),1.62,0.24)
cylinder('cc_core_second_tier',(0,0,0.28),1.20,0.08,dark)
cylinder('cc_core_landmark_foot',(0,0,0.56),0.62,0.46)
# Four inward tapered fins shape an open civic landmark, rather than a solid tower.
for index,angle in enumerate((0,math.pi/2,math.pi,3*math.pi/2)):
    obj=box(f'cc_core_landmark_fin_{index}',(0.81*math.cos(angle),0.81*math.sin(angle),1.52),(0.22,0.42,1.75),dark,bevel=0.10)
    obj.rotation_euler.z=angle
ring('cc_core_crown',0.94,0.20,2.35)
bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=16,radius=0.45,location=(0,0,1.70))
finish(bpy.context.object,'cc_core_system_volume',land)

# Split terrace masses and staggered skyline keep sight lines open.
terraces=[(-6.35,-2.8,1.0,1.75,0.7),(-6.25,2.85,1.2,1.75,1.0),
          (6.35,-2.8,1.0,1.75,0.7),(6.95,3.75,0.75,1.45,1.1),
          (-2.45,5.2,1.3,1.3,1.2),(2.45,5.2,1.3,1.3,1.2),
          (-2.7,-5.0,1.15,1.3,0.6),(2.7,-5.0,1.15,1.3,0.6)]
for i,(x,y,sx,sy,height) in enumerate(terraces):
    box(f'cc_shell_terrace_{i}',(x,y,height/2),(sx,sy,height),stone,bevel=0.15)
    box(f'cc_shell_terrace_cap_{i}',(x,y,height+0.09),(sx+0.1,sy+0.1,0.18),dark,bevel=0.08)
    for step in range(3):
        # All approach terraces are perimeter scenery, outside the walk annulus.
        box(f'cc_shell_level_step_{i}_{step}',(x,y-0.42+step*0.28,height+0.20+step*0.12),(sx*0.75,0.25,0.18),stone,bevel=0.03)

for i,(x,y,height,width) in enumerate(((-2.45,5.05,5.05,0.85),(2.45,5.05,4.4,0.85),(-6.5,2.95,3.8,0.85),
                                     (6.95,3.95,3.2,0.70),(-6.5,-3.0,2.7,0.7),(6.5,-3.0,2.4,0.7))):
    box(f'cc_pylon_civic_tower_{i}',(x,y,height/2),(width,0.85,height),stone,bevel=0.16)
    box(f'cc_pylon_crown_{i}',(x,y,height-0.35),(width+0.32,1.16,0.28),dark,bevel=0.10)
    box(f'cc_shell_inset_{i}',(x,y-0.43,height*0.60),(width*0.55,0.06,height*0.45),dark,bevel=0.025)

# Each portal has independent silhouette while retaining certified clear apertures.
def portal(name,center,width,height,orientation):
    x,y=center
    dx,dy=math.cos(orientation),math.sin(orientation)
    for side in (-1,1):
        box(f'cc_portal_{name}_post_{side}',(x+side*width/2*dx,y+side*width/2*dy,height/2),(0.28,0.28,height),dark,bevel=0.10)
    beam=box(f'cc_arch_{name}',(x,y,height),(width+0.40,0.42,0.28),stone,bevel=0.10)
    beam.rotation_euler.z=orientation
    return beam
portal('client',(-7.2,0),3.85,2.6,math.pi/2)
portal('hobby',(7.2,0),3.85,3.2,math.pi/2)
portal('timeline',(0,-5.35),3.85,2.45,0)
portal('build',(-5,5.25),3.8,3.55,0)
portal('automation',(5,5.25),3.8,4.15,0)
# Ask is architectural framing only, clear above the approach.
box('cc_ask_frame',(4.35,2.70,2.60),(1.35,0.62,0.25),land,bevel=0.10)
for i in range(3):
    box(f'cc_console_scale_{i}',(6.95,2.10+0.45*i,0.67),(0.28,0.35,1.3),dark,bevel=0.08)

# Landscape blocks and human-scale cues occupy perimeter pockets, never circulation.
for i,(x,y) in enumerate(((-5.6,-3.3),(5.6,-3.3),(-7.0,3.3),(7.0,3.3),(-2.7,-5.2),(2.7,-5.2))):
    box(f'cc_shell_planter_{i}',(x,y,0.30),(0.65,0.65,0.6),dark,bevel=0.10)
    cylinder(f'cc_pylon_tree_trunk_{i}',(x,y,1.0),0.08,1.15,dark,vertices=16)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=0.48,location=(x,y,1.82))
    finish(bpy.context.object,f'cc_shell_canopy_{i}',land)
for i,(x,y) in enumerate(((-5.9,-4.45),(5.9,-4.45))):
    box(f'cc_console_bench_{i}',(x,y,0.47),(1.1,0.43,0.18),stone,bevel=0.07)
    box(f'cc_console_bench_leg_{i}',(x,y,0.20),(0.75,0.24,0.40),dark,bevel=0.03)

# Review-only bridges/satellite masses indicate larger-world depth, not Stage 03 assets.
for i,(start,end) in enumerate((((-7.5,0),(-11.7,0)),((7.5,0),(11.7,0)),((0,-5.5),(0,-10.0)),((-5,5.5),(-7,9.6)),((5,5.5),(7,9.6)))):
    a,b=Vector((*start,0)),Vector((*end,0))
    mid=(a+b)/2
    length=(b-a).length
    angle=math.atan2(b.y-a.y,b.x-a.x)
    obj=box(f'review_bridge_{i}',(mid.x,mid.y,-0.22),(length,1.55,0.30),stone,preview,0.10)
    obj.rotation_euler.z=angle
    for side in (-1,1):
        offset=Vector((-math.sin(angle),math.cos(angle),0))*side*0.78
        obj=box(f'review_bridge_rail_{i}_{side}',tuple(mid+offset+Vector((0,0,0.47))),(length,0.10,0.80),dark,preview,0.03)
        obj.rotation_euler.z=angle
    cylinder(f'review_destination_platform_{i}',(b.x,b.y,-0.55),1.6,0.9,dark,preview,vertices=16)
    box(f'review_destination_silhouette_{i}',(b.x,b.y,0.85+0.18*i),(1.0,0.85,1.6+0.36*i),stone,preview,0.15)

# A scale figure at the certified spawn is solely preview scenery.
cylinder('review_player_body',(0,-3.5,0.80),0.18,1.1,dark,preview,vertices=24)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,radius=0.20,location=(0,-3.5,1.52))
finish(bpy.context.object,'review_player_head',stone,preview)

for obj in bpy.data.collections['GUIDES_DO_NOT_EXPORT'].objects:
    obj.hide_render=True
scene=bpy.context.scene
scene.render.engine=select_eevee_engine(scene.render)
scene.render.resolution_x=1600
scene.render.resolution_y=900
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
scene.view_settings.exposure=0
world=scene.world
world.use_nodes=True
world.node_tree.nodes['Background'].inputs['Color'].default_value=(0.19,0.28,0.39,1)
world.node_tree.nodes['Background'].inputs['Strength'].default_value=0.65
for light in [o for o in preview.objects if o.type=='LIGHT']:
    light.data.color=(1.0,0.79,0.59) if 'KEY' in light.name.upper() or light.data.type=='SUN' else (0.64,0.80,1.0)
    if light.data.type=='SUN': light.data.energy=2.5
camera=bpy.data.objects['PREVIEW_RUNTIME']
camera.location=(0,-21,10)
aim_object_at(camera,(0,0,1.6))
camera.data.type='PERSP'
camera.data.angle=math.radians(52)
scene.camera=camera
bpy.ops.wm.save_as_mainfile(filepath=str(source))
print('MASSING V2 source saved; failed source backed up:',backup)
