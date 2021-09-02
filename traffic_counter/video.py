import pathlib

import cv2


def snapshot_to_file(video_url: str, filepath: pathlib.Path) -> None:
    cam = cv2.VideoCapture(video_url)
    success, frame = cam.read()

    if not success:
        raise Exception("Could not read frame from stream")

    cam.release()

    cv2.imwrite(str(filepath), frame)


def snapshot_to_image(video_url: str, format: str = ".jpg") -> tuple:
    cam = cv2.VideoCapture(video_url)
    success, frame = cam.read()

    if not success:
        raise Exception("Could not read frame from stream")

    cam.release()

    success, image = cv2.imencode(format, frame)

    if not success:
        raise Exception("Could not encode frane as image")

    return image
