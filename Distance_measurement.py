import cv2
import numpy as np

# === Load Calibration Data ===
data = np.load("live_camera_calibration.npz")
camera_matrix = data['camera_matrix']
dist_coeffs = data['distortion_coeffs']

# === Real-world diameter of one known circle (in cm) ===
known_diameter_cm = 2.5  # for example, a coin of 2.5 cm diameter

# === Start Webcam ===
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Failed to open camera.")
    exit()

print("Press ESC to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to capture frame.")
        break

    # === Undistort Frame ===
    undistorted = cv2.undistort(frame, camera_matrix, dist_coeffs)

    # === Convert to Grayscale ===
    gray = cv2.cvtColor(undistorted, cv2.COLOR_BGR2GRAY)

    # === Apply Gaussian Blur ===
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # === Optional DEBUG Visuals (RESOLVED) ===
    # cv2.imshow("Undistorted Frame", undistorted)  # Debugging step - resolved
    # cv2.imshow("Grayscale", gray)                # Debugging step - resolved
    # cv2.imshow("Blurred", blurred)               # Debugging step - resolved
    # cv2.imwrite("debug_frame.jpg", blurred)      # Saved for offline analysis - resolved

    # === Detect Circles ===
    circles = cv2.HoughCircles(
        blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
        param1=50, param2=30, minRadius=10, maxRadius=100
    )

    display = undistorted.copy()

    # === Draw Circles and Measure Distance ===
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        for (x, y, r) in circles:
            cv2.circle(display, (x, y), r, (0, 255, 0), 2)
            cv2.circle(display, (x, y), 2, (0, 0, 255), 3)

        if len(circles) >= 2:
            # Estimate pixel-to-cm scale from known diameter
            actual_radius_cm = known_diameter_cm / 2.0
            reference_circle = circles[0]
            pixels_per_cm = reference_circle[2] / actual_radius_cm

            # Compute distance between first two circles
            c1 = np.array([circles[0][0], circles[0][1]])
            c2 = np.array([circles[1][0], circles[1][1]])
            pixel_dist = np.linalg.norm(c2 - c1)
            real_dist_cm = pixel_dist / pixels_per_cm

            # Draw line and label distance
            cv2.line(display, tuple(c1), tuple(c2), (255, 0, 0), 2)
            mid = ((c1[0] + c2[0]) // 2, (c1[1] + c2[1]) // 2)
            cv2.putText(display, f"{real_dist_cm:.2f} cm", mid,
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    else:
        cv2.putText(display, "No circles detected", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # === Show Final Display Window ===
    cv2.imshow("Circular Object Distance", display)

    # === Exit on ESC Key ===
    key = cv2.waitKey(1)
    if key == 27:
        break

# === Clean Up ===
cap.release()
cv2.destroyAllWindows()
