from django.db import models

class Clients(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя_Клиента')
    phone = models.CharField(max_length=15, verbose_name='Телефон')
    message = models.CharField(max_length=500, verbose_name='Текст_сообщения')
    state = models.BooleanField(verbose_name='Статус сообщения', default=False)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name