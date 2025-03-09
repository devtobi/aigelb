def confirm_action(logger, question):
    entered = "none"
    while entered != "exit" and entered != "":
        logger.info(
            f"{question} Press ENTER to confirm... (Type 'exit' or hit Ctrl+C to exit.)"
        )
        try:
            entered = input()
        except KeyboardInterrupt:
            return False
    return True if not entered else False
