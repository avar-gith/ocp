# file: adan/models.py

from django.db import models

# API modell, amely tárolja az API-k nevét, teljes URL-jét és leírását
class API(models.Model):
    name = models.CharField(max_length=200, verbose_name="API neve")
    url = models.URLField(verbose_name="API URL")  # URLField teljes URL-ekhez
    description = models.TextField(verbose_name="API leírása", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "API"
        verbose_name_plural = "API-k"
        ordering = ['name']

# Modell típusa
class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name="Típus neve")
    value = models.CharField(max_length=100, verbose_name="Típus értéke")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Típus"
        verbose_name_plural = "Típusok"
        ordering = ['name']


# Modell személyisége
class Personality(models.Model):
    name = models.CharField(max_length=100, verbose_name="Személyiség neve")
    value = models.CharField(max_length=100, verbose_name="Személyiség értéke")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Személyiség"
        verbose_name_plural = "Személyiségek"
        ordering = ['name']


# Modell tanulási útja
class LearningPath(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tanulási út neve")
    value = models.CharField(max_length=100, verbose_name="Tanulási út értéke")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tanulási út"
        verbose_name_plural = "Tanulási utak"
        ordering = ['name']


# A tényleges modell, amelyhez hozzárendelünk egy típust, személyiséget és tanulási útvonalat, valamint API-kat
class Model(models.Model):
    name = models.CharField(max_length=100, verbose_name="Modell neve")  # A modell neve
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Típus")  # Kapcsolódik a Type modellhez
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE, verbose_name="Személyiség", blank=True, null=True)  # Kapcsolódik a Personality modellhez, de nem kötelező
    learning_paths = models.ManyToManyField(LearningPath, verbose_name="Tanulási utak", blank=True)  # Kapcsolódik több LearningPath modellhez
    apis = models.ManyToManyField(API, verbose_name="Kapcsolódó API-k", blank=True)  # Kapcsolódó API-k
    is_active = models.BooleanField(default=False, verbose_name="Aktív")  # Új mező az aktív állapot jelzésére

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Modell"
        verbose_name_plural = "Modellek"
        ordering = ['name']
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Modell"
        verbose_name_plural = "Modellek"
        ordering = ['name']

    # Mielőtt mentjük a modellt, kikapcsoljuk a többi aktív modellt
    def save(self, *args, **kwargs):
        if self.is_active:
            # Kikapcsoljuk a többi modellt, ha ez a modell aktív
            Model.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
