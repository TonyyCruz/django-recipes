import math

from django.core.paginator import Paginator


def make_pagination_range(page_range, qty_pages, current_page):
    start_range_idx = 0
    total_pages = len(page_range)
    pagination_range = math.floor(qty_pages / 2)
    pagination_middle = math.ceil(qty_pages / 2)
    pagination = list()

    if len(page_range) <= qty_pages:
        pagination = page_range

    elif current_page <= pagination_middle:
        pagination = page_range[
            start_range_idx:pagination_middle + pagination_range]

    elif current_page + pagination_range > total_pages:
        pagination_middle = total_pages - math.ceil(qty_pages / 2)
        pagination = page_range[- qty_pages:]

    else:
        pagination_middle = current_page
        start_range_idx = current_page - pagination_range - 1
        pagination = page_range[
            start_range_idx:current_page + pagination_range]

    return {
        "pagination": pagination,
        "page_range": page_range,
        "qty_pages": qty_pages,
        "current_page": current_page,
        "total_pages": total_pages,
        "start_range": start_range_idx,
        "stop_range": pagination[-1],
        "first_page_out_of_range": current_page > math.ceil(qty_pages / 2),
        "last_page_out_of_range": pagination[-1] < total_pages,
    }


def make_pagination(request, object_list, per_page, qty_pages=5):
    current_page = request.GET.get("page", 1)
    paginator = Paginator(object_list, per_page)
    pages_obj = paginator.get_page(current_page)

    try:
        current_page = int(current_page)
    except ValueError:
        current_page = 1

    pagination_range = make_pagination_range(
        page_range=paginator.page_range,
        qty_pages=qty_pages,
        current_page=current_page,
    )

    return pages_obj, pagination_range
