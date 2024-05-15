from rest_framework.pagination import PageNumberPagination


class ProductsPaginator(PageNumberPagination):
    page_size = 2