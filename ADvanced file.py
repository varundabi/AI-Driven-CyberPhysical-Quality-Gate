import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim


def get_first_valid_image(folder_path):
    """Safely retrieves the absolute path of the first image file in a directory, handling .tif extensions."""
    if not os.path.exists(folder_path):
        print(f"❌ Target path does not exist on your system: {folder_path}")
        return None

    # Updated filter to explicitly look for your Solid Edge .tif files
    files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))])

    if len(files) == 0:
        print(f"⚠️ No images found inside folder: {folder_path}")
        return None

    chosen_file = os.path.join(folder_path, files[0])
    print(f"📁 Successfully targeted image: {chosen_file}")
    return chosen_file


def inspect_and_visualize(perfect_path, defect_path, defect_title, save_name):
    if perfect_path is None or defect_path is None:
        return

    # 1. Load Images
    img_perf = cv2.imread(perfect_path)
    img_def = cv2.imread(defect_path)

    if img_perf is None or img_def is None:
        print(f"❌ OpenCV failed to read the images for {defect_title}.")
        return

    # Resize to standard resolution for precise structural comparison
    img_perf = cv2.resize(img_perf, (640, 480))
    img_def = cv2.resize(img_def, (640, 480))

    gray_perf = cv2.cvtColor(img_perf, cv2.COLOR_BGR2GRAY)
    gray_def = cv2.cvtColor(img_def, cv2.COLOR_BGR2GRAY)

    # 2. Compute Structural Similarity Index (SSIM)
    score, diff = ssim(gray_perf, gray_def, full=True)
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image to isolate geometric changes
    _, thresh = cv2.threshold(diff, 180, 255, cv2.THRESH_BINARY_INV)

    # Clean up image noise using morphology filtering
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # 3. Find contours of the defect regions
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    output_img = img_def.copy()
    defect_count = 0

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 50:  # Filter out minor rendering artifacts or light reflections
            continue

        defect_count += 1
        # Calculate bounding circle dimensions around the structural delta
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius) + 15  # Visual padding around the defect zone

        # Draw a bright red circle around the anomaly
        cv2.circle(output_img, center, radius, (0, 0, 255), 3)

        # Place label text next to the marker
        cv2.putText(output_img, f"DEFECT {defect_count}", (center[0] - radius, center[1] - radius - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # 4. Render the comparative inspection window panel
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    perf_rgb = cv2.cvtColor(img_perf, cv2.COLOR_BGR2RGB)
    out_rgb = cv2.cvtColor(output_img, cv2.COLOR_BGR2RGB)

    axes[0].imshow(perf_rgb)
    axes[0].set_title("Master Template (Perfect Assembly)", fontsize=12, fontweight='bold')
    axes[0].axis('off')

    axes[1].imshow(out_rgb)
    axes[1].set_title(f"Production Scan: {defect_title}\n({defect_count} Anomalies Detected)", fontsize=12,
                      fontweight='bold', color='red')
    axes[1].axis('off')

    plt.tight_layout()
    plt.savefig(save_name, dpi=300)
    print(f"🌟 Visual Report Saved Successfully: '{save_name}'\n")
    plt.show()


if __name__ == '__main__':
    print("--- Directly Querying Source Folders for Image Assets ---\n")

    # Direct paths to your original Solid Edge output folders
    PATH_VENT = fr"C:\Users\Varun Raju Dabi\Desktop\ALL SUBJECTS\CAX\Poka Yoke  inetrgation project\PAck shots VENT"
    PATH_DEFECT1 = fr"C:\Users\Varun Raju Dabi\Desktop\ALL SUBJECTS\CAX\Poka Yoke  inetrgation project\PAck shots VENT Defect 1"
    PATH_DEFECT2 = fr"C:\Users\Varun Raju Dabi\Desktop\ALL SUBJECTS\CAX\Poka Yoke  inetrgation project\PAck shots VENT Defect 2"
    PATH_DEFECT3 = fr"C:\Users\Varun Raju Dabi\Desktop\ALL SUBJECTS\CAX\Poka Yoke  inetrgation project\PAck shots VENT Defect 3"

    # Automatically fetch the first available image from each directory
    perfect_img = get_first_valid_image(PATH_VENT)
    defect_1_img = get_first_valid_image(PATH_DEFECT1)
    defect_2_img = get_first_valid_image(PATH_DEFECT2)
    defect_3_img = get_first_valid_image(PATH_DEFECT3)

    print("\n--- Running Comparative Computer Vision Metrology Loop ---")

    inspect_and_visualize(perfect_img, defect_1_img, "Missing Bolt Assembly Error", "report_missing_bolt.png")
    inspect_and_visualize(perfect_img, defect_2_img, "Sharp Edges / Missing Corner Radius", "report_sharp_edges.png")
    inspect_and_visualize(perfect_img, defect_3_img, "Incorrect Bolt Length Specification", "report_bolt_length.png")