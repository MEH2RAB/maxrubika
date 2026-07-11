import maxrubika
from ..core.api import Api

class Connect:
    async def connect(self: "maxrubika.Client") -> "maxrubika.Client":
        """
        Establish a connection to the Rubika API.

        Creates an Api instance and loads stored session information
        (auth, guid, private_key, user_agent) if available.

        Returns:
            Client instance with active connection.
        """
        self.connection = Api(client=self)

        information = self.session.information()
        self.logger.info(f'the session information was read {information}')

        if information:
            self.auth = information[1]
            self.guid = information[2]
            self.private_key = information[4]

            if isinstance(information[3], str):
                self.user_agent = information[3] or self.user_agent

        return self