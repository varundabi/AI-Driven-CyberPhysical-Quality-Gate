import win32com.client
import time
import math

application = win32com.client.GetActiveObject("SolidEdge.Application")
window = application.ActiveWindow
view = window.View

# Let's increase the shots to 150 to ensure we capture a dense 360-degree global sphere
total_shots = 150

for i in range(total_shots):
    # 1. Horizontal rotation step (Yaw) - continuous spinning around the Y-axis
    # (2.4 degrees * 150 shots = 360 degrees full rotation)
    view.RotateCamera(2.4, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0)

    # 2. Vertical tilt step (Pitch) - uses a sine wave pattern to smoothly
    # tilt the camera up and down between -30 and +30 degrees as it spins
    tilt_angle = 10 * math.sin(i * 0.2)
    view.RotateCamera(tilt_angle, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)  # Rotates on X-axis

    # Keep the part perfectly locked in the center of the viewport
    view.Fit()

    # Your dataset path configuration
    image_path = fr"C:\Users\Varun Raju Dabi\Desktop\ALL SUBJECTS\CAX\Poka Yoke  inetrgation project\PAck shots VENT Defect 3\img_{i}.png"

    # Save the frame
    view.SaveAsImage(image_path, Width=1920, Height=1080)

    time.sleep(0.05)  # Lowered sleep slightly so 150 frames renders faster