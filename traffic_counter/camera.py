import abc
import time
import threading
from collections.abc import Generator
from typing import Optional
from dataclasses import dataclass

import cv2
import numpy as np


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
        while True:
            if self._frame is not None:
                yield self._frame

            time.sleep(1.0 / self._output_fps)

    @abc.abstractmethod
    def _calculate_frame(self) -> Optional[np.ndarray]:
        """Generator that returns frames from the camera."""
        raise NotImplementedError()

    def _run(self) -> None:
        """Camera background thread."""
        while True:
            frame = self._calculate_frame()
            if frame is None:
                raise Exception("Error calculating frame")

            self._frame = frame
            time.sleep(1.0 / self._camera_fps)


class OpenCVCamera(BaseCamera):
    def __init__(
        self, source: str, *,
        format: str = ".jpg",
        output_fps: float = 25.0,
    ) -> None:
        self._format = format
        self._camera = cv2.VideoCapture(source)

        if not self._camera.isOpened():
            raise Exception("Could not start camera.")

        camera_fps = 30.0

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
