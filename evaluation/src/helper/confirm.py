from sys import exit

from keyboard import wait


def confirm_action(logger, question):
    logger.info(f"{question}: Press ENTER to confirm... (Ctrl/Cmd+C to abort)")
    try:
        wait("enter")
    except KeyboardInterrupt:
        exit(0)
