import os
import sys
import glob
import time

import cv2
import numpy as np
from ultralytics import YOLO

# ----------- HARD-CODED CONFIG -----------
model_path = "/home/tanay/final_7pm/LR8n.pt"   # <-- CHANGE if filename differs
img_source = "usb0"
min_thresh = 0.4
user_res = "1280x720"
record = False
# ----------------------------------------

# Check if model file exists
if (not os.path.exists(model_path)):
    print('ERROR: Model path is invalid or model was not found.')
    sys.exit(0)

# Load model
model = YOLO(model_path, task='detect')
labels = model.names

# Determine source type
img_ext_list = ['.jpg','.JPG','.jpeg','.JPEG','.png','.PNG','.bmp','.BMP']
vid_ext_list = ['.avi','.mov','.mp4','.mkv','.wmv']

if os.path.isdir(img_source):
    source_type = 'folder'
elif os.path.isfile(img_source):
    _, ext = os.path.splitext(img_source)
    if ext in img_ext_list:
        source_type = 'image'
    elif ext in vid_ext_list:
        source_type = 'video'
    else:
        print(f'File extension {ext} not supported.')
        sys.exit(0)
elif 'usb' in img_source:
    source_type = 'usb'
    usb_idx = int(img_source[3:])
elif 'picamera' in img_source:
    source_type = 'picamera'
    picam_idx = int(img_source[8:])
else:
    print(f'Invalid input source: {img_source}')
    sys.exit(0)

# Resolution
resize = False
if user_res:
    resize = True
    resW, resH = map(int, user_res.split('x'))

# Recording setup
if record:
    if source_type not in ['video','usb']:
        print('Recording only works for video/USB')
        sys.exit(0)
    if not user_res:
        print('Specify resolution for recording')
        sys.exit(0)

    recorder = cv2.VideoWriter(
        'demo1.avi',
        cv2.VideoWriter_fourcc(*'MJPG'),
        30,
        (resW, resH)
    )

# Load source
if source_type == 'image':
    imgs_list = [img_source]

elif source_type == 'folder':
    imgs_list = []
    for file in glob.glob(img_source + '/*'):
        if os.path.splitext(file)[1] in img_ext_list:
            imgs_list.append(file)

elif source_type in ['video', 'usb']:
    cap_arg = img_source if source_type == 'video' else usb_idx
    cap = cv2.VideoCapture(cap_arg)

    if user_res:
        cap.set(3, resW)
        cap.set(4, resH)

elif source_type == 'picamera':
    from picamera2 import Picamera2
    cap = Picamera2()
    cap.configure(cap.create_video_configuration(
        main={"format": 'RGB888', "size": (resW, resH)}
    ))
    cap.start()

# Colors
bbox_colors = [(164,120,87),(68,148,228),(93,97,209),(178,182,133),
               (88,159,106),(96,202,231),(159,124,168),(169,162,241),
               (98,118,150),(172,176,184)]

# FPS tracking
avg_frame_rate = 0
frame_rate_buffer = []
fps_avg_len = 200
img_count = 0

# ----------- MAIN LOOP -----------
while True:

    t_start = time.perf_counter()

    # Load frame
    if source_type in ['image', 'folder']:
        if img_count >= len(imgs_list):
            print('Done.')
            break
        frame = cv2.imread(imgs_list[img_count])
        img_count += 1

    elif source_type == 'video':
        ret, frame = cap.read()
        if not ret:
            break

    elif source_type == 'usb':
        ret, frame = cap.read()
        if frame is None:
            break

    elif source_type == 'picamera':
        frame = cap.capture_array()
        if frame is None:
            break

    # Resize
    if resize:
        frame = cv2.resize(frame, (resW, resH))

    # Inference
    results = model(frame, verbose=False)
    detections = results[0].boxes

    object_count = 0

    for det in detections:
        xyxy = det.xyxy.cpu().numpy().squeeze().astype(int)
        xmin, ymin, xmax, ymax = xyxy

        classidx = int(det.cls.item())
        classname = labels[classidx]
        conf = det.conf.item()

        if conf > min_thresh:
            color = bbox_colors[classidx % 10]

            cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), color, 2)

            label = f'{classname}: {int(conf*100)}%'
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

            y = max(ymin, h + 10)
            cv2.rectangle(frame, (xmin, y-h-10), (xmin+w, y), color, -1)
            cv2.putText(frame, label, (xmin, y-5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)

            object_count += 1

    # FPS
    if source_type in ['video','usb','picamera']:
        cv2.putText(frame, f'FPS: {avg_frame_rate:.2f}',
                    (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    cv2.putText(frame, f'Objects: {object_count}',
                (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)

    cv2.imshow('YOLO detection', frame)

    if record:
        recorder.write(frame)

    key = cv2.waitKey(5)
    if key in [ord('q'), ord('Q')]:
        break

    # FPS calc
    fps = 1 / (time.perf_counter() - t_start)

    if len(frame_rate_buffer) >= fps_avg_len:
        frame_rate_buffer.pop(0)
    frame_rate_buffer.append(fps)

    avg_frame_rate = np.mean(frame_rate_buffer)

# Cleanup
print(f'Average FPS: {avg_frame_rate:.2f}')

if source_type in ['video','usb']:
    cap.release()
elif source_type == 'picamera':
    cap.stop()

if record:
    recorder.release()

cv2.destroyAllWindows()
