import tkinter as tk
import math
import random # Import random for stars

# --- Window Setup ---
root = tk.Tk()
root.title("📡 Realistic Satellite Orbiting Earth")
canvas_width = 600
canvas_height = 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="black")
canvas.pack()

# --- Star Field Setup ---
NUM_STARS = 150 # Number of stars to draw
stars = []
for _ in range(NUM_STARS):
    stars.append((random.randint(0, canvas_width), random.randint(0, canvas_height)))

# --- Earth Setup ---
earth_radius = 80 # Increased Earth size for better detail
earth_x = canvas_width // 2
earth_y = canvas_height // 2

earth_elements = [] # List to store Earth's canvas IDs

# Base ocean layer
earth_elements.append(canvas.create_oval(
    earth_x - earth_radius, earth_y - earth_radius,
    earth_x + earth_radius, earth_y + earth_radius,
    fill="#000080", # Deep Ocean Blue
    outline="#ADD8E6", # Light Blue for subtle atmospheric glow
    width=2
))
# Lighter ocean shades / shallow waters
earth_elements.append(canvas.create_oval(
    earth_x - earth_radius * 0.95, earth_y - earth_radius * 0.95,
    earth_x + earth_radius * 0.95, earth_y + earth_radius * 0.95,
    fill="#0022AA", # Medium Ocean Blue
    outline=""
))
# Landmasses (simple, abstract shapes)
earth_elements.append(canvas.create_oval(
    earth_x - earth_radius * 0.7, earth_y - earth_radius * 0.8,
    earth_x + earth_radius * 0.1, earth_y - earth_radius * 0.4,
    fill="#228B22", # Forest Green
    outline=""
))
earth_elements.append(canvas.create_oval(
    earth_x + earth_radius * 0.2, earth_y + earth_radius * 0.3,
    earth_x + earth_radius * 0.8, earth_y + earth_radius * 0.7,
    fill="#228B22", # Forest Green
    outline=""
))
earth_elements.append(canvas.create_oval(
    earth_x - earth_radius * 0.8, earth_y + earth_radius * 0.1,
    earth_x - earth_radius * 0.3, earth_y + earth_radius * 0.5,
    fill="#8B4513", # Saddle Brown for deserts/mountains
    outline=""
))
# Polar ice caps (simple white ovals)
earth_elements.append(canvas.create_oval(
    earth_x - earth_radius * 0.4, earth_y - earth_radius * 0.9,
    earth_x + earth_radius * 0.4, earth_y - earth_radius * 0.7,
    fill="white", outline=""
))
earth_elements.append(canvas.create_oval(
    earth_x - earth_radius * 0.4, earth_y + earth_radius * 0.7,
    earth_x + earth_radius * 0.4, earth_y + earth_radius * 0.9,
    fill="white", outline=""
))

earth_text_id = canvas.create_text(earth_x, earth_y + earth_radius + 15, 
                        text="Earth", fill="white", font=("Arial", 10, "bold"))
earth_elements.append(earth_text_id) # Add text ID to earth_elements

# --- Satellite Orbit Settings ---
orbit_radius = 200 # Adjusted orbit radius to accommodate larger Earth
angle = 0 # Current angle in degrees
SATELLITE_ORBIT_SPEED = 1 # New variable for satellite speed (degrees per frame)

# --- Satellite Drawing: More realistic shape ---

sat_body_size = 15
# Solar panel dimensions
panel_length = 30
panel_width = 10

body = canvas.create_rectangle(0, 0, 0, 0, fill="#808080", outline="white", width=1) 
# Left solar panel
left_panel = canvas.create_rectangle(0, 0, 0, 0, fill="#4B0082", outline="#8A2BE2", width=1) 
# Right solar panel
right_panel = canvas.create_rectangle(0, 0, 0, 0, fill="#4B0082", outline="#8A2BE2", width=1)
# Communication Dish (small circle)
dish_radius = 5
dish_antenna = canvas.create_oval(0, 0, 0, 0, fill="silver", outline="gray", width=1)
# Boom arm for the dish (line)
boom_arm = canvas.create_line(0, 0, 0, 0, fill="silver", width=1)
# Small thrusters (simple rectangles)
thruster_left = canvas.create_rectangle(0, 0, 0, 0, fill="darkgray", outline="gray", width=1)
thruster_right = canvas.create_rectangle(0, 0, 0, 0, fill="darkgray", outline="gray", width=1)

# List of all satellite parts for easy management
satellite_parts = [body, left_panel, right_panel, dish_antenna, boom_arm, thruster_left,
                    thruster_right]


# --- Animation Function ---
def animate():
    global angle

    # This prevents flickering of the Earth
    for item in stars_on_canvas: # Delete existing stars
        canvas.delete(item)
    
    for item_id in earth_elements:
        canvas.tag_raise(item_id) 

    stars_on_canvas.clear() 
    for x, y in stars:
        stars_on_canvas.append(canvas.create_oval(x, y, x + 1, y + 1,
                                                   fill="white", outline="white"))


    rad = math.radians(angle)
    sat_center_x = earth_x + orbit_radius * math.cos(rad)
    sat_center_y = earth_y + orbit_radius * math.sin(rad)

    # Satellite body
    canvas.coords(
        body,
        sat_center_x - sat_body_size // 2, sat_center_y - sat_body_size // 2,
        sat_center_x + sat_body_size // 2, sat_center_y + sat_body_size // 2
    )

    # Solar panels (positioned relative to the body)
    # Left solar panel
    canvas.coords(
        left_panel,
        sat_center_x - sat_body_size // 2 - panel_length, sat_center_y - panel_width // 2,
        sat_center_x - sat_body_size // 2, sat_center_y + panel_width // 2
    )

    # Right solar panel
    canvas.coords(
        right_panel,
        sat_center_x + sat_body_size // 2, sat_center_y - panel_width // 2,
        sat_center_x + sat_body_size // 2 + panel_length, sat_center_y + panel_width // 2
    )

    # Dish is slightly offset from the top-right of the main body
    dish_x = sat_center_x + sat_body_size // 2 + dish_radius
    dish_y = sat_center_y - sat_body_size // 2 - dish_radius
    canvas.coords(
        dish_antenna,
        dish_x - dish_radius, dish_y - dish_radius,
        dish_x + dish_radius, dish_y + dish_radius
    )
    # Boom arm connects dish to main body
    canvas.coords(
        boom_arm,
        sat_center_x + sat_body_size // 2, sat_center_y - sat_body_size // 2, # Connects to top-right corner of body
        dish_x - dish_radius * 0.7, dish_y + dish_radius * 0.7 # Connects to dish (approx center)
    )

    # Thrusters (small rectangles at corners of body)
    canvas.coords(
        thruster_left,
        sat_center_x - sat_body_size // 2 - 5, sat_center_y + sat_body_size // 2 - 5,
        sat_center_x - sat_body_size // 2, sat_center_y + sat_body_size // 2
    )
    canvas.coords(
        thruster_right,
        sat_center_x + sat_body_size // 2, sat_center_y + sat_body_size // 2 - 5,
        sat_center_x + sat_body_size // 2 + 5, sat_center_y + sat_body_size // 2
    )

    # Bring satellite parts to the front
    for part in satellite_parts:
        canvas.tag_raise(part)

    angle = (angle + SATELLITE_ORBIT_SPEED) % 360 # Use SATELLITE_ORBIT_SPEED
    canvas.after(50, animate) # Animation delay

# --- Title ---
canvas.create_text(canvas_width//2, 30, text="📡 Satellite Orbiting Earth", fill="white", 
                   font=("Arial", 16, "bold"))

# List to store star IDs created in animate()
stars_on_canvas = []

# --- Start Animation ---
animate()
root.mainloop()
