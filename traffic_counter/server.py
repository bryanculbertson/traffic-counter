"""
poetry run uvicorn traffic_counter.server:app --reload
"""

import functools
from typing import Iterator

import fastapi
import fastapi.templating
import pydantic

from traffic_counter import video

app = fastapi.FastAPI()
templates = fastapi.templating.Jinja2Templates(directory="traffic_counter/templates")


class Settings(pydantic.BaseSettings):
    video_url: str = (
        "https://cams.cdn-surfline.com/cdn-wc/wc-southoceanbeach/chunklist.m3u8"
    )


@functools.lru_cache()
def get_settings() -> Settings:
    return Settings()


@app.get("/")
async def read_root(request: fastapi.Request) -> fastapi.Response:
    return templates.TemplateResponse("index.html", context={"request": request})


def streamer(video_url: str) -> Iterator[bytes]:
    for image in video.video_as_images(video_url):
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + bytearray(image) + b"\r\n"
        )


@app.get("/video")
async def video_endpoint(range: str = fastapi.Header(None)) -> fastapi.Response:
    settings = get_settings()

    return fastapi.responses.StreamingResponse(
        streamer(settings.video_url),
        media_type="multipart/x-mixed-replace;boundary=frame",
    )
