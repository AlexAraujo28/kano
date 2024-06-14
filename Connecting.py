import asyncio
import tkinter as tk
from tkinter import scrolledtext
from bleak import BleakScanner, BleakClient

async def search_for_kano_wand(textbox):
    while True:
        textbox.insert(tk.END, "Searching for Kano Wand...\n")
        devices = await BleakScanner.discover()
        kano_wands = [device for device in devices if "Kano-Wand" in str(device)]
        if kano_wands:
            for wand in kano_wands:
                textbox.insert(tk.END, f"Found Kano Wand: {wand.address}\n")
                success = await connect_to_wand(wand.address, textbox)
                if success:
                    textbox.insert(tk.END, "Connection to Kano Wand successful.\n")
                else:
                    textbox.insert(tk.END, "Failed to connect to Kano Wand.\n")
            textbox.insert(tk.END, f"Found {len(kano_wands)} Kano Wand(s).\n")
            break  # Exit the loop if a Kano Wand is found
        else:
            textbox.insert(tk.END, "No Kano Wand found. Retrying...\n")
            await asyncio.sleep(5)  # Wait for 5 seconds before retrying

async def connect_to_wand(wand_address, textbox):
    try:
        async with BleakClient(wand_address) as client:
            return True
    except Exception as e:
        textbox.insert(tk.END, f"Failed to connect: {e}\n")
        return False

async def search_and_connect_gui():
    window = tk.Tk()
    window.title("Kano Wand Search")
    window.geometry('600x300')

    textbox = scrolledtext.ScrolledText(window, width=40, height=10)
    textbox.grid(column=0, row=0)

    # Automatically start searching for Kano Wands when the app starts
    await search_for_kano_wand(textbox)

    window.mainloop()

if __name__ == "__main__":
    asyncio.run(search_and_connect_gui())
