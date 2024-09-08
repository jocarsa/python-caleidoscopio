import cv2
import numpy as np
import os
import time

# Constants
width, height = 1280, 720
fps = 30
duration_seconds = 60  # Duration of the video in seconds
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

# Function to update direction smoothly with a bias towards the center
def update_direction(x, y, direction, rate=0.1, center_bias=0.02):
    direction_change = np.random.uniform(-rate, rate)
    direction += direction_change

    # Calculate the bias towards the center
    cx, cy = width // 2, height // 2
    dx = cx - x
    dy = cy - y
    distance = np.sqrt(dx**2 + dy**2)
    
    # Apply a bias based on the distance from the center
    bias_direction = np.arctan2(dy, dx)
    direction = (1 - center_bias) * direction + center_bias * bias_direction

    return direction

# Initialize the canvas
canvas = np.zeros((height, width, 3), dtype=np.uint8)

# Number of kaleidoscope segments
num_segments = 8

# Function to calculate smooth color transition
def calculate_color(frame_number):
    # Use sine functions to smoothly transition through RGB colors
    r = int((np.sin(frame_number * 0.02) + 1) * 127.5)
    g = int((np.sin(frame_number * 0.02 + 2 * np.pi / 3) + 1) * 127.5)
    b = int((np.sin(frame_number * 0.02 + 4 * np.pi / 3) + 1) * 127.5)
    return (r, g, b)

# Function to draw mirrored segments
def draw_mirrored_segments(x, y, canvas, color):
    cx, cy = width // 2, height // 2  # Center of the canvas
    for i in range(num_segments):
        angle = i * (2 * np.pi / num_segments)
        # Calculate the rotated positions
        x_rot = int(np.cos(angle) * (x - cx) - np.sin(angle) * (y - cy) + cx)
        y_rot = int(np.sin(angle) * (x - cx) + np.cos(angle) * (y - cy) + cy)
        cv2.circle(canvas, (x_rot, y_rot), brush_size, color, -1)

for frame_number in range(total_frames):
    # Update the direction smoothly with a bias towards the center
    direction = update_direction(x, y, direction)

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

    # Calculate the color for this frame
    color = calculate_color(frame_number)

    # Draw the brush and its mirrored segments on the canvas
    draw_mirrored_segments(x, y, canvas, color)

    # Write the frame to the video file
    out.write(canvas)

# Release the VideoWriter object
out.release()

print(f"Video saved as {filename}")
