import config
import pyautogui
import threading
import tkinter as tk
import win32gui
import time

WINDOW_TITLE = "Ragnarok"
CONFIDENCE = 0.6


def main():
    windows = pyautogui.getWindowsWithTitle(WINDOW_TITLE)
    if not windows:
        print("Window not found.")
        return
    hwnd = windows[0]._hWnd
    if not hwnd:
        print("Window not found.")
        return

    (x1, y1, x2, y2) = win32gui.GetWindowRect(hwnd)
    width = x2 - x1
    height = y2 - y1

    root = tk.Tk()
    root.geometry(f"{width-16}x{height}+{x1}+{y1-30}")
    root.attributes("-topmost", True)
    root.wm_attributes("-transparentcolor", "pink")
    tk.Frame(root, background="pink").pack(expand=True, fill=tk.BOTH)
    labels = []
    for index, item in enumerate(config.display_skills):
        label = tk.Label(
            font=("", 8, "bold"),
            foreground=item["color"],
            background="pink",
            anchor=tk.NW,
            justify=tk.LEFT,
        )
        label.place(
            x=width // 2, y=height // 2 + 40 + 20 * index, width=width // 3, height=20
        )
        labels.append(label)

    detect = True

    def detector():
        while detect:
            row = 0
            for index, item in enumerate(config.display_skills):
                try:
                    pyautogui.locateOnScreen(
                        item["file_path"],
                        region=(x1 + width // 3 * 2, y1, x2, y2),
                        confidence=CONFIDENCE,
                    )
                    # labels[index].place(y=height // 2 + 20 * row)
                    labels[index]["text"] = item["display_name"]
                    row = row + 1
                except:
                    try:
                        labels[index]["text"] = ""
                    except:
                        pass
            time.sleep(0.05)

    thread = threading.Thread(target=detector)
    thread.start()
    root.mainloop()
    detect = False
    thread.join(10)


main()
