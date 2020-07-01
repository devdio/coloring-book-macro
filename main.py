from ppadb.client import Client
import cv2, time
import numpy as np

SKIP_PIXELS = 9
TARGET_COLOR = [139, 139, 139]

palette = [
    [150, 1890],
    [430, 1890],
    [710, 1890],
    [990, 1890],
    [1280, 1890],
    [150, 2180],
    [430, 2180],
    [710, 2180],
    [990, 2180],
    [1280, 2180],
]

client = Client(host='127.0.0.1', port=5037)

devices = client.devices()
print(devices)

if len(devices) == 0:
    print('no devices attached')
    exit()

device = devices[0]

def take_screenshot():
    img_byte = device.screencap()
    img = cv2.imdecode(np.frombuffer(img_byte, np.uint8), flags=-1) # with alpha channel
    img = img[:, :, :3] # drop alpha channel
    return img

page = 0

while True:
    for i, p in enumerate(palette):
        print('[*] Painting color %d...' % (page * 10 + i + 1))
        device.input_swipe(p[0], p[1], p[0], p[1], 100)

        img = take_screenshot()

        for y in range(300, img.shape[0] - 900, 9):
            for x in range(47, img.shape[1] -47, 9):
                pixel = img[y, x]

                if np.array_equal(pixel, TARGET_COLOR):
                    tap_x = x + 10
                    tap_y = y + 10

                    print('TAP (%d, %d)' % (tap_x, tap_y))
                    device.input_swipe(tap_x, tap_y, tap_x, tap_y, 100)

                    img = take_screenshot()

    device.input_swipe(1280, 1890, 150, 1890, 300)
    page += 1
