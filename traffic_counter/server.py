"""
poetry run uvicorn traffic_counter.server:app --reload
"""

import functools
from typing import Iterator

import fastapi
import fastapi.templating
import pydantic

from traffic_counter import camera

app = fastapi.FastAPI()
templates = fastapi.templating.Jinja2Templates(directory="traffic_counter/templates")


class Settings(pydantic.BaseSettings):
    video_url: str = (
        "https://cams.cdn-surfline.com/cdn-wc/wc-southoceanbeach/chunklist.m3u8"
    )


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()


source_camera = None


@app.get("/")
async def read_root(request: fastapi.Request) -> fastapi.Response:
    return templates.TemplateResponse("index.html", context={"request": request})


def streamer(source: camera.BaseCamera) -> Iterator[bytes]:
    for frame in source.frames():
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame.tobytes() + b"\r\n"
        )


@app.get("/video")
async def video_endpoint(range: str = fastapi.Header(None)) -> fastapi.Response:
    global source_camera

    if not source_camera:
        settings = get_settings()
        source_camera = camera.OpenCVCamera(settings.video_url)
        source_camera.start()

    return fastapi.responses.StreamingResponse(
        streamer(source_camera),
        media_type="multipart/x-mixed-replace;boundary=frame",
    )
