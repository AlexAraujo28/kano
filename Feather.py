import asyncio
import tkinter as tk
from tkinter import scrolledtext
from PIL import ImageTk, Image
from threading import Thread
from bleak import BleakScanner, BleakClient

async def search_for_kano_wand(textbox, image_label):
    while True:
        textbox.insert(tk.END, "Searching for Kano Wand...\n")
        devices = await BleakScanner.discover()
        kano_wands = [device for device in devices if "Kano-Wand" in str(device)]
        if kano_wands:
            for wand in kano_wands:
                textbox.insert(tk.END, f"Found Kano Wand: {wand.address}\n")
                success = await connect_to_wand(wand.address, textbox, image_label)
                if success:
                    textbox.insert(tk.END, "Connection to Kano Wand successful.\n")
                else:
                    textbox.insert(tk.END, "Failed to connect to Kano Wand.\n")
            textbox.insert(tk.END, f"Found {len(kano_wands)} Kano Wand(s).\n")
            break
        else:
            textbox.insert(tk.END, "No Kano Wand found. Retrying...\n")
            await asyncio.sleep(5)

async def connect_to_wand(wand_address, textbox, image_label):
    try:
        async with BleakClient(wand_address) as client:
            await detect_gestures(client, textbox, image_label)
            return True
    except Exception as e:
        textbox.insert(tk.END, f"Failed to connect: {e}\n")
        return False

async def detect_gestures(client, textbox, image_label):
    while True:
        # Read data from the Kano Wand to detect gestures
        # Implement this part based on the Kano Wand's API or protocol
        gesture = await read_gesture_data(client)
        if gesture:
            # Map gestures to feather movement
            move_feather_based_on_gesture(gesture, image_label)
        await asyncio.sleep(0.1)  # Adjust the sleep duration as needed

async def read_gesture_data(client):
    # Read data from the Kano Wand to detect gestures
    # Implement this part based on the Kano Wand's API or protocol
    # Return the detected gesture
    pass

def move_feather_based_on_gesture(gesture, image_label):
    # Map gestures to feather movement
    # Update the position of the feather image label based on the detected gesture
    pass

def search_and_connect_gui():
    window = tk.Tk()
    window.title("Kano Wand Search")
    window.geometry('800x400')

    textbox = scrolledtext.ScrolledText(window, width=40, height=10)
    textbox.grid(column=0, row=0)

    image_frame = tk.Frame(window)
    image_frame.grid(column=1, row=0)

    img = Image.open("feather.png")
    img = img.resize((100, 100))  # Resize without anti-aliasing
    img = ImageTk.PhotoImage(img)

    image_label = tk.Label(image_frame, image=img)
    image_label.image = img
    image_label.pack()

    async def start_search():
        await search_for_kano_wand(textbox, image_label)

    def start_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_search())

    search_thread = Thread(target=start_loop)
    search_thread.start()

    window.mainloop()

if __name__ == "__main__":
    search_and_connect_gui()
