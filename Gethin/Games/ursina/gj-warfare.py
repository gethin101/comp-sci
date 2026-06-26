# === Dependency Check ===
try:
    from ursina import *
    from ursina.prefabs.first_person_controller import FirstPersonController
except ImportError:
    print("U need ursina to run our game. Run: py -m pip install ursina")
    import sys; sys.exit(1)
    #ursina for 3d

try:
    from PIL import Image
except ImportError:
    print("U need pillow to run our game. Run: py -m pip install pillow")
    import sys; sys.exit(1)
    #pillow for images - might not need anymore

#===========imports==========
#get full ursina module
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
#get base64 for textures
import base64
from io import BytesIO
from PIL import Image
import sys #system for quit, etc
import time
from ursina import invoke
from ursina import Mesh
from io import StringIO
#===========================

#asign app and window name
app = Ursina("GJ Warfare")

#=====assets references======
floor_texture = 'assets/textures/floor.png'
wall_texture = 'assets/textures/wall.png'
crosshair_texture = 'assets/textures/crosshair.png'
rifle_texture = 'assets/textures/rifle.png'
rifle_ads_texture = 'assets/textures/rifle_ads.png'
pistol_texture = 'assets/textures/pistol.png'
pistol_ads_texture = 'assets/textures/pistol_ads.png'
pistol_audio = Audio('assets/sounds/pistol.ogg', autoplay=False)
rifle_audio = Audio('assets/sounds/rifle.ogg', autoplay=False)
#=========================

#1st person
player = FirstPersonController(
    position=(0, 5, 0),
    speed=10,
    jump_height=2
)

player.cursor.visible = False  #gets rid of original dot
player.mouse_look = False #gets rid of built in rotation so i can do ads slow
mouse.locked = True

last_shot_time = 0
fire_rate = 0.15

#===========================crosshair mc========================

#crosshair entity (centered, textured quad)
crosshair = Entity(
    parent=camera.ui,
    model='quad',
    texture=crosshair_texture,
    scale=(0.05, 0.05),  #size
    position=Vec2(0, 0)
)

cybertruck = Entity(
    model='assets/models/cybertruck.glb',
    scale=0.6,
    position=(20, -1, 10),
    rotation=Vec3(0, 0, 0),
    collider='mesh'
)

cybertruck.texture_scale = (1, 1)
cybertruck.double_sided = True  # optional, if needed


#=========================misc===========================

floor = Entity(
    model='plane',  # Use 'plane' for proper 3D collision
    texture='assets/textures/floor.png',
    scale=(150, 1, 150),
    position=(0, 0, 0),
    collider='box'
)

floor.texture_scale = (150, 150)  # Tile the texture across the surface

floor.texture_scale = (150, 150)



#=====menu======
#esc menu
pause_menu = Entity(
    parent=camera.ui,
    enabled=False,
    model='quad',
    color=color.rgba(0, 0, 0, 180),  #translucent black
    scale=(0.5, 0.5),
    position=(0, 0)
)

#resume button
resume_button = Button(
    text='Resume',
    parent=pause_menu,
    scale=(0.4, 0.1),
    position=(0, 0.1),
    on_click=lambda: toggle_pause(False)
)

#toggle movement and menu
def toggle_pause(state):
    pause_menu.enabled = state
    player.enabled = not state
    mouse.locked = True


#======================walls==========
#wall with wall texture
platform_size = 150 #match platform size
wall_height = 10
wall_thickness = 1

walls = []

#front - all walls the same (cube, unphasable, adjusts to floor - position & scale)
walls.append(Entity(
    model='cube',
    texture=wall_texture,
    scale=(platform_size, wall_height, wall_thickness),
    position=(0, wall_height/2 - 1, -platform_size/2),
    collider='box'
))

#back
walls.append(Entity(
    model='cube',
    texture=wall_texture,
    scale=(platform_size, wall_height, wall_thickness),
    position=(0, wall_height/2 - 1, platform_size/2),
    collider='box'
))

#left
walls.append(Entity(
    model='cube',
    texture=wall_texture,
    scale=(wall_thickness, wall_height, platform_size),
    position=(-platform_size/2, wall_height/2 - 1, 0),
    collider='box'
))

#right
walls.append(Entity(
    model='cube',
    texture=wall_texture,
    scale=(wall_thickness, wall_height, platform_size),
    position=(platform_size/2, wall_height/2 - 1, 0),
    collider='box'
))

#tile (multiple not 1 texture) - wall
for wall in walls:
    wall.texture_scale = (150,10)

#tile (multiple blocks not 1 image) - floor
floor.texture_scale = (150, 150)

#=================target practice=================
from random import choice, uniform

from math import dist
from random import uniform

def move_target():
    platform_size_x = floor.scale_x
    platform_size_z = floor.scale_z

    while True:
        x = uniform(-platform_size_x/2 + 5, platform_size_x/2 - 5)
        z = uniform(-platform_size_z/2 + 5, platform_size_z/2 - 5)
        if dist((x, z), (player.x, player.z)) > 30:
            break

    y = 0.5
    target.position = Vec3(x, y, z)
    target.scale = (3, 3)
    target.billboard = True
    target.enabled = True 
    print("Target moved to:", target.position)

target = Entity(
    model='cube',
    color=color.red,
    scale=(1, 1),
    collider='box',
    parent=scene
)

move_target()

target.collider = BoxCollider(target, size=Vec3(3, 3, 3))
#================================================


#=========================gun=====================
# Gun entity - attatched to 1st person camera
rifle = Entity(
    parent=player.camera_pivot,
    model='quad',
    origin=Vec3(-0.5, -0.5),
    always_on_top=True,
    color=color.white
)

#ads and hip-fire positions and scale
hip_position = Vec3(-0.4, -0.28, 0.45)
ads_position = Vec3(-0.12, -0.165, 0.45)

hip_rotation = Vec3(0, -50, 0)
ads_rotation = Vec3(0, 0, 0)

hip_scale = Vec3(0.4, 0.22, 0.22)
ads_scale = Vec3(0.24, 0.27, 0.27)

rifle.always_on_top = True


#shooting actual bullet
def shoot():
    # === Raycast for detection ===
    direction = camera.forward.normalized()
    origin = camera.world_position + camera.forward
    ignore_list = [rifle, crosshair, fence, floor] + walls

    hit_info = raycast(origin, direction, distance=1000, ignore=ignore_list)

    # === Positional Sound Playback ===
    if current_gun_name == 'pistol':
        Audio('assets/sounds/pistol.ogg', position=origin, autoplay=True)
    elif current_gun_name == 'rifle':
        Audio('assets/sounds/rifle.ogg', position=origin, autoplay=True)

    # === Bullet trail entity ===
    bullet = Entity(
        model='cube',
        color=color.white,
        scale=(0.02, 0.02, 0.2),
        position=origin,
        parent=scene
    )
    bullet.look_at(origin + direction)

    # === Determine bullet destination ===
    if hit_info.hit:
        # Manually freeze the target's world position
        frozen_hit_point = Vec3(hit_info.entity.world_position)
        bullet.animate_position(frozen_hit_point, duration=0.1)
    else:
        bullet.animate_position(origin + direction * 100, duration=0.1)

    bullet.fade_out(duration=0.2)
    invoke(bullet.disable, delay=0.3)

    # === Target hit logic ===
    if hit_info.hit and hit_info.entity == target:
        print('Target hit by raycast!')
        target.animate_scale((0.1, 0.1, 0.1), duration=0.2)
        target.enabled = False
        invoke(move_target, delay=0.5)


def input(key):
    if key == 'left mouse down':
        print("Left click detected — firing weapon")
        shoot()

    elif key == 'escape':
        print("Escape pressed — toggling pause menu")
        toggle_pause(not pause_menu.enabled)

    elif key == '1':
        print("Switching to rifle")
        equip_gun('rifle')

    elif key == '2':
        print("Switching to pistol")
        equip_gun('pistol')

#=================different guns=========


gun_data = {
    'pistol': {
        'texture': pistol_texture,
        'ads_texture': pistol_ads_texture,
        'hip_position': Vec3(-0.42, -0.28, 0.45),
        'ads_position': Vec3(-0.12, -0.155, 0.45),
        'hip_scale': Vec3(0.32, 0.18, 0.18),
        'ads_scale': Vec3(0.24, 0.27, 0.27),
        'hip_rotation': Vec3(0, -60, 0),
        'ads_rotation': Vec3(0, 0, 0)
    },

    'rifle': {
        'texture': rifle_texture,
        'ads_texture': rifle_ads_texture,
        'hip_position': Vec3(-0.5, -0.3, 0.45),
        'ads_position': Vec3(-0.12, -0.155, 0.45),
        'hip_scale': Vec3(0.5, 0.25, 0.25),
        'ads_scale': Vec3(0.24, 0.27, 0.27),
        'hip_rotation': Vec3(8, -25, 0),
        'ads_rotation': Vec3(0, 0, 0)
    }
}


current_gun_name = 'pistol'


def equip_gun(name):
    global current_gun_name
    current_gun_name = name
    data = gun_data[name]
    rifle.texture = data['texture']
    rifle.rotation = lerp(rifle.rotation,
    data['ads_rotation'] if held_keys['right mouse'] else data['hip_rotation'],
    time.dt * 10)

    rifle.position = data['hip_position']
    rifle.scale = data['hip_scale']

equip_gun('pistol')  # or whichever gun you want to start with







#====================================================

#speed variables (walk,sprint) & crouch variables (stand,crouch)
walk_speed = 9
sprint_speed = 12
sprint_jump_speed = 12
crouch_speed = 4
crouch_height = 1
stand_height = 2

#smooth movement
current_speed = walk_speed
current_height = stand_height


#constantly checking for movement keys
def update():
    global current_speed, current_height, current_gun_name, last_shot_time

    # === Gun switching ===
    if held_keys['1']:
        equip_gun('rifle')
    if held_keys['2']:
        equip_gun('pistol')

    # === Movement speed logic ===
    is_moving = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d']

    if held_keys['left shift'] and player.grounded:
        target_speed = crouch_speed
    elif player.grounded:
        if held_keys['left control'] and is_moving:
            target_speed = sprint_speed
        else:
            target_speed = walk_speed
    else:
        target_speed = sprint_jump_speed

    current_speed = lerp(current_speed, target_speed, time.dt * 5)
    player.speed = current_speed

    # === Crouch height logic ===
    target_height = crouch_height if held_keys['left shift'] and player.grounded else stand_height
    current_height = lerp(current_height, target_height, time.dt * 5)
    player.camera_pivot.y = current_height

    # === ADS gun transform ===
    data = gun_data[current_gun_name]
    if held_keys['right mouse']:
        rifle.texture = data['ads_texture']
        rifle.position = lerp(rifle.position, data['ads_position'], time.dt * 10)
        rifle.scale = lerp(rifle.scale, data['ads_scale'], time.dt * 10)
        rifle.rotation = lerp(rifle.rotation, data['ads_rotation'], time.dt * 10)
    else:
        rifle.texture = data['texture']
        rifle.position = lerp(rifle.position, data['hip_position'], time.dt * 10)
        rifle.scale = lerp(rifle.scale, data['hip_scale'], time.dt * 10)
        rifle.rotation = lerp(rifle.rotation, data['hip_rotation'], time.dt * 10)

    # === Camera look ===
    sensitivity = 40
    player.rotation_y += mouse.velocity[0] * sensitivity
    player.camera_pivot.rotation_x = clamp(
        player.camera_pivot.rotation_x - mouse.velocity[1] * sensitivity,
        -90,
        90
    )

    # === Crosshair brightness logic ===
    hit_info = raycast(camera.world_position, camera.forward, distance=100, ignore=[player])
    if hit_info.hit and hit_info.entity:
        c = hit_info.entity.color
        brightness = 0.299 * c.r + 0.587 * c.g + 0.114 * c.b
        inverted = 1 - brightness
        crosshair.color = color.rgb(inverted, inverted, inverted)
    else:
        crosshair.color = color.rgb(1, 1, 0)

    # === Automatic rifle fire ===
    if held_keys['left mouse'] and current_gun_name == 'rifle':
        if time.time() - last_shot_time > 0.15:  # fire rate in seconds
            shoot()
            last_shot_time = time.time()


#entity models================

fence = Entity(
    model='assets/models/fence.obj',
    texture='assets/textures/fence.png',
    scale=180,
    position=(5, 0, 5),
    rotation=Vec3(270, 0, 0),  # Rotate 90 degrees around the Y-axis
    collider='mesh'
)

fence.texture_scale = (2, 2)
fence.double_side = True



#==========================================================

# Sky
Sky(color=color.azure)

app.run()


#================================================
#Created by Gethin & James
#================================================
