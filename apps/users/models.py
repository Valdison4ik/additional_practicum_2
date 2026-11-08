from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, PermissionsMixin
from django.core.validators import MinLengthValidator
from django.db import models
from apps.base.models import TimeStampModel3
from django.utils.translation import gettext_lazy as _

class User(TimeStampModel3, AbstractBaseUser, PermissionsMixin):

    class Position(models.TextChoices):
        CEO = 'ceo', 'CEO'
        CTO = 'cto', 'CTO'
        DESIGNER = 'designer', 'Designer'
        PROGRAMMER = 'programmer', 'Programmer'
        PROD_OWNER = 'product_owner', 'Product_owner'
        PROJ_OWNER = 'project_owner', 'Project_owner'
        PROJ_MANAGER = 'project_manager', 'Project_manager'
        QA = 'qa', 'QA'

    username = models.CharField(_('Имя пользователя'),
                                unique=True,
                                max_length=50,
                                # null=False,
                                error_messages = {"unique": _("A user with that username already exists."),
                                                  })
    first_name = models.CharField(_('Имя'), unique=True, max_length=40, validators=[MinLengthValidator(2)])
    last_name = models.CharField( _("Фамилия"), max_length=80, validators=[MinLengthValidator(2)])
    email = models.EmailField(_('Электронный адрес'), unique=True)
    phone = models.CharField(_('Номер телефона'), max_length=75, null=True, blank=True)
    is_staff = models.BooleanField(_('Является ли сотрудником'),default=False)
    position = models.CharField(_('Должность'),max_length=20, null=True, blank=True,
                                choices=Position)
    is_active = models.BooleanField(_('Является ли активным'),default=True)
    last_login = models.DateTimeField(_('Последнее подключение'), null=True, blank=True) # Поле даты и времени, заполняется при входе в систему

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_deleted(self):
        return self.deleted_at is not None

    USERNAME_FIELD = "email" # Укажите поле email, как поле для входа в систему.

    # Добавьте дополнительные поля для регистрации:
    # ● username
    # ● last_name
    # ● first_name
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    # переопределение стандартного менеджера
    objects = UserManager()

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # ordering = ['due_date', 'assignee']
        # constraints = [models.UniqueConstraint(fields=['name', 'project'], name='unique_name_project')]
        db_table = 'users'