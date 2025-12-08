import cowsay


def greet(message: str = "Hello from una!") -> str:
    """
    Generate a greeting message using cowsay.

    Args:
        message: The message for the cow to say.

    Returns:
        A string containing the cowsay ASCII art with the message.

    >>> result = greet("Hi")
    >>> "Hi" in result
    True
    """
    result: str = cowsay.say(message)
    return result
