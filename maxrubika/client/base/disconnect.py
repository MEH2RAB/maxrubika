from .. import exceptions
import maxrubika
import asyncio
import logging

logger = logging.getLogger(__name__)

class Disconnect:
    async def close(self: "maxrubika.Client") -> None:
        """
        Close the connection to the MAXRubika server (async version).
        """
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

    def disconnect(self: "maxrubika.Client") -> None:
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