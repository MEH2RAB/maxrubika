from typing import Literal, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import maxrubika

class GetCalls:
    async def get_calls(
        self: "maxrubika.Messenger",
        sort: Literal['FromMin', 'FromMax'] = 'FromMax',
        filter_type: Literal['All', 'Missed'] = 'All',
        max_id: Optional[Union[str, int]] = None,
        min_id: Optional[Union[str, int]] = None
    ):
        """
        Get the list of calls.

        Parameters:
            sort (Literal['FromMin', 'FromMax']): Sort order. Required. Default: 'FromMax'
            filter_type (Literal['All', 'Missed']): Filter calls by type. Default: 'All'
            max_id (Union[str, int], optional): Maximum call ID for pagination. Defaults to None.
            min_id (Union[str, int], optional): Minimum call ID for pagination. Defaults to None.

        Returns:
            The result of the API call.
        """
        from ..exceptions import InvalidInput

        sort_map = {
            'frommin': 'FromMin',
            'frommax': 'FromMax',
        }
        sort = sort_map.get(sort.lower())

        if not sort:
            raise InvalidInput("'sort' must be 'FromMin' or 'FromMax'.")

        filter_type_map = {
            'all': 'All',
            'missed': 'Missed',
        }
        filter_type = filter_type_map.get(filter_type.lower())

        if not filter_type:
            raise InvalidInput("'filter_type' must be 'All' or 'Missed'.")

        input_data = {
            'sort': sort,
            'filter_type': filter_type
        }

        if max_id is not None:
            input_data['max_id'] = max_id

        if min_id is not None:
            input_data['min_id'] = min_id

        return await self.request(
            method='getCalls',
            input=input_data
        )