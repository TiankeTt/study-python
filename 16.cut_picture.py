from PIL import Image

# 打开原始图片
original_img = Image.open("../../资源 4.png")

# 要裁剪的尺寸列表，格式为 (width, height)
sizes = [(2560, 1217)]

for index, size in enumerate(sizes):
    width, height = size
    # 裁剪图片，从(0,0)开始，裁剪出 width x height 的区域
    cropped_img = original_img.crop((0, 0, width, height))
    # 保存裁剪后的图片，命名为 cropped_0.jpg、cropped_1.jpg 等
    # cropped_img.save(f"cropped_{index}.png")
    cropped_img.save(f"free_form_bg.png")