from .. import exceptions
import maxrubika

class Disconnect:
    async def disconnect(self: "maxrubika.Client") -> None:
        """
        Disconnect from the maxrubika server.

        Raises:
            exceptions.NoConnection: If the client is not connected.
        """
        try:
            await self.connection.close()
            self.logger.info('The client was disconnected.')

        except AttributeError:
            raise exceptions.NoConnection(
                'You must first connect the Client'
                ' with the *.connect() method')