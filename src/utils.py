"""
utils
"""

from __future__ import annotations
import logging.config
import logging
import os
import functools
from typing import Callable

import yaml
import boxsdk


log = logging.getLogger(__name__)


def configure_logging(configuration: dict) -> None:
    log_dict_config = configuration["log"]
    for handler_alias, handler_config in log_dict_config["handlers"].items():
        if "filename" in handler_config.keys():
            if not os.path.exists(handler_config["filename"]):
                with open(handler_config["filename"], "w"):
                    pass

    logging.config.dictConfig(log_dict_config)
    log.debug(f"configured logging")


def load_configuration(env_alias: str) -> dict:
    config_file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "configuration",
        f"{env_alias}.yml",
    )
    with open(config_file_path) as fh:
        return yaml.load(fh, Loader=yaml.FullLoader)


def write_configuration(env_alias: str, config_dict: dict) -> None:
    config_file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "configuration",
        f"{env_alias}.yml",
    )
    with open(config_file_path, "w") as fh:
        yaml.dump(config_dict, fh, default_flow_style=False)


def config_env(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        env_alias = kwargs.get("env")
        if not env_alias:
            raise TypeError("Missing 'env' kwargs")

        config = load_configuration(env_alias)
        configure_logging(config)
        log.info(f"Running {func.__name__} CLI")
        kwargs["config"] = config

        return func(*args, **kwargs)

    return wrapper


def box_auth_from_config(config: dict) -> boxsdk.JWTAuth:
    box_auth = boxsdk.JWTAuth.from_settings_dictionary(config["box"]["jwt"])

    return box_auth


def box_client_from_config(config: dict) -> boxsdk.Client:
    box_auth = box_auth_from_config(config)
    client = boxsdk.Client(box_auth)

    return client


def box_event_type_filters_from_config(config: dict) -> list:
    return [event_type for event_type in config["box"]["event_types"]]


def log_box_event(event):
    event_response_object = event.response_object
    log.info("Processing Box Event")
    log.info(f"Event ID: {event_response_object['event_id']}")
    if event_response_object["event_type"] == "UPLOAD":
        log_box_item_event(event_response_object)


def log_box_item_event(event_response_object):
    log.info(f"Item ID: {event_response_object['source']['item_id']}")
    log.info(f"Item Name: {event_response_object['source']['item_name']}")
    log.info(f"Item Created By: {event_response_object['created_by']['login']}\n")
