from django.db import models

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


# A tényleges modell, amelyhez hozzárendelünk egy típust, személyiséget és tanulási útvonalat
class Model(models.Model):
    name = models.CharField(max_length=100, verbose_name="Modell neve")
    type = models.ForeignKey(Type, on_delete=models.CASCADE, verbose_name="Típus")
    personality = models.ForeignKey(Personality, on_delete=models.CASCADE, verbose_name="Személyiség")
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE, verbose_name="Tanulási út")
    is_active = models.BooleanField(default=False, verbose_name="Aktív")  # Kapcsoló, hogy a modell aktív-e

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Modell"
        verbose_name_plural = "Modellek"
        ordering = ['name']

    # Mielőtt mentjük a modellt, kikapcsoljuk a többi aktív modellt
    def save(self, *args, **kwargs):
        if self.is_active:
            # Kikapcsoljuk a többi modellt
            Model.objects.filter(is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
