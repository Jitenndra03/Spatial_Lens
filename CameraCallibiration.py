import cv2
import numpy as np

# Chessboard configuration
chessboard_size = (7, 7)  # inner corners
square_size = 0.025       # 25mm = 0.025m

# Prepare object points based on real-world layout
objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2) * square_size

# Storage for calibration points
obj_points = []  # 3D world points
img_points = []  # 2D image points

# Start webcam
cap = cv2.VideoCapture(0)

print("Press SPACE to capture a frame when corners are visible.")
print("Press ESC to perform calibration and exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    display_frame = frame.copy()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect corners
    ret_corners, corners = cv2.findChessboardCorners(gray, chessboard_size, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE)

    if ret_corners:
        cv2.drawChessboardCorners(display_frame, chessboard_size, corners, ret_corners)
        cv2.putText(display_frame, "Press SPACE to capture", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # Show frame
    cv2.imshow("Live Calibration", display_frame)
    key = cv2.waitKey(1)

    if key == 27:  # ESC key
        break
    elif key == 32 and ret_corners:  # SPACE key
        obj_points.append(objp.copy())
        img_points.append(corners)
        print(f"[INFO] Captured frame {len(obj_points)}")

# Cleanup
cap.release()
cv2.destroyAllWindows()

# Perform calibration if enough frames
if len(obj_points) >= 10:
    ret, camera_matrix, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
        obj_points, img_points, gray.shape[::-1], None, None
    )

    if ret:
        print("\n✅ Camera calibration successful!")
        print("Camera Matrix:\n", camera_matrix)
        print("Distortion Coefficients:\n", dist_coeffs)
        # Save for later
        np.savez("live_camera_calibration.npz",
                 camera_matrix=camera_matrix,
                 distortion_coeffs=dist_coeffs,
                 rvecs=rvecs,
                 tvecs=tvecs)
        print("Results saved to 'live_camera_calibration.npz'")
    else:
        print("❌ Calibration failed.")
else:
    print("⚠️ Not enough valid captures to calibrate (need at least 10).")
