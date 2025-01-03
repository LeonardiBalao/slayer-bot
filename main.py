import pyautogui # type: ignore
import time

def press_keys():
    last_space_time = 0
    last_d_time = 0
    space_interval = 5  # 5 seconds interval for space bar
    d_interval = 0.1  # 100 ms interval for 'd' key

    while True:
        current_time = time.time()
        
        if current_time - last_space_time >= space_interval:
            pyautogui.press('space')  # Press the space bar
            last_space_time = current_time
        
        if current_time - last_d_time >= d_interval:
            pyautogui.press('d')  # Press the 'd' key
            last_d_time = current_time

        time.sleep(0.01)  # Small sleep to prevent CPU overuse

if __name__ == "__main__": 
    press_keys()
