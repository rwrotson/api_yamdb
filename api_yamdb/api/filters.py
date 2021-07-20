from rest_framework import filters


class TitleFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        category = request.GET.get('category')
        if category is not None:
            queryset = queryset.filter(category__slug=category)
        genre = request.GET.get('genre')
        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)
        name = request.GET.get('name')
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        year = request.GET.get('year')
        if year is not None:
            queryset = queryset.filter(year=year)
        return queryset
