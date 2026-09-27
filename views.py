from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404

from .models import Promise, Tag


class PromiseListMixin:
    """Shared list config so browse/search/tag-filter views stay DRY."""

    model = Promise
    template_name = "promises/promise_list.html"
    context_object_name = "promises"
    paginate_by = 20


class PromiseListView(PromiseListMixin, ListView):
    """Default browse view — all promises, newest first within ordering."""

    def get_queryset(self):
        return Promise.objects.all().prefetch_related("tags")


class PromiseSearchView(PromiseListMixin, ListView):
    """?q=<term> — reuses the same template/pagination as browse."""

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query:
            return Promise.objects.none()
        return Promise.objects.search(query).prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        return context


class PromiseByTagView(PromiseListMixin, ListView):
    """/tag/<group>/<slug>/ — e.g. /tag/emotion/anxious/"""

    def get_queryset(self):
        self.tag = get_object_or_404(
            Tag, group=self.kwargs["group"], slug=self.kwargs["slug"]
        )
        return self.tag.promises.all().prefetch_related("tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


class PromiseDetailView(DetailView):
    model = Promise
    template_name = "promises/promise_detail.html"
    context_object_name = "promise"
