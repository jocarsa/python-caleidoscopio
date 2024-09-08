import cv2
import numpy as np
import os
import time

# Constants
width, height = 1920, 1080
fps = 30
duration_seconds = 10  # Duration of the video in seconds
brush_size = 30

# Calculate the total number of frames
total_frames = fps * duration_seconds

# Create a render directory if it doesn't exist
os.makedirs("render", exist_ok=True)

# Generate the filename using the current epoch time
filename = f"render/{int(time.time())}.mp4"

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

# Initial brush position, direction, and speed
x, y = width // 2, height // 2
speed = 5
direction = np.random.uniform(0, 2 * np.pi)  # Random direction in radians

# Function to update direction smoothly
def update_direction(direction, rate=0.1):
    direction_change = np.random.uniform(-rate, rate)
    return direction + direction_change

# Initialize the canvas
canvas = np.zeros((height, width, 3), dtype=np.uint8)

for _ in range(total_frames):
    # Update the direction smoothly
    direction = update_direction(direction)

    # Calculate the new position
    x += int(speed * np.cos(direction))
    y += int(speed * np.sin(direction))

    # Bounce off the borders
    if x <= brush_size or x >= width - brush_size:
        direction = np.pi - direction
    if y <= brush_size or y >= height - brush_size:
        direction = -direction

    # Ensure the brush stays within bounds
    x = np.clip(x, brush_size, width - brush_size)
    y = np.clip(y, brush_size, height - brush_size)

    # Draw the brush on the canvas, leaving a trail
    color = (255, 0, 0)  # Blue brush
    cv2.circle(canvas, (x, y), brush_size, color, -1)

    # Write the frame to the video file
    out.write(canvas)

# Release the VideoWriter object
out.release()

print(f"Video saved as {filename}")
