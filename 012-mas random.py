import cv2
import numpy as np
import os
import time
import random

# Constants
width, height = 1280, 720
fps = 60
duration_seconds = 60*1  # Duration of the video in seconds
min_brush_size, max_brush_size = 15, 60  # Variable brush size range

# Calculate the total number of frames
total_frames = fps * duration_seconds

# Create a render directory if it doesn't exist
os.makedirs("render", exist_ok=True)

# Generate the filename using the current epoch time
filename = f"render/{int(time.time())}.mp4"

# Create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

# Center of the canvas
cx, cy = width // 2, height // 2

# Initialize the canvas
canvas = np.zeros((height, width, 3), dtype=np.uint8)

# Number of kaleidoscope segments
num_segments = 8

# Function to calculate smooth color transition with randomness
def calculate_color(frame_number):
    # Add randomness to the color transition
    r = int((np.sin(frame_number * 0.02 + random.uniform(-0.1, 0.1)) + 1) * 127.5)
    g = int((np.sin(frame_number * 0.02 + 2 * np.pi / 3 + random.uniform(-0.1, 0.1)) + 1) * 127.5)
    b = int((np.sin(frame_number * 0.02 + 4 * np.pi / 3 + random.uniform(-0.1, 0.1)) + 1) * 127.5)
    return (r, g, b)

# Function to draw mirrored segments with some randomness in angle
def draw_mirrored_segments(x, y, canvas, color, brush_size):
    for i in range(num_segments):
        angle = i * (2 * np.pi / num_segments) + random.uniform(-0.1, 0.1)  # Slight random angle shift
        # Calculate the rotated positions
        x_rot = int(np.cos(angle) * (x - cx) - np.sin(angle) * (y - cy) + cx)
        y_rot = int(np.sin(angle) * (x - cx) + np.cos(angle) * (y - cy) + cy)
        cv2.circle(canvas, (x_rot, y_rot), brush_size, color, -1)

# Start time of rendering
start_time = time.time()

for frame_number in range(total_frames):
    # Elliptic parameters with added randomness
    a = 200 + 60 * np.sin(frame_number * 0.01) + random.uniform(-20, 20)  # Semi-major axis
    b = 10 + 35 * np.cos(frame_number * 0.01) + random.uniform(-10, 10)   # Semi-minor axis
    angle = frame_number * 0.02 + random.uniform(-0.1, 0.1)  # Angle to rotate the ellipse with randomness

    # Calculate the position on the ellipse
    x = int(cx + a * np.cos(angle))
    y = int(cy + b * np.sin(angle))

    # Rotate the ellipse around the center with random rotation angle
    rotation_angle = frame_number * 0.01 + random.uniform(-0.1, 0.1)  # Randomized rotation angle
    x_rot = int(np.cos(rotation_angle) * (x - cx) - np.sin(rotation_angle) * (y - cy) + cx)
    y_rot = int(np.sin(rotation_angle) * (x - cx) + np.cos(rotation_angle) * (y - cy) + cy)

    # Calculate the color for this frame with some randomness
    color = calculate_color(frame_number)

    # Randomize brush size
    brush_size = random.randint(min_brush_size, max_brush_size)

    # Draw the brush and its mirrored segments on the canvas
    draw_mirrored_segments(x_rot, y_rot, canvas, color, brush_size)

    # Write the frame to the video file
    out.write(canvas)

    # Calculate statistics every second (every 'fps' frames)
    if frame_number % fps == 0:
        elapsed_time = time.time() - start_time
        frames_remaining = total_frames - frame_number
        time_remaining = (frames_remaining / fps) / 60  # In minutes
        estimated_finish = time.time() + frames_remaining / fps
        percentage_complete = (frame_number / total_frames) * 100
        
        print(f"Time Elapsed: {elapsed_time:.2f} seconds")
        print(f"Time Remaining: {time_remaining:.2f} minutes")
        print(f"Estimated Time of Finish: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(estimated_finish))}")
        print(f"Completion: {percentage_complete:.2f}%\n")

# Release the VideoWriter object
out.release()

print(f"Video saved as {filename}")
