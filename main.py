import win32gui
import win32ui
import win32con
import numpy as np
import cv2 as cv
import pyautogui as pag
import time

pag.FAILSAFE = True


def capture_screen(x, y, width, height):
    # 创建设备上下文对象（Device Context，DC）
    hdesktop = win32gui.GetDesktopWindow()
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)

    # 创建一个内存设备上下文对象，用于临时存储截图
    mem_dc = img_dc.CreateCompatibleDC()

    # 创建一个位图对象，并将其与内存设备上下文对象关联
    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    mem_dc.SelectObject(screenshot)

    # 将指定区域的屏幕内容复制到内存设备上下文对象中
    mem_dc.BitBlt((0, 0), (width, height), img_dc, (x, y), win32con.SRCCOPY)

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
x1, y1, w1, h1 = 837, 730, 18, 18
x2, y2, w2, h2 = 913, 730, 18, 18

base = 34387

print("倒数:")
for i in range(3):
    print(3 - i)
    time.sleep(1)


fish = 0

while True:
    img1 = capture_screen(x1, y1, w1, h1)
    e1_sum = matrix_sum(img1)
    img2 = capture_screen(x2, y2, w2, h2)
    e2_sum = matrix_sum(img2)

    if e1_sum == base:
        press_button()

    elif e2_sum == base:
        press_button()
        fish = fish + 1
        print("数量:", fish)
        time.sleep(2)
