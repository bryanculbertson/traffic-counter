import pathlib

import cv2


def snapshot_to_file(video_url: str, filepath: pathlib.Path) -> None:
    cam = cv2.VideoCapture(video_url)
    f, image = cam.read()

    if not f:
        raise Exception("Could not read image from stream")

    cam.release()

    cv2.imwrite(str(filepath), image)
