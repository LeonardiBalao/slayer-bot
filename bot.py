import cv2
import pyautogui
from PIL import ImageGrab
import numpy as np
import time
import threading

# Paths to image files
close_button_path = './assets/close.png'
chest_path = './assets/chest.png'
activate_button_path = './assets/activate.png'
right = './assets/right.png'
left = './assets/left.png'
close_button_path2 = './assets/close2.png'

paused = False 

def capture_game_window():    
    screenshot = ImageGrab.grab()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2RGB)
    return screenshot

def find_image_color(game_window, image_path, threshold=0.8  ):
    template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    game_window = cv2.cvtColor(game_window, cv2.COLOR_BGR2GRAY).astype(np.uint8)
    template = cv2.cvtColor(template, cv2.COLOR_BGRA2GRAY).astype(np.uint8)
    
    res = cv2.matchTemplate(game_window, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        return pt
    return None

def attack():
    for _ in range(9):
        pyautogui.keyDown('space')
        pyautogui.keyUp('space')
        # Alternate attack mode
        # pyautogui.press('d')
        
def listen_for_pause_key():
    global paused
    while True:
        if pyautogui.hotkey('p'):
            paused = not paused
            if paused:
                print("Script paused. Press 'p' to resume.")
            else:
                print("Script resumed. Press 'p' to pause.")
            time.sleep(3)  # Small delay to debounce key press
            
def listen_for_dash():
    while True:
        pyautogui.press('d')
    
# Main function
def main():
    threading.Thread(target=listen_for_dash, daemon=True).start()
    while True:
        if not paused:
            game_window = capture_game_window()
            close_button_pos = find_image_color(game_window, close_button_path)
            close_button_pos2 = find_image_color(game_window, close_button_path2)
            chest_pos = find_image_color(game_window, chest_path)
            activate_button_pos = find_image_color(game_window, activate_button_path)
            left_pos = find_image_color(game_window, left)
            right_pos = find_image_color(game_window, right)
            
            # Bonus Stage Prompt
            if right_pos:
                pyautogui.moveTo(right_pos[0] + 50, right_pos[1] + 50)
                pyautogui.mouseDown()
                pyautogui.dragTo(right_pos[0] + 700, right_pos[1] + 50, duration=2)  # Drag to the right by 300 pixels
                pyautogui.mouseUp()
            
            # Bonus Stage Prompt
            if left_pos:
                pyautogui.moveTo(left_pos[0] + 50, left_pos[1] + 50)
                pyautogui.mouseDown()
                pyautogui.dragTo(left_pos[0] - 700, left_pos[1] + 50, duration=2)
                pyautogui.mouseUp()
                
            # Close Bonus Stage on Second Wind
            if close_button_pos2:
                pyautogui.moveTo(close_button_pos2[0] + 50, close_button_pos2[1] + 50)
                pyautogui.click()
                pyautogui.click()
                pyautogui.click()

            # Activate Bonus
            if activate_button_pos:
                pyautogui.moveTo(activate_button_pos[0] + 50, activate_button_pos[1] + 50)
                pyautogui.click()
                pyautogui.click()
                pyautogui.click()

            # Close Chest Hunt
            if close_button_pos:
                pyautogui.moveTo(close_button_pos[0] + 50, close_button_pos[1] + 50)
                pyautogui.click()
            
            # Open Chests
            if chest_pos:
                print('Chest spotted!')
                pyautogui.moveTo(chest_pos[0] + 50, chest_pos[1] + 50)
                pyautogui.click()
        
            # Attack every iteration
            attack()
            time.sleep(0.01)  # Small sleep to prevent CPU overuse
        else:
            time.sleep(5)
            print("Sleeping...")

if __name__ == "__main__":
    main()
