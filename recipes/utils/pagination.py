import math


def make_pagination_range(page_range, qty_pages, current_page):
    if len(page_range) <= qty_pages:
        return page_range

    start_range_idx = 0
    end_range_pagination = len(page_range)
    pagination_range = math.floor(qty_pages / 2)
    pagination_middle = math.ceil(qty_pages / 2)

    if current_page <= pagination_middle:
        return page_range[start_range_idx:pagination_middle + pagination_range]

    start_range_idx = current_page - pagination_range - 1
    pagination_middle = current_page

    if pagination_middle + pagination_range > end_range_pagination:
        return page_range[- qty_pages:]

    return page_range[start_range_idx:current_page + pagination_range]
