from unittest import TestCase

from recipes.utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_return_a_correct_pagination(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4, 5], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=3,
        )
        pagination_2 = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=3,
        )
        self.assertEqual([1, 2, 3, 4, 5], pagination)
        self.assertEqual([1, 2, 3, 4, 5], pagination_2)

    def test_first_range_change_if_current_page_passed_the_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=4,
        )
        pagination_2 = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=6,
        )
        self.assertEqual([2, 3, 4, 5, 6], pagination)
        self.assertEqual([4, 5, 6, 7, 8], pagination_2)
