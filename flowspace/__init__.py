import logging


def get_logger():
    logger = logging.getLogger(__name__)

    try:
        from systemd import journal
        logger.addHandler(journal.JournalHandler())
    except ModuleNotFoundError as e:
        print(e)

    return logger
