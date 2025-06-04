# animation.py
import bpy, sys, os

input_path = sys.argv[-2]
output_path = sys.argv[-1]

print("📥 입력:", input_path)
print("📤 출력:", output_path)

if not os.path.exists(input_path):
    raise Exception(f"❌ 입력 파일이 존재하지 않습니다: {input_path}")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=input_path)

obj = bpy.context.selected_objects[0]
bpy.context.view_layer.objects.active = obj

for frame, z in [(1, 0), (10, 0.3), (20, 0)]:
    obj.location.z = z
    obj.keyframe_insert(data_path="location", index=2, frame=frame)
    

fcurve = obj.animation_data.action.fcurves.find("location", index=2)
fcurve.modifiers.new(type='CYCLES')

bpy.ops.export_scene.gltf(filepath=output_path, export_format='GLB', export_animations=True)



