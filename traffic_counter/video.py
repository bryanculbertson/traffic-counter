import pathlib
import tempfile

import cv2


def snapshot_to_file(video_url: str, filepath: pathlib.Path) -> None:
    cam = cv2.VideoCapture(video_url)
    success, frame = cam.read()

    if not success:
        raise Exception("Could not read frame from stream")

    cam.release()

    # Write to temp file to support uploading to cloud filesystem
    with tempfile.NamedTemporaryFile(suffix=filepath.suffix) as tmp_file:
        cv2.imwrite(tmp_file.name, frame)
        tmp_file.seek(0)

        with filepath.open("wb") as outfile:
            for content in tmp_file:
                outfile.write(content)


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
