import abc

class RatingsParser(abc.ABC):
    @abc.abstractmethod
    def tracks(self):
        pass
