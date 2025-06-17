from .logging_service import LoggingService


def confirm_action(question: str) -> bool:
    entered: str = "none"
    while entered != "exit" and entered != "":
        LoggingService.info(f"{question} Press ENTER to confirm... (Type 'exit' or hit Ctrl+C to exit.)")
        try:
            entered = input()
        except KeyboardInterrupt:
            return False
    return True if not entered else False
