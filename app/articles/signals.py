# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from articles.models import Article
# from chat.models import ChatNotification
# from core.models import User
# from vacancy.models.vacancy import Vacancy
#
#
# @receiver(post_save, sender=Article)
# def send_create_article(sender, instance: Article, created, **kwargs):
#     """Сигнал уведомления на создание статьи. Рассылка членам команды"""
#     if created:
#         receivers: list = [
#             item.candidate_id.professional_id.owner.id
#             for item in instance.company_id.work_team.all()
#         ]
#
#         receivers.append(instance.company_id.owner.id)
#         for receiver in receivers:
#             user = User.objects.filter(id=receiver).first()
#             ChatNotification.objects.create(
#                 user=user,
#                 text=f"Startup {instance.company_id.name} created new Article '{instance.name}'",
#             )
#
#
# @receiver(post_delete, sender=Article)
# def send_delete_article(sender, instance: Article, **kwargs):
#     """Сигнал уведомления на удаление статьи. Рассылка членам команды"""
#     receivers: list = [
#         item.candidate_id.professional_id.owner.id
#         for item in instance.company_id.work_team.all()
#     ]
#
#     receivers.append(instance.company_id.owner.id)
#
#     for receiver in receivers:
#         user = User.objects.filter(id=receiver).first()
#         ChatNotification.objects.create(
#             user=user,
#             text=f"Article '{instance.name}' has from  {instance.company_id.name}  deleted",
#         )
#
#
# @receiver(post_save, sender=Vacancy)
# def send_create_vacancy(sender, instance: Vacancy, created, **kwargs):
#     """Сигнал уведомления на создание вакансии. Рассылка членам команды"""
#     if created:
#
#         receivers: list = [
#             item.candidate_id.professional_id.owner.id
#             for item in instance.company_id.work_team.all()
#             if item.vacancy_management
#         ]
#
#         receivers.append(instance.company_id.owner.id)
#
#         for receiver in receivers:
#             user = User.objects.filter(id=receiver).first()
#             ChatNotification.objects.create(
#                 user=user,
#                 text=f"Startup {instance.company_id.name} created new Vacancy to position {instance.position}",
#             )
#
#
# @receiver(post_delete, sender=Vacancy)
# def send_delete_vacancy(sender, instance: Vacancy, **kwargs):
#     """Сигнал уведомления на удаление вакансии. Рассылка членам команды"""
#     receivers: list = [
#         item.candidate_id.professional_id.owner.id
#         for item in instance.company_id.work_team.all()
#         if item.vacancy_management
#     ]
#
#     receivers.append(instance.company_id.owner.id)
#
#     for receiver in receivers:
#         user = User.objects.filter(id=receiver).first()
#         ChatNotification.objects.create(
#             user=user,
#             text=f"Startup {instance.company_id.name} deleted  Vacancy to position {instance.position}",
#         )
