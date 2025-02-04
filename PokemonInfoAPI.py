"""
Members of JHM pokedex:

    James Brian Cullantes
    Hugo Arabia
    Marianne Maligang
"""


import tkinter as tk            # import tkinter libray for GUI
from tkinter import messagebox  # import messagebox for error handling
import requests                 # import requests library for API requests
from io import BytesIO          # import BytesIO for handling binary data
from PIL import Image, ImageTk  # Pillow library for handling images


def fetch_pokemon_info(): 
    pokemon_name = entry.get().lower() 
    if not pokemon_name:
        messagebox.showerror("Error", "Please enter a Pokémon name.")
        return

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    try:
        response = requests.get(url) 
        response.raise_for_status() 
        data = response.json() 
        
        name = data['name'].capitalize()
        id_ = data['id']
        types = ", ".join([t['type']['name'].capitalize() for t in data['types']])
        height = data['height']
        weight = data['weight']
        sprite_url = data['sprites']['front_default']  # Fetch the front sprite URL

        # for text info
        result_text = (f"Name: {name}\n"
                       f"ID: {id_}\n"
                       f"Type(s): {types}\n"
                       f"Height: {height / 10} m\n"
                       f"Weight: {weight / 10} kg")
        result_label.config(text=result_text)

        # Fetch and display Pokémon image
        if sprite_url:
            sprite_response = requests.get(sprite_url)
            sprite_response.raise_for_status()
            sprite_data = Image.open(BytesIO(sprite_response.content))
            sprite_data = sprite_data.resize((200, 200), Image.Resampling.LANCZOS)  
            sprite_image = ImageTk.PhotoImage(sprite_data)
            image_label.config(image=sprite_image, highlightbackground="black", highlightthickness=2)  #  black border
            image_label.image = sprite_image  # Keep a reference to avoid garbage collection
        else:
            image_label.config(image=None)
            image_label.image = None

    except requests.exceptions.HTTPError:
        messagebox.showerror("Error", "Pokémon not found. Please try another name.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# GUI Setup
root = tk.Tk()
root.title("Pokémon Info Finder")
root.attributes('-fullscreen', True)  # Enable fullscreen mode

# for  background image
canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

image = Image.open("pokemon1.jpg")  # Open the image using PIL
background_image = ImageTk.PhotoImage(image)  # Replace with your background image file
canvas.create_image(0, 0, anchor="nw", image=background_image)

# Centered widgets
label = tk.Label(root, text="Enter Pokémon Name:", font=("Arial", 24), bg="white", fg="black", highlightbackground="black", highlightthickness=2)
entry = tk.Entry(root, font=("Arial", 20), width=30, highlightbackground="black", highlightthickness=2)
search_button = tk.Button(root, text="Search", command=fetch_pokemon_info, font=("Arial", 18), bg="white", relief="solid", highlightbackground="black", highlightthickness=2)
result_label = tk.Label(root, text="", font=("Arial", 18), justify="left", bg="white", fg="black", highlightbackground="black", highlightthickness=2)
image_label = tk.Label(root, bg="white", highlightbackground="black", highlightthickness=2)

# Function to bind Enter key
def on_enter_key(event):
    fetch_pokemon_info()

# Bind Enter key to the Entry widget
entry.bind("<Return>", on_enter_key)

# Place widgets on the canvas
canvas.create_window(root.winfo_screenwidth()//2, 100, window=label)
canvas.create_window(root.winfo_screenwidth()//2, 180, window=entry)
canvas.create_window(root.winfo_screenwidth()//2, 260, window=search_button)
canvas.create_window(root.winfo_screenwidth()//2, 360, window=result_label)  # Increased the coordinate for spacing
canvas.create_window(root.winfo_screenwidth()//2, 600, window=image_label)

# exit functionality
def exit_fullscreen(event):
    root.attributes('-fullscreen', False)

root.bind("<Escape>", exit_fullscreen)  # Press 'Escape' to exit fullscreen

# Start the GUI loop
root.mainloop()
