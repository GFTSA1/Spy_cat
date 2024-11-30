from django.db import models


class Cat(models.Model):
    name = models.CharField(max_length=100)
    experience = models.IntegerField()
    breed = models.CharField(max_length=200)
    salary = models.FloatField()

    def __str__(self):
        return self.name


class Target(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=150)
    notes = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Mission(models.Model):
    cat = models.ForeignKey(Cat, on_delete=models.SET_NULL, default=None, blank=True, null=True)
    targets = models.ManyToManyField(Target)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Mission by {self.cat.name if self.cat else 'Unknown'}"


