from collections.abc import Callable
from sqlalchemy.exc import OperationalError, IntegrityError



class MaybeMonad:

    def __init__(self, data, error_status = None):
        self.data = data
        self.error_status = error_status

    async def bind(self, function: Callable):
        if not self.data:
            self.error_status = {"status": 500, "reason": "No data in repository monad"}
            return MaybeMonad(None, self.error_status)
        try:
            await function(self.data)
            return MaybeMonad(self.data, self.error_status)
        except OperationalError:
            self.error_status = {"status": 502, "reason": "Failed to connect to database"}
            return MaybeMonad(None, self.error_status)
        except IntegrityError:
            self.error_status = {"status": 409, "reason": "Failed to insert data into database"}
            return MaybeMonad(None, self.error_status)
