import logging
import time

import click

from src import utils


log = logging.getLogger(__name__)


def write_created_after_to_config(env, config, events_created_after):
    config["box"]["events_created_after"] = events_created_after
    utils.write_configuration(env, config)


@click.command()
@click.option(
    "-e",
    "--env",
    default="dev",
    help="env environment alias",
    type=str,
)
@utils.config_env
def poll_events(env, config):
    box_client = utils.box_client_from_config(config)
    event_type_filters = utils.box_event_type_filters_from_config(config)
    events_created_after = config["box"]["events_created_after"]
    try:
        while True:
            events = box_client.events().get_admin_events(
                created_after=events_created_after, event_types=event_type_filters
            )
            length = len(events["entries"])
            if length > 0:
                for event in events["entries"]:
                    events_created_after = event.response_object["created_at"]
                    utils.log_box_event(event)
            else:
                write_created_after_to_config(env, config, events_created_after)
                time.sleep(60)

    except (Exception, KeyboardInterrupt) as e:
        if events_created_after:
            write_created_after_to_config(env, config, events_created_after)

        log.error(e)
