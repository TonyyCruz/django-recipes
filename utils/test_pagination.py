from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_return_a_correct_pagination(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=1,
        )["pagination"]

        self.assertEqual([1, 2, 3, 4, 5], pagination)

    def test_first_range_is_static_if_current_page_is_less_than_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=3,
        )["pagination"]
        pagination_2 = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=3,
        )["pagination"]

        self.assertEqual([1, 2, 3, 4, 5], pagination)
        self.assertEqual([1, 2, 3, 4, 5], pagination_2)

    def test_first_range_change_if_current_page_passed_the_middle(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=4,
        )["pagination"]
        pagination_2 = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=6,
        )["pagination"]
        pagination_3 = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=10,
        )["pagination"]

        self.assertEqual([2, 3, 4, 5, 6], pagination)
        self.assertEqual([4, 5, 6, 7, 8], pagination_2)
        self.assertEqual([8, 9, 10, 11, 12], pagination_3)

    def test_pagination_range_is_correct_when_current_page_is_at_end(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=18,
        )["pagination"]
        pagination_2 = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=19,
        )["pagination"]
        pagination_3 = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=5,
            current_page=20,
        )["pagination"]

        self.assertEqual([16, 17, 18, 19, 20], pagination)
        self.assertEqual([16, 17, 18, 19, 20], pagination_2)
        self.assertEqual([16, 17, 18, 19, 20], pagination_3)
