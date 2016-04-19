import logging

from django.conf import settings
from slacker import Slacker

logger = logging.getLogger(__name__)

# Check required settings
for required_setting in ['SLACK_API_TOKEN', 'SLACK_CHANNEL']:
    if not hasattr(settings, required_setting):
        raise RuntimeError("The %s setting needs to be set in your settings"
                           " file" % required_setting)


def is_debug_enabled():
    return bool(getattr(settings, 'SLACK_DEBUG', False))


def post_message(message):
    """
    Post the given message on slack, or just log it if debug mode is enabled.
    """
    slacker = Slacker(settings.SLACK_API_TOKEN)

    if is_debug_enabled():
        logger.info(message)
    else:
        try:
            slacker.chat.post_message(settings.SLACK_CHANNEL, message,
                                       link_names=True)
        except Exception:
            logger.exception("Unable to send slack message")
