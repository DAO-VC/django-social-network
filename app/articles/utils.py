from articles.models import Tag, Article
from image.models import Image
from profiles.models.investor import Investor
from profiles.models.professional import Professional
from profiles.models.startup import Startup


class TagsCleaner(object):
    """Очищение неиспользуемых тэгов"""

    def clean(self) -> None:
        all_tags: list = [tag.id for tag in Tag.objects.all()]
        all_using_tags: list = [
            item.id for obj in Article.objects.all() for item in obj.tags.all()
        ]
        result: set = set(all_tags).difference(set(all_using_tags))
        for item in result:
            Tag.objects.get(id=item).delete()
        return


class ImagesCleaner(object):
    """Очищение неиспользуемых картинок"""

    def clean(self) -> None:
        all_tags: list = [image.id for image in Image.objects.all()]

        all_using_articles: list = [
            item.image.id for item in Article.objects.all() if item.image
        ]
        all_using_startups_logo: list = [
            item.logo.id for item in Startup.objects.all() if item.logo
        ]
        all_using_startups_background: list = [
            item.background.id for item in Startup.objects.all() if item.background
        ]
        all_using_professional_photo: list = [
            item.photo.id for item in Professional.objects.all() if item.photo
        ]
        all_using_investor: list = [
            item.photo.id for item in Investor.objects.all() if item.photo
        ]
        temp: set = set()
        temp.update(
            all_using_articles,
            all_using_startups_background,
            all_using_professional_photo,
            all_using_investor,
            all_using_startups_logo,
        )

        result: set = set(all_tags).difference(temp)

        for item in result:
            Image.objects.get(id=item).delete()

        return
