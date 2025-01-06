import cv2
import pyautogui
from PIL import ImageGrab
import numpy as np
import time


def capture_game_window():
    screenshot = ImageGrab.grab()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY).astype(np.uint8)


def template_from_path(image_path):
    print(f"Reading image {image_path}")
    template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    return cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY).astype(np.uint8)


def find_image_color(game_window, template, threshold=0.8):
    res = cv2.matchTemplate(game_window, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        return pt
    return None


def click_action(pos):
    previous_position = pyautogui.position()
    pyautogui.click(x=pos[0], y=pos[1], clicks=3)
    pyautogui.moveTo(*previous_position)


def chest_action(pos):
    print("Chest found!")
    click_action(pos)


def drag_action(pos, dx):
    pyautogui.moveTo(pos[0], pos[1])
    pyautogui.mouseDown()
    pyautogui.dragTo(pos[0] + dx, pos[1], duration=0.666)
    pyautogui.mouseUp()


IMG_TO_ACTION = {
    "activate": click_action,
    "close": click_action,
    "close2": click_action,
    "chest": chest_action,
    "left": lambda pos: drag_action(pos, -700),
    "right": lambda pos: drag_action(pos, 700),
    "rage": click_action,
}
IMG_TO_TEMPLATE = {
    k: template_from_path(f"./assets/{k}.png") for k in IMG_TO_ACTION.keys()
}


def main():
    pyautogui.PAUSE = 0.03
    print("Starting main loop")
    count = 0
    search_images = False

    while True:
        pyautogui.press("w")
        pyautogui.click(clicks=4, interval=0.07)
        pyautogui.click(button="right")  # Dash every iteration
        search_images |= count % 19 == 0
        count += 1
        if not search_images:
            continue

        search_images = False
        game_window = capture_game_window()

        for img_name, action in IMG_TO_ACTION.items():
            template = IMG_TO_TEMPLATE[img_name]
            if (pos := find_image_color(game_window, template)) is not None:
                print(f"Matched {img_name} image, {template.shape}!")
                h, w = template.shape
                x, y = pos[0] + w / 2, pos[1] + h / 2
                action((x, y))
                search_images = img_name == "chest"  # click chests quicker
                break


if __name__ == "__main__":
    main()
