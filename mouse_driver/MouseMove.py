import mouse_driver.ghub_mouse as ghub
import pyautogui

def ghub_mouse_move(rel_x, rel_y):
    ghub.mouse_xy(round(rel_x), round(rel_y))

def pygui_mouse_move(rel_x, rel_y):
    pyautogui.moveRel(rel_x, rel_y)

if __name__ == "__main__":
    import time
    trials = 1000
    start_time = time.time()
    for i in range(trials):
        ghub.mouse_down()
        ghub.mouse_up()
        # ghub_mouse_move(1000,0)
        # ghub_mouse_move(-1000,0)
        time.sleep(0.01)
    ghub.mouse_done()
    ghub.mouse_up()
    now_time = time.time()
    fps = trials / (now_time - start_time)
    print("time is ", now_time - start_time)
    print("fps is ", fps)
