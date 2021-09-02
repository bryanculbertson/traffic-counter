import abc
import math
import threading
import time
from collections.abc import Generator
from typing import Optional

import cv2
import numpy as np
import pandas as pd


class BaseCamera(abc.ABC):
    def __init__(
        self,
        *,
        output_fps: float = 25.0,
        camera_fps: float = 25.0,
    ) -> None:
        """Start the background camera thread"""
        self._output_fps = output_fps
        self._camera_fps = camera_fps
        self._event = threading.Event()
        self._frame: Optional[np.ndarray] = None
        self._thread: Optional[threading.Thread] = None

    def start(self) -> None:
        self._thread = threading.Thread(target=self._run)
        self._thread.daemon = True
        self._thread.start()

    def frames(self) -> Generator[np.ndarray, None, None]:
        """Return the current camera frame."""
        prev = time.monotonic()
        while True:
            if self._frame is not None:
                yield self._frame

            current = time.monotonic()
            elasped = current - prev
            prev = current

            sleep_time = 1.0 / self._output_fps - elasped

            time.sleep(max(sleep_time, 0.0))

    @abc.abstractmethod
    def _calculate_frame(self) -> Optional[np.ndarray]:
        """Generator that returns frames from the camera."""
        raise NotImplementedError()

    def _run(self) -> None:
        """Camera background thread."""

        prev = time.monotonic()
        while True:
            frame = self._calculate_frame()
            if frame is None:
                raise Exception("Error calculating frame")

            self._frame = frame

            current = time.monotonic()
            elasped = current - prev
            prev = current

            sleep_time = 1.0 / self._camera_fps - elasped

            time.sleep(max(sleep_time, 0.0))


class OpenCVCamera(BaseCamera):
    def __init__(
        self,
        source: str,
        *,
        format: str = ".jpg",
        output_fps: float = 25.0,
    ) -> None:
        self._format = format
        self._camera = cv2.VideoCapture(source)

        if not self._camera.isOpened():
            raise Exception("Could not start camera.")

        camera_fps = 25.0

        prop_fps = self._camera.get(cv2.CAP_PROP_FPS)
        if prop_fps and prop_fps > 0.0:
            camera_fps = prop_fps / 2.0

        super().__init__(output_fps=output_fps, camera_fps=camera_fps)

    def __del__(self) -> None:
        if self._camera is not None:
            self._camera.release()
            self._camera = None

    def _calculate_frame(self) -> Optional[np.ndarray]:
        if self._camera is None:
            print("Camera is not initialized")
            return None

        success, unencoded_frame = self._camera.read()
        if not success:
            print("Cannot read from camera")
            return None

        success, encoded_frame = cv2.imencode(self._format, unencoded_frame)
        if not success:
            print("Cannot encode image from camera")
            return None

        return encoded_frame


class TrafficCounterCamera(OpenCVCamera):
    def __init__(
        self,
        source: str,
        *,
        format: str = ".jpg",
        output_fps: float = 25.0,
    ) -> None:
        self._df = pd.DataFrame()
        self._df.index.name = "Frames"

        self._centroids: list[tuple[int, int]] = []
        self._totalcars = 0
        self._fgbg = cv2.createBackgroundSubtractorMOG2()

        super().__init__(source, format=format, output_fps=output_fps)

    def _calculate_frame(self) -> Optional[np.ndarray]:
        if self._camera is None:
            print("Camera is not initialized")
            return None

        success, unencoded_frame = self._camera.read()
        if not success:
            print("Cannot read from camera")
            return None

        # Only grab the highway
        image = unencoded_frame[400:600, 0:1024]

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        fgmask = self._fgbg.apply(gray)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closing = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(opening, kernel)
        _, bins = cv2.threshold(dilation, 220, 255, cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(
            bins, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        hull = [cv2.convexHull(c) for c in contours]

        cv2.drawContours(image, hull, -1, (0, 255, 0), 3)

        # min area for contours in case a bunch of small noise contours are created
        minarea = 1000

        # max area for contours, can be quite large for buses
        maxarea = 50000

        current_centroids = []

        for i in range(len(contours)):  # cycles through all contours in current frame

            if hierarchy[0, i, 3] == -1:

                area = cv2.contourArea(contours[i])  # area of contour

                if minarea < area < maxarea:  # area threshold for contour

                    # calculating centroids of contours
                    cnt = contours[i]
                    M = cv2.moments(cnt)
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # gets bounding points of contour to create rectangle
                    # x,y is top left corner and w,h is width and height
                    x, y, w, h = cv2.boundingRect(cnt)

                    # creates a rectangle around contour
                    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    # Prints centroid text in order to double check later on
                    cv2.putText(
                        image,
                        str(cx) + "," + str(cy),
                        (cx + 10, cy + 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.3,
                        (0, 0, 255),
                        1,
                    )

                    cv2.drawMarker(
                        image,
                        (cx, cy),
                        (0, 0, 255),
                        cv2.MARKER_STAR,
                        markerSize=5,
                        thickness=1,
                        line_type=cv2.LINE_AA,
                    )

                    # adds centroids that passed previous criteria to centroid list
                    current_centroids.append((cx, cy))

        max_distance = 100

        existing_centroids = list(self._centroids)
        for current_centroid in current_centroids:
            found = -1
            for i, existing_centroid in enumerate(existing_centroids):
                if math.dist(current_centroid, existing_centroid) < max_distance:
                    found = i
                    break

            if found > -1:
                del existing_centroids[i]
            else:
                self._totalcars += 1

        self._centroids = current_centroids

        cv2.putText(
            image,
            "Cars: " + str(self._totalcars),
            (5, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (200, 200, 200),
            2,
        )

        success, encoded_frame = cv2.imencode(self._format, image)
        if not success:
            print("Cannot encode image from camera")
            return None

        return encoded_frame
