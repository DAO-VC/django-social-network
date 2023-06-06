from articles.models import Tag, Article


class TagsCleaner(object):
    """Очищение неиспользуемых тэгов"""

    def clean(self) -> None:
        all_tags: list = [tag.id for tag in Tag.objects.all()]
        all_using_tags: list = [
            item.id for obj in Article.objects.all() for item in obj.tags.all()
        ]
        result: set = set(all_using_tags).symmetric_difference(set(all_tags))
        for item in result:
            Tag.objects.get(id=item).delete()
        return
