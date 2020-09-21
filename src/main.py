from __future__ import annotations
import click

from src.commands import poll_events


@click.group()
def cli() -> None:
    pass


def main() -> None:
    [
        cli.add_command(command)
        for command in [
            poll_events.poll_events,
        ]
    ]
    cli()


if __name__ == "__main__":
    main()
