from django.contrib import admin
from .models import Tweet, Like


# Register your models here.
class ContainElonMusk(admin.SimpleListFilter):

    title = "Catain Elon Musk Filter"

    parameter_name = "elon"

    def lookups(self, request, model_admin):
        return [
            ("ok", "Contain Elon"),
            ("no", "Don't contain Elon"),
        ]

    def queryset(self, request, reviews):
        word = self.value()
        if word == "ok":
            return reviews.filter(
                payload__icontains="Elon Musk",
            )
        elif word == "no":
            return reviews.exclude(
                payload__icontains="Elon Musk",
            )
        else:
            return reviews


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "payload",
        "total_likes",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
        ContainElonMusk,
    )

    search_fields = (
        "user__username",
        "payload",
    )

    def total_likes(self, tweet):
        return tweet.likes.count()


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "tweet",
        "created_at",
    )

    list_filter = ("created_at",)

    search_fields = ("user__username",)
