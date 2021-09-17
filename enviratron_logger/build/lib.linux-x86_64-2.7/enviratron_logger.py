import sys
import logging
from datetime import datetime
from pathlib import Path
import yaml
from pythonjsonlogger import jsonlogger
from chamber import GrowthChamberControl as gcc


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom log format class"""

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        log_record["timestamp"] = now

        if log_record.get("level"):
            log_record["level"] = log_record["level"].upper()
        else:
            log_record["level"] = record.levelname

    # Overriding process_log_record() in order to remove the default 'message' key from the record:
    def process_log_record(self, log_record):
        del log_record["message"]

        try:
            del log_record["env_var"]
            del log_record["env_val"]
        except KeyError:
            pass

        try:
            # change Percival's 0-10,000 scale for lighting intensity to the more readable 0-100 scale:
            for i in range(1, 8):
                log_record[f"lighting_{i}"] = log_record[f"lighting_{i}"] / 100
        except KeyError:
            pass

        return super(CustomJsonFormatter, self).process_log_record(log_record)


def get_logger(chamber_id: int, log_dir_path: Path):
    """Convenience function for getting a logger instance"""

    formatter = CustomJsonFormatter("%(timestamp)s %(level)s %(message)s")
    # When working with multiple loggers, it seems that passing a name to getLogger is necessary,
    # or else you'll get things logging to unexpected places
    logger = logging.getLogger(f"chamber_{chamber_id}_logger")
    log_handler = logging.FileHandler(
        log_dir_path / f"chamber_{chamber_id}_environment.log"
    )
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
    return logger


def main():
    DEFAULT_CHAMBER_IDS = (1, 2, 3, 4, 6, 7, 8)

    if len(sys.argv) == 2:
        yaml_filepath_str = sys.argv[-1]

        with open(yaml_filepath_str, "r") as config_handle:
            config = yaml.load(config_handle, Loader=yaml.Loader)
            chamber_ids = config.get("chamber_ids", DEFAULT_CHAMBER_IDS)
            log_path = Path(config.get("log_directory", "."))
            log_path.mkdir(exist_ok=True, parents=True)

    else:
        # No yaml configuration file found in the call
        chamber_ids = DEFAULT_CHAMBER_IDS
        log_path = Path(".")

    for chamber_id in chamber_ids:
        logger = get_logger(chamber_id, log_dir_path=log_path)
        chamber = gcc(chamber_id)
        state = chamber.get_state()

        if state.get("type") == "ConnectionError":
            logger.error(msg=state)
        else:
            logger.info(msg=state)


if __name__ == "__main__":
    main()
