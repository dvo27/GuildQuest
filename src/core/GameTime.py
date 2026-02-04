from typing import TYPE_CHECKING
from .WorldClock import WorldClock

if TYPE_CHECKING:
    from .WorldClock import WorldClock    # fixes circular import

class GameTime:
    def __init__(self, current_day: int = 0, current_hour: int = 0, current_minute: int = 0, current_seconds: int = 0):
        self.current_day    = current_day  # added game_time to track day to make more sense apart from uml design
        self.current_hour = current_hour
        self.current_minute = current_minute
        self.current_seconds = current_seconds
        self.full_time = self._format_time()
        
    def _format_time(self) -> str:
        """
        Internal helper function to format the full date into string format

        Returns:
            str: Full formatted date as a string.
        """
        return f"Day {self.current_day}, {self.current_hour:02d}:{self.current_minute:02d}:{self.current_seconds:02d}"

    def start_time(self, c: WorldClock) -> None:
        """
        Starts the world clock

        Args:
            c (World_Clock): World_Clock object to start clock
        """
        c.start()
    
    def pause_time(self, c: WorldClock) -> None:
        """
        Pauses the world clock

        Args:
            c (World_Clock): World_Clock object to pause clock
        """
        c.stop()
    
    def get_day(self) -> int:
        """
        Returns current day

        Returns:
            int: current day
        """
        return self.current_day
    
    def get_hour(self) -> int:
        """
        Returns current hour

        Returns:
            int: current hour
        """
        return self.current_hour
    
    def get_minute(self) -> int:
        """
        Returns current minute

        Returns:
            int: current minute
        """
        return self.current_minute
    
    def get_seconds(self) -> int:
        """
        Returns current seconds

        Returns:
            int: current seconds
        """
        return self.current_seconds
    
    def get_fulltime(self) -> str:
        """
        Returns the full formatted date string

        Returns:
            str: Full date
        """
        return self.full_time