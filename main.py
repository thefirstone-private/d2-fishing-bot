import win32gui
import win32ui
import win32con
import win32api
import numpy as np
import cv2 as cv
import pyautogui as pag
import time

pag.FAILSAFE = True


import win32gui
import win32ui
import win32con
import numpy as np
import cv2 as cv

def capture_screen():
    # 获取屏幕尺寸
    screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

    # 创建设备上下文对象（Device Context，DC）
    hdesktop = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # 创建一个内存设备上下文对象，用于临时存储截图
    mem_dc = img_dc.CreateCompatibleDC()

    # 创建一个位图对象，并将其与内存设备上下文对象关联
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, screen_width, screen_height)
    mem_dc.SelectObject(screenshot)

    # 将整个屏幕内容复制到内存设备上下文对象中
    mem_dc.BitBlt((0, 0), (screen_width, screen_height), img_dc, (0, 0), win32con.SRCCOPY)

    # 获取位图的像素数据
    bmp_info = screenshot.GetInfo()
    bmp_str = screenshot.GetBitmapBits(True)

    # 将位图数据转换为OpenCV的图像格式
    img_data = np.frombuffer(bmp_str, dtype=np.uint8).reshape((bmp_info['bmHeight'], bmp_info['bmWidth'], 4))
    img_bgr = cv.cvtColor(img_data, cv.COLOR_BGRA2BGR)

    # 清理资源
    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())
    img_dc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, desktop_dc)

    return img_bgr


def crop_image(image, region):
    x, y, width, height = region

    # 确定裁剪区域的边界
    x_end = x + width
    y_end = y + height

    # 裁剪图像
    cropped_image = image[y:y_end, x:x_end]

    return cropped_image

def matrix_sum(image):
    gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    matrix = np.array(gray_image, dtype=np.uint8)
    matrix_sum = np.sum(matrix)
    return matrix_sum


def press_button():
    pag.keyDown('e')
    time.sleep(.4)
    pag.keyUp('e')


# 指定截图区域的坐标和大小
region_1 = [837, 730, 18, 18]
region_2 = [913, 730, 18, 18]

base = 34387

print("倒数:")
for i in range(3):
    print(3 - i)
    time.sleep(1)


fish = 0

while True:
    img = capture_screen()
    img1 = crop_image(img, region_1)
    e1_sum = matrix_sum(img1)
    img2 = crop_image(img, region_2)
    e2_sum = matrix_sum(img2)

    if e1_sum == base:
        press_button()

    elif e2_sum == base:
        press_button()
        fish = fish + 1
        print("数量:", fish)
        time.sleep(2)
