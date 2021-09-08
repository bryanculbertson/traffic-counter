#!/usr/bin/env python3

"""
Tool for counting traffic

Example usage:
    poetry run traffic-counter version

    poetry run traffic-counter snapshot \
        --video-url=https://cams.cdn-surfline.com/cdn-wc/wc-southoceanbeach/chunklist.m3u8 \
        --filepath=out/ocean.png

"""
import pathlib
from typing import Optional

import click
import dotenv
import pathy
import uvicorn

from traffic_counter import video


class FluidPath(click.ParamType):
    name = "fluid_path"

    def convert(
        self,
        value: Optional[str],
        param: Optional[click.Parameter],
        ctx: Optional[click.Context],
    ) -> Optional[pathy.FluidPath]:
        if value is None:
            return None

        try:
            return pathy.Pathy.fluid(value)
        except (TypeError, ValueError):
            self.fail(
                f"{value!r} needs to be a local or GCS file path string.", param, ctx
            )
            return None


@click.group()
def cli() -> None:
    """Run cli commands"""
    dotenv.load_dotenv()


@cli.command()
@click.option("--video-url", type=str, required=True)
@click.option(
    "--filepath",
    type=FluidPath(),
    required=True,
)
def snapshot(video_url: str, filepath: pathlib.Path) -> None:
    """Save a image from a video to a file"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    video.snapshot_to_file(video_url, filepath)


@cli.command()
def serve() -> None:
    """Serve traffic counter app"""
    uvicorn.run("traffic_counter.server:app")


@cli.command()
def version() -> None:
    """Get the cli version."""
    click.echo(click.style("0.1.0", bold=True))


if __name__ == "__main__":
    cli()
