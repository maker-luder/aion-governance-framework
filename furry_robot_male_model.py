"""
毛茸茸机器人男性模型 - Blender Python脚本
完整尺寸标注，包含所有身体部分
"""

import bpy
import bmesh
from mathutils import Vector
import math

# 清空场景
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# ========== 尺寸定义（单位：厘米 → Blender单位） ==========
SCALE = 0.01  # 1 cm = 0.01 Blender单位

HEIGHT = 185 * SCALE  # 身高 185 cm
CHEST = 110 * SCALE   # 胸围 110 cm（微胖）
WAIST = 95 * SCALE    # 腰围 95 cm
HIP = 100 * SCALE     # 臀围 100 cm
SHOULDER = 50 * SCALE # 肩宽 50 cm
HEAD_R = 11 * SCALE   # 头部半径 22 cm直径
NECK_R = 8 * SCALE    # 颈部半径 16 cm
ARM_R = 5.5 * SCALE   # 手臂半径 11 cm
LEG_R = 6.5 * SCALE   # 腿部半径 13 cm
FOOT_L = 29 * SCALE   # 脚长 29 cm
HAND_L = 19 * SCALE   # 手长 19 cm

# ========== 创建材质 ==========
def create_material(name, color, roughness=0.4):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs['Base Color'].default_value = color
    bsdf.inputs['Roughness'].default_value = roughness
    return mat

# 皮肤材质（白人肤色）
skin_mat = create_material("SkinMaterial", (0.95, 0.85, 0.75, 1.0), 0.3)

# 毛皮材质（浅灰色毛发）
fur_mat = create_material("FurMaterial", (0.75, 0.75, 0.78, 1.0), 0.6)

# 金属材质（机器人部件）
metal_mat = create_material("MetalMaterial", (0.4, 0.4, 0.45, 1.0), 0.2)

# ========== 辅助函数 ==========
def create_sphere(name, radius, location, material, segments=32, rings=16):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius, location=location, 
        segments=segments, ring_count=rings
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(material)
    return obj

def create_cylinder(name, radius, depth, location, material, vertices=32):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, vertices=vertices
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.data.materials.append(material)
    return obj

def create_capsule(name, radius, depth, location, material):
    """创建胶囊形体（圆柱+两个半球）"""
    # 主圆柱体
    cyl = create_cylinder(f"{name}_cyl", radius, depth - 2*radius, location, material)
    
    # 顶部球体
    top_sphere = create_sphere(f"{name}_top", radius, 
        (location[0], location[1], location[2] + (depth/2 - radius)), material)
    
    # 底部球体
    bot_sphere = create_sphere(f"{name}_bot", radius, 
        (location[0], location[1], location[2] - (depth/2 - radius)), material)
    
    return cyl

# ========== 构建身体 ==========
print("构建身体基础...")

# 躯干（微胖）
torso_height = HEIGHT * 0.43  # 躯干占身高约43%
torso = create_sphere("Torso", CHEST/2 * 1.05, 
    (0, 0, HEIGHT/2 - torso_height/2), skin_mat, segments=32, rings=24)
torso.scale = (1.0, 0.85, 1.1)  # 压扁前后，拉长上下（微胖效果）
bpy.context.view_layer.objects.active = torso
bpy.ops.object.transform_apply(scale=True)

# 胸部（略微隆起）
chest = create_sphere("Chest", CHEST/2 * 1.08,
    (0, 0, HEIGHT * 0.63), skin_mat, segments=32, rings=20)
chest.scale = (1.05, 0.90, 1.0)
bpy.context.view_layer.objects.active = chest
bpy.ops.object.transform_apply(scale=True)

# 腹部（微凸）
belly = create_sphere("Belly", WAIST/2 * 1.1,
    (0, 0, HEIGHT * 0.50), skin_mat, segments=32, rings=20)
belly.scale = (1.08, 0.92, 0.95)
bpy.context.view_layer.objects.active = belly
bpy.ops.object.transform_apply(scale=True)

# 头部（光头，白人特征）
print("构建头部...")
head = create_sphere("Head", HEAD_R, 
    (0, 0, HEIGHT - HEAD_R * 1.8), skin_mat, segments=32, rings=24)
head.scale = (1.0, 1.05, 1.1)  # 略微拉长脸
bpy.context.view_layer.objects.active = head
bpy.ops.object.transform_apply(scale=True)

# 颈部
neck = create_cylinder("Neck", NECK_R, NECK_R * 2.5,
    (0, 0, HEIGHT - NECK_R * 2), skin_mat, vertices=16)

# 脸部细节
# 眼睛（机器人风格发光眼睛）
eye_mat = create_material("EyeMaterial", (0.2, 0.8, 0.9, 1.0), 0.1)  # 青蓝色发光
left_eye = create_sphere("LeftEye", HEAD_R * 0.25,
    (-HEAD_R * 0.4, HEAD_R * 0.5, HEIGHT - HEAD_R * 0.8), eye_mat, segments=16, rings=12)
right_eye = create_sphere("RightEye", HEAD_R * 0.25,
    (HEAD_R * 0.4, HEAD_R * 0.5, HEIGHT - HEAD_R * 0.8), eye_mat, segments=16, rings=12)

# 鼻子
nose = create_sphere("Nose", HEAD_R * 0.15,
    (0, HEAD_R * 0.7, HEIGHT - HEAD_R), skin_mat, segments=12, rings=8)

# 嘴
mouth_mat = create_material("MouthMaterial", (0.3, 0.1, 0.1, 1.0), 0.4)
mouth = create_sphere("Mouth", HEAD_R * 0.2,
    (0, HEAD_R * 0.2, HEIGHT - HEAD_R - HEAD_R * 0.3), mouth_mat, segments=16, rings=8)

# 耳朵（毛茸茸风格）
print("构建耳朵...")
left_ear = create_sphere("LeftEar", HEAD_R * 0.35,
    (-HEAD_R * 0.8, 0, HEIGHT - HEAD_R * 0.3), fur_mat, segments=20, rings=16)
left_ear.scale = (0.6, 1.2, 1.3)
bpy.context.view_layer.objects.active = left_ear
bpy.ops.object.transform_apply(scale=True)

right_ear = create_sphere("RightEar", HEAD_R * 0.35,
    (HEAD_R * 0.8, 0, HEIGHT - HEAD_R * 0.3), fur_mat, segments=20, rings=16)
right_ear.scale = (0.6, 1.2, 1.3)
bpy.context.view_layer.objects.active = right_ear
bpy.ops.object.transform_apply(scale=True)

# 脸颊毛簇（毛茸茸感）
left_cheek_fur = create_sphere("LeftCheekFur", HEAD_R * 0.25,
    (-HEAD_R * 0.6, HEAD_R * 0.4, HEIGHT - HEAD_R * 0.5), fur_mat, segments=16, rings=12)
right_cheek_fur = create_sphere("RightCheekFur", HEAD_R * 0.25,
    (HEAD_R * 0.6, HEAD_R * 0.4, HEIGHT - HEAD_R * 0.5), fur_mat, segments=16, rings=12)

# 四肢
print("构建四肢...")
ARM_LENGTH = HEIGHT * 0.38  # 手臂长度占身高约38%

# 左上臂
left_upper_arm = create_cylinder("LeftUpperArm", ARM_R,
    ARM_LENGTH * 0.55, 
    (-SHOULDER/2 - ARM_R, 0, HEIGHT * 0.70), skin_mat, vertices=16)

# 右上臂
right_upper_arm = create_cylinder("RightUpperArm", ARM_R,
    ARM_LENGTH * 0.55,
    (SHOULDER/2 + ARM_R, 0, HEIGHT * 0.70), skin_mat, vertices=16)

# 左前臂
left_forearm = create_cylinder("LeftForearm", ARM_R * 0.95,
    ARM_LENGTH * 0.45,
    (-SHOULDER/2 - ARM_R, 0, HEIGHT * 0.45), skin_mat, vertices=16)

# 右前臂
right_forearm = create_cylinder("RightForearm", ARM_R * 0.95,
    ARM_LENGTH * 0.45,
    (SHOULDER/2 + ARM_R, 0, HEIGHT * 0.45), skin_mat, vertices=16)

# 手
left_hand = create_sphere("LeftHand", ARM_R * 0.8,
    (-SHOULDER/2 - ARM_R, 0, HEIGHT * 0.28), skin_mat, segments=16, rings=12)
left_hand.scale = (1.0, 0.9, 1.2)
bpy.context.view_layer.objects.active = left_hand
bpy.ops.object.transform_apply(scale=True)

right_hand = create_sphere("RightHand", ARM_R * 0.8,
    (SHOULDER/2 + ARM_R, 0, HEIGHT * 0.28), skin_mat, segments=16, rings=12)
right_hand.scale = (1.0, 0.9, 1.2)
bpy.context.view_layer.objects.active = right_hand
bpy.ops.object.transform_apply(scale=True)

# 腿
print("构建腿部...")
LEG_LENGTH = HEIGHT * 0.48  # 腿长占身高约48%

# 左大腿
left_thigh = create_cylinder("LeftThigh", LEG_R * 1.1,
    LEG_LENGTH * 0.55,
    (-SHOULDER/3, 0, HEIGHT * 0.28), skin_mat, vertices=18)

# 右大腿
right_thigh = create_cylinder("RightThigh", LEG_R * 1.1,
    LEG_LENGTH * 0.55,
    (SHOULDER/3, 0, HEIGHT * 0.28), skin_mat, vertices=18)

# 左小腿
left_calf = create_cylinder("LeftCalf", LEG_R * 0.95,
    LEG_LENGTH * 0.45,
    (-SHOULDER/3, 0, HEIGHT * 0.08), skin_mat, vertices=18)

# 右小腿
right_calf = create_cylinder("RightCalf", LEG_R * 0.95,
    LEG_LENGTH * 0.45,
    (SHOULDER/3, 0, HEIGHT * 0.08), skin_mat, vertices=18)

# 脚
left_foot = create_sphere("LeftFoot", LEG_R * 1.2,
    (-SHOULDER/3, FOOT_L/2, LEG_R * 0.8), skin_mat, segments=20, rings=12)
left_foot.scale = (1.0, 1.8, 0.7)
bpy.context.view_layer.objects.active = left_foot
bpy.ops.object.transform_apply(scale=True)

right_foot = create_sphere("RightFoot", LEG_R * 1.2,
    (SHOULDER/3, FOOT_L/2, LEG_R * 0.8), skin_mat, segments=20, rings=12)
right_foot.scale = (1.0, 1.8, 0.7)
bpy.context.view_layer.objects.active = right_foot
bpy.ops.object.transform_apply(scale=True)

# 尾巴（可选的毛茸茸元素）
print("构建尾巴...")
tail_curve_points = [
    (0, -HIP/2 * 1.2, HEIGHT * 0.35),
    (0, -HIP * 1.0, HEIGHT * 0.30),
    (0, -HIP * 1.3, HEIGHT * 0.20),
    (0, -HIP * 1.4, HEIGHT * 0.05),
]
for i, pos in enumerate(tail_curve_points[:-1]):
    next_pos = tail_curve_points[i+1]
    tail_seg = create_cylinder(f"TailSeg{i}", LEG_R * 0.6,
        ((pos[0]-next_pos[0])**2 + (pos[1]-next_pos[1])**2 + (pos[2]-next_pos[2])**2)**0.5,
        ((pos[0]+next_pos[0])/2, (pos[1]+next_pos[1])/2, (pos[2]+next_pos[2])/2),
        fur_mat, vertices=14)

# 机器人面罩（面部上方）
print("构建机器人元件...")
visor_mat = create_material("VisorMaterial", (0.2, 0.3, 0.4, 0.8), 0.15)
visor = create_sphere("Visor", HEAD_R * 0.5,
    (0, HEAD_R * 0.6, HEIGHT - HEAD_R * 0.4), visor_mat, segments=24, rings=16)
visor.scale = (1.8, 0.5, 0.8)
bpy.context.view_layer.objects.active = visor
bpy.ops.object.transform_apply(scale=True)

# 胸口机器人面板
chest_panel = bpy.data.objects.new("ChestPanel", bpy.data.meshes.new("ChestPanelMesh"))
scene = bpy.context.collection
scene.objects.link(chest_panel)
chest_panel.location = (0, CHEST/2 * 0.3, HEIGHT * 0.60)
chest_panel.scale = (CHEST/3, CHEST/4, CHEST/6)
chest_panel.data.materials.append(metal_mat)

# ========== 输出尺寸信息 ==========
print("\n" + "="*50)
print("男性毛茸茸机器人模型尺寸")
print("="*50)
print(f"身高：185 cm")
print(f"胸围：110 cm（微胖体型）")
print(f"腰围：95 cm")
print(f"臀围：100 cm")
print(f"肩宽：50 cm")
print(f"手臂长度：70 cm")
print(f"腿长：89 cm")
print(f"脚长：29 cm")
print(f"头围：22 cm（光头）")
print("\n体型特征：")
print("- 白人种族特征（肤色 R:0.95 G:0.85 B:0.75）")
print("- 光头设计")
print("- 微胖体型（腰腹部略凸出）")
print("- 毛茸茸耳朵、脸颊和尾巴")
print("- 机器人风格发光眼睛（青蓝色）")
print("- 机器人面罩和胸部面板")
print("="*50)

# 设置渲染
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 128

print("\n模型构建完成！")
print("可在Blender中调整、导出为 .fbx、.obj 或 .blend 格式")
