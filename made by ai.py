import cv2

# 1. Capture Video Stream
cap = cv2.VideoCapture(0) # Use 0 for webcam, or provide a video file path

# 2. Read Initial Frame (Reference Frame)
ret, frame1 = cap.read()
if not ret:
    print("Failed to read initial frame.")
    exit()

gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray_frame1 = cv2.GaussianBlur(gray_frame1, (21, 21), 0)

while True:
    # 3. Process Subsequent Frames
    ret, frame2 = cap.read()
    if not ret:
        break

    gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray_frame2 = cv2.GaussianBlur(gray_frame2, (21, 21), 0)

    # Calculate absolute difference
    diff = cv2.absdiff(gray_frame1, gray_frame2)

    # Apply threshold
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # Dilate the thresholded image to fill holes
    dilated = cv2.dilate(thresh, None, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 500:  # Adjust this threshold as needed
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Motion Detection", frame2)
    gray_frame1 = gray_frame2  # Update previous frame

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 4. Release Resources
cap.release()
cv2.destroyAllWindows()