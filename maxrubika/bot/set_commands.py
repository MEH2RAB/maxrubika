from typing import List, Dict, Any, Optional, Union
import re; import maxrubika
from .exceptions import InvalidInput

class SetCommands:
    async def set_commands(
        self: "maxrubika.Bot",
        commands: Optional[Union[List[Dict[str, str]], Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Sets custom commands for the bot. Pass empty list/dict to remove all commands.

        Parameters:
            commands (List[Dict[str, str]] or Dict[str, str], optional): 
                Either a list of dictionaries with 'command' and 'description',
                or a simple dictionary like {"start": "Start the bot", "help": "Help"}.
                Example: [{"command": "start", "description": "Start the bot"}, ...]
                or: {"start": "Start the bot", "help": "Show help"}
                If None or empty, all commands will be removed.

        Returns:
            dict: API response.
        """
        if not commands:
            payload: Dict[str, Any] = {'bot_commands': []}
            return await self._request('POST', 'setCommands', json = payload)

        formatted_commands = []

        if isinstance(commands, dict):
            for cmd, desc in commands.items():
                formatted_commands.append({'command': cmd, 'description': desc})
        elif isinstance(commands, list):
            formatted_commands = commands
        else:
            raise InvalidInput("'commands' must be a list or dictionary.")

        for cmd in formatted_commands:
            command = cmd.get('command', '')
            description = cmd.get('description', '')

            if command.startswith("/"):
                command = command[1:]
                cmd['command'] = command

            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]{0,31}$', command):
                message = f"Invalid command format: '{command}'. Must start with letter or underscore, followed by letters, numbers, or underscores (max 32 chars)."
                raise InvalidInput(message)

            if len(description) > 256:
                message = f"Description for '/{command}' must be <= 256 characters."
                raise InvalidInput(message)

        payload: Dict[str, Any] = {'bot_commands': formatted_commands}
        return await self._request('POST', 'setCommands', json = payload)