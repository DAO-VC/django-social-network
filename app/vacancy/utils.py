from vacancy.models.vacancy import Skill, Vacancy, Requirement


class SkillsCleaner(object):
    """Очищение неиспользуемых скилов"""

    def clean(self) -> None:
        all_skills: list = [skill.id for skill in Skill.objects.all()]
        all_using_skills: list = [
            item.id for obj in Vacancy.objects.all() for item in obj.skills.all()
        ]
        result: set = set(all_skills).difference(set(all_using_skills))
        for item in result:
            Skill.objects.get(id=item).delete()
        return


class RequirementsCleaner(object):
    """Очищение неиспользуемых требований"""

    def clean(self) -> None:
        all_requirements: list = [
            requirement.id for requirement in Requirement.objects.all()
        ]
        all_using_requirements: list = [
            item.id for obj in Vacancy.objects.all() for item in obj.requirements.all()
        ]
        result: set = set(all_requirements).difference(set(all_using_requirements))
        for item in result:
            Requirement.objects.get(id=item).delete()
        return
