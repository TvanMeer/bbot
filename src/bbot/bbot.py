from .options import Options

from .asyncbot import _AsyncBot


class Bot:
    """Main class that holds public API."""

    # Public
    def stop(self) -> None:
        pass

    # Internal
    def __init__(self, options: Options) -> None:
        self._create_client(options)

    def _create_client(self, options: Options) -> None:
        """Process fork or thread spawn here..."""
        self._bot = _AsyncBot(options)
