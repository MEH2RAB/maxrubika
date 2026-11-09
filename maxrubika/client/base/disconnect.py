import asyncio
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

logger = logging.getLogger(__name__)

class Disconnect:
    async def close(self: "maxrubika.Messenger"):
        """
        Close the connection to the MAXRubika server (async version).
        """
        from .. import exceptions

        try:
            if self.connection is not None:
                await self.connection.close()
                self.logger.info('The client was disconnected.')
        except AttributeError:
            raise exceptions.NoConnection(
                'You must first connect the Client'
                ' with the *.connect() method'
            )
        except Exception as e:
            try:
                self.logger.debug(f'Error during disconnect: {e}')
            except Exception:
                pass

    def disconnect(self: "maxrubika.Messenger") -> None:
        """
        Disconnect from the MAXRubika server (sync version).
        """
        if self.connection is None:
            return

        result = self.close()

        if asyncio.iscoroutine(result):
            try:
                asyncio.get_running_loop().create_task(result)
            except RuntimeError:
                result.close()