from models.response_model import *
from typing import Union, Literal, List, Dict, Any
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.collation import Collation

def get_find_cursor(
        collection: Collection,
        filter: Dict[str, Any],
        sort_direction: Union[Literal[-1], Literal[1]] = 1,
        sort_by: str = "created_at",
        page: int = 1,
        page_size: int = 10,
    ) -> Cursor:
        return (
            collection.find(filter)
            .sort(sort_by, sort_direction)
            .collation(Collation(locale="en", strength=2))  # ensure case insensitivity
            .skip(((page - 1) * page_size))
            .limit(page_size)
        )

def format_response(
    data: List,
    total_documents: int,
    sort_direction: Union[Literal[-1], Literal[1]],
    sort_by: str,
    page: int,
    page_size: int,
) -> ListSuccessResponse:
    """
    Format response data into a generic api return format

    Args:
        data (List): List of retrieved document
        total_documents (int): Total number of documents
        sort_direction (-1, 1): Sort direction where -1 = DESC and 1 = ASC 
        sort_by (str): Sort field name
        page (int): Page number to display
        page_size (int): Page size

    Returns:
        ListSuccessResponse: Formatted response containing the documents, sorting, and pagination metadata
    """
    sorting = SortingModel(sort_by, "ASC" if sort_direction > 0 else "DESC")
    pagination = PaginationModel(
        page,
        page_size,
        (
            (total_documents // page_size + 1)
            if total_documents % page_size > 0
            else total_documents // page_size
        ),
        total_documents,
    )
    return ListSuccessResponse(data=data, sorting=sorting, pagination=pagination).dict()
