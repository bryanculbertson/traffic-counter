#!/usr/bin/env python3

"""
Tool for counting traffic

Example usage:
    poetry run traffic-counter version

"""
import click
import dotenv


@click.group()
def cli() -> None:
    """Run cli commands"""
    dotenv.load_dotenv()


@cli.command()
def version() -> None:
    """Get the cli version."""
    click.echo(click.style("0.1.0", bold=True))


if __name__ == "__main__":
    cli()
