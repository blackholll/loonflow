class CustomCommonException(Exception):
    """
    custom common exception. this type exception's message will display to user
    """
    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
