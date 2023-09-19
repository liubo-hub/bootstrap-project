import cv2
#from PIL import Image

# image=cv2.imread('wavedog.jpg')
# hsv_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.imshow('original',image)
# cv2.imshow('HSV image',hsv_image)
# cv2.imshow('Gray image',gray_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#__________________________________________________________________
# 打开图像文件
#image = Image.open('wavedog.jpg')

# 获取图像的像素数据
# pixels = image.load()
#
# # 遍历图像的每个像素
# for i in range(image.width):
#     for j in range(image.height):
#         # 获取像素的RGB值
#         r, g, b = pixels[i, j]
#
#         # 修改RGB值，这里将红色通道值加100，将绿色通道值减50，将蓝色通道值保持不变
#         new_r = r + 100
#         new_g = g - 50
#         new_b = b
#
#         # 确保RGB值在0-255之间
#         new_r = max(0, min(new_r, 255))
#         new_g = max(0, min(new_g, 255))
#         new_b = max(0, min(new_b, 255))
#
#         # 更新像素的RGB值
#         pixels[i, j] = (new_r, new_g, new_b)
#
# # 保存修改后的图像
# image.save('modified_image.jpg')
from PIL import Image

initial_image = Image.open('initial.png')
target_image = Image.open('img.png')
initial_pixels = initial_image.load()
target_pixels = target_image.load()
print(initial_image.width, initial_image.height)
for i in range(initial_image.width):
    for j in range(initial_image.height):
        # 获取源照片像素的RGB值
        r, g, b = initial_pixels[i, j][:3]

        # 将源照片像素值赋值给目标照片对应位置的像素
        target_pixels[i, j] = (r, g, b)
        target_image.save('modified_image.png')
