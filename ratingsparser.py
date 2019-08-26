import abc
from typing import List

from track import Track

class RatingsParser(abc.ABC):
    @abc.abstractmethod
    def tracks(self) -> List[Track]:
        pass
