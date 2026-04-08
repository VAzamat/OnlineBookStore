from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Genre(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="ID жанра")
    uuid = models.UUIDField(verbose_name="UUID жанра")
    name = models.CharField(max_length=255, verbose_name="Название жанров")
    is_root = models.BooleanField(default=False, verbose_name="Корневой ли?")
    url = models.CharField(max_length=255, verbose_name="URL жанра")
    is_main = models.BooleanField(default=False, verbose_name="Основной ли?")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self): return self.name

class Publisher(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="ID издательства")
    name = models.CharField(max_length=255, verbose_name="Название издательства")
    url = models.CharField(max_length=255, verbose_name="URL издательства", blank=True, null=True)

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"

    def __str__(self): return self.name

class Copyrighter(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="ID копирайтера", blank=True)
    name = models.CharField(max_length=255, verbose_name="Название копирайтера")
    url = models.CharField(max_length=255, verbose_name="URL", blank=True, null=True)

    class Meta:
        verbose_name = "Копирайтер"
        verbose_name_plural = "Копирайтеры"

    def __str__(self): return self.name


class Rightholder(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="ID правообладателя")
    name = models.CharField(max_length=255, verbose_name="Название")
    url = models.CharField(max_length=255, verbose_name="URL", blank=True, null=True)

    class Meta:
        verbose_name = "Правообладатель"
        verbose_name_plural = "Правообладатели"

    def __str__(self): return self.name

class Rating(models.Model):
    user_rating = models.FloatField(null=True, blank=True, verbose_name="Рейтинг книги")
    rated_1_count = models.IntegerField(default=0, verbose_name="Кол-во оценок '1'")
    rated_2_count = models.IntegerField(default=0, verbose_name="Кол-во оценок '2'")
    rated_3_count = models.IntegerField(default=0, verbose_name="Кол-во оценок '3'")
    rated_4_count = models.IntegerField(default=0, verbose_name="Кол-во оценок '4'")
    rated_5_count = models.IntegerField(default=0, verbose_name="Кол-во оценок '5'")
    rated_avg = models.FloatField(verbose_name="Средний рейтинг")
    rated_total_count = models.IntegerField(verbose_name="Общее кол-во оценок")

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self):
        return f"Avg: {self.rated_avg} ({self.rated_total_count} votes)"

class Contributor(models.Model):
    id = models.BigIntegerField(unique=True, verbose_name="ID",default=0)
    uuid = models.UUIDField(primary_key=True, editable=False)
    full_name = models.CharField(max_length=255)
    full_rodit = models.CharField(max_length=255)
    url = models.URLField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.full_name


class Book(models.Model):
    id = models.BigIntegerField(unique=True, verbose_name="ID")
    uuid = models.UUIDField(primary_key=True, editable=False)
    title = models.CharField(max_length=255, verbose_name="Название книги")
    slug = models.SlugField(max_length=300, unique=True)

    # Many-to-Many
    # Связь с участниками через промежуточную таблицу
    contributors = models.ManyToManyField(
        'Contributor',
        through='BookContributor',
        related_name='books'
    )

    # One-to-Many (ForeignKey)
    genres = models.ManyToManyField(
        Genre, null=True, blank=True,
        related_name="books", verbose_name="Жанры"
    )

    publisher = models.ForeignKey(
        Publisher, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="books", verbose_name="Издатель"
    )
    copyrighter = models.ForeignKey(
        Copyrighter, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="books", verbose_name="Копирайтер"
    )
    rightholder = models.ManyToManyField(
        Rightholder, null=True, blank=True,
        related_name="books", verbose_name="Правообладатель"
    )

    # поля из первого JSON
    subtitle = models.CharField(max_length=255, verbose_name="Подзаголовок", null=True, blank=True)
    cover_url = models.CharField(max_length=255, verbose_name="URL обложки")
    url = models.CharField(max_length=500, verbose_name="URL книги")
    is_draft = models.BooleanField(default=False, verbose_name="Черновик")
    art_type = models.IntegerField(verbose_name="Тип контента")
    prices = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    is_auto_speech_gift = models.BooleanField(default=False, verbose_name="Авто-озвучка в подарок")
    min_age = models.PositiveIntegerField(verbose_name="Возрастные ограничения")
    language_code = models.CharField(max_length=10, verbose_name="Код языка")
    last_updated_at = models.DateTimeField(verbose_name="Дата последнего обновления")
    last_released_at = models.DateTimeField(verbose_name="Дата последнего релиза")
    availability = models.BooleanField(default=False, verbose_name="Доступность")
    available_from = models.DateTimeField(verbose_name="Доступна с")

    rating = models.ForeignKey(Rating, on_delete=models.CASCADE, related_name="books", verbose_name="Рейтинг")

    html_annotation = models.TextField(verbose_name="HTML-аннотация")
    html_annotation_litres = models.TextField(verbose_name="HTML-аннотация Litres")
    livelib_rated_count = models.IntegerField(verbose_name="Кол-во оценок LiveLib")
    livelib_rated_avg = models.FloatField(verbose_name="Средняя оценка LiveLib")
    isbn = models.CharField(max_length=20, verbose_name="ISBN", null=True, blank=True)
    publication_date = models.DateField(verbose_name="Дата публикации")
    contents_url = models.CharField(max_length=255, verbose_name="URL содержания", null=True, blank=True)

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title


class BookContributor(models.Model):
    class Role(models.TextChoices):
        AUTHOR = 'author', _('Author')
        EDITOR = 'editor', _('Editor')
        CORRECTOR = 'corrector', _('Corrector')
        ILLUSTRATOR = 'illustrator', _('Illustrator')
        TRANSLATOR = 'translator', _('Translator')
        PUBLISHER = 'publisher', _('Publisher')
        READER = 'reader', _('Reader')

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=Role.choices, verbose_name="Вклад в книгу")

    class Meta:
        # один и тот же человек не может иметь одинаковую роль в одной книге дважды
        constraints = [
            models.UniqueConstraint(
                fields=['book', 'contributor', 'role'],
                name='unique_book_contributor_role'
            )
        ]

    def __str__(self):
        return f"{self.contributor.name} - {self.role}"



class BookManager(models.Manager):
    def get_related(self, current_slug, max_count=3):
        genres = self.filter(slug=current_slug).values_list('genres', flat=True)

        return self.get_queryset().filter(
            genres__in=genres,
            availability=True
        ).exclude(slug=current_slug).distinct()[:max_count]

    def get_random_featured(self, max_count=3):
        return self.get_queryset().filter(availability=True).order_by('?')[:max_count]

    def get_best_sellers(self, max_count=4):
        """
        Возвращает самые популярные книги на основе рейтинга и количества оценок.
        """
        return self.get_queryset().filter(
            availability=True
        ).order_by('-rating__rated_total_count', '-rating__rated_avg')[:max_count]
        #).order_by('-livelib_rated_count', '-livelib_rated_avg')[:max_count]



class Product(Book):
    objects = BookManager()

    class Meta:
        proxy = True