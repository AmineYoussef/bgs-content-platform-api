from typing import List, Any
from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

@dataclass
class SortingModel():
    sort_by: str = Field(..., description="Field by which to sort.")
    sort_direction: str = Field(-1, description="Direction of sorting: 1 for ascending, -1 for descending.")


    def __init__(self, sort_by, sort_direction):
        self.sort_by = sort_by
        self.sort_direction = sort_direction


@dataclass
class PaginationModel():
    page: int = Field(1, ge=1, description="Current page number.")
    page_size: int = Field(10, ge=1, description="Number of items per page.")
    total_pages: int = Field(0, ge=0, description="Total number of pages.")
    total_items: int = Field(0, ge=0, description="Total number of items.")

    def __init__(self, page, page_size, total_pages, total_items):
        self.page = page
        self.page_size = page_size
        self.total_pages = total_pages
        self.total_items = total_items


class ListSuccessResponse(BaseModel):
    data: List[Any] = Field(..., description="List of data items.")
    sorting: SortingModel = Field(..., description="Sorting information.")
    pagination: PaginationModel = Field(..., description="Pagination information.")

    def __init__(self, **data):
        super().__init__(**data)