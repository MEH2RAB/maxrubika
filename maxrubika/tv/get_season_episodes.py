from typing import Optional, Literal, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetSeasonEpisodes:
    async def get_season_episodes(
        self: "maxrubika.RubikaTV",
        season_id: str,
        series_id: str,
        section_type: Optional[Literal["MediaInfo", "Player"]] = None,
        track_id: Optional[str] = None
    ):
        """
        Retrieve episodes of a season.

        Parameters:
            season_id (str): Identifier of the season.
            series_id (str): Identifier of the series.
            section_type (str, optional): Optional section type: "MediaInfo" or "Player". Case-insensitive.
            track_id (str, optional): Optional tracking identifier.

        Returns:
            The API output.
        """
        from .exceptions import InvalidInput

        input_data = {
            "season_id": season_id,
            "series_id": series_id
        }

        if section_type is not None:
            section_type_map = {
                'mediainfo': 'MediaInfo',
                'media_info': 'MediaInfo',
                'player': 'Player'
            }

            normalized_section_type = section_type_map.get(str(section_type).lower())

            if not normalized_section_type:
                message = "'section_type' must be 'MediaInfo' or 'Player'."
                raise InvalidInput(message)

            input_data["section_type"] = normalized_section_type

        if track_id is not None:
            input_data["track_id"] = track_id

        return await self.request(
            method="getSeasonEpisodes",
            input=input_data
        )