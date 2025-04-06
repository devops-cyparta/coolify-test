from rest_framework.pagination import PageNumberPagination

class DefaultPagination(PageNumberPagination):
  page_size = 6


class TopGamesPagination(PageNumberPagination):
  page_size = 4


class FAQPagination(PageNumberPagination):
  page_size = 4