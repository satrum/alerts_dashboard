from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField, HStoreField
from django.utils import timezone
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User, AnonymousUser
from colorfield.fields import ColorField
import datetime

# Create your models here.
class Category(models.Model):
    """
    id, name, visible

    другие:
    icon (file)
    tags - many to many
    подкатегории
    порядок отображения
    """
    name = models.CharField(max_length=20, unique=True, help_text='название категории')
    visible = models.BooleanField(help_text='Показывать', default=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

class Sharetext(models.Model):
    text = models.CharField(max_length=200, help_text='текст для расшаривания опроса')

    def __str__(self):
        return self.text

class Poll(models.Model):
    """
    repeat = Choices (можно ли повторно проводить опрос тому же пользователю и как часто)

    """
    text = models.CharField(max_length=200, unique=True, help_text='тип опроса')
    TYPE_CHOICES = [
        ('A', 'On-Off'),
        ('O', 'One from all'),
        ('M', 'Many from all'),
    ]
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, help_text='тип системы')
    options = ArrayField(models.CharField(max_length=200))
    another = models.BooleanField(help_text='Есть другое', default=False)
    another_text = models.BooleanField(help_text='поле текста если выбрано другое', default=False)
    share_text = models.ForeignKey(Sharetext, on_delete=models.SET_NULL, null=True, blank=True, related_name="share_polls")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="category_polls")
    # enable, archive, disable
    STATE_CHOICES = [
        ('E', 'Enable'),
        ('D', 'Disable'),
        ('A', 'Archived'),
    ]
    state = models.CharField(max_length=1, choices=STATE_CHOICES, default='E', help_text='состояние')
    created_time = models.DateTimeField(default=timezone.now, help_text='Время создания опроса') # auto_now=True если нужно обновлять
    color = ColorField(default='#FF0000', help_text='Цвет блока')
    repeat = models.BooleanField(help_text='Можно ли повторять опрос', default=False)
    repeat_pause = models.DurationField(help_text='как часто можно повторять опрос', default=datetime.timedelta(days=1))

    def __str__(self):
        return self.text

class Results(models.Model):
    created_time = models.DateTimeField(default=timezone.now, help_text='Время опроса пользователем')
    poll = models.ForeignKey(Poll, on_delete=models.PROTECT, related_name="share_polls") #null=False, blank=False defaults
    result = ArrayField(models.CharField(max_length=200))
    input_text = models.CharField(max_length=200, blank=True, null=True, help_text='текст со своим вариантом')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_polls")
    #session_key = models.CharField(max_length=200, help_text='request.session.session_key')
    session_key = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, help_text='request.session.session_key')

    def __str__(self):
        if self.user is None:
            return self.poll.text + str(self.pk)
        else:
            return self.user.username + self.poll.text + str(self.pk)




