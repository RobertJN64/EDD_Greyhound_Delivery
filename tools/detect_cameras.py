import traceback
import cv2
import os

videos = []
for fpath in os.listdir('/dev'):
    if fpath.startswith('video') and len(fpath) == len("video") + 1:
        videos.append(int(fpath.removeprefix('video')))

videos = sorted(videos)
print("Potential videos: ", videos)
for video in videos:
    try:
        _cap = cv2.VideoCapture(video)
        _cap.grab()
        ret, frame = _cap.retrieve()
        print(video, ret)
        if ret:
            cv2.imwrite(f"video_{video}.png", frame)
    except (Exception,) as e:
        trace = traceback.format_exc()
        print(f"Video {video} Error:\n", trace)
