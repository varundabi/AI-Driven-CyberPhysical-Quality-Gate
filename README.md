AI-Driven Cyber-Physical Quality Gate (Poka-Yoke Implementation)
AI-driven Industry 4.0 quality gate blending CAD automation (Solid Edge API), PyTorch deep learning triage, and precise OpenCV homography metrology.

🛠️ Technology Stack
* **CAD Generation:** Solid Edge API, Python `win32com`
* **Deep Learning Neural Network:** PyTorch, Torchvision (`MobileNetV3`)
* **Computer Vision & Metrology:** OpenCV (`ORB Keypoints`, `Homography`), Scikit-Image (`SSIM`), Matplotlib, Seaborn

📐 System Architecture & RAMI 4.0 Mapping

The project is structured across the core layers of the Reference Architectural Model Industry 4.0:

1. **Asset Layer:** The physical component configurations (Master Plate, Missing Bolts, Profile Deviations) modeled in CAD.
2. **Integration Layer:** Automated script capturing multi-angle camera views (`.png.tif`) using programmatic camera orbits.
3. **Information Layer:** A lightweight, high-performance `MobileNetV3` network acting as a fast-triage sorting gate on the conveyor line.
4. **Functional Layer:** An advanced vision pipeline that matches camera perspectives via **ORB Homography** and uses **SSIM** to isolate localized anomalies.
