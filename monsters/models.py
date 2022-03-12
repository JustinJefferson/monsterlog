from django.core.exceptions import BadRequest
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Monster(models.Model):
    name = models.CharField(max_length=40, unique=True)
    family_1 = models.ForeignKey('Family', on_delete=models.SET_NULL, blank=True, null=True, related_name='family1')
    family_2 = models.ForeignKey('Family', on_delete=models.SET_NULL, blank=True, null=True, related_name='family2')
    hp = models.IntegerField(default=1, validators=[MaxValueValidator(300), MinValueValidator(1)])
    defense = models.IntegerField(default=1, validators=[MaxValueValidator(300), MinValueValidator(1)])
    agility = models.IntegerField(default=1, validators=[MaxValueValidator(300), MinValueValidator(1)])
    strength = models.IntegerField(default=1, validators=[MaxValueValidator(300), MinValueValidator(1)])
    dexterity = models.IntegerField(default=1, validators=[MaxValueValidator(300), MinValueValidator(1)])
    intellect = models.IntegerField(default=1, validators=[MaxValueValidator(300), MinValueValidator(1)])

    def save(self, *args, **kwargs):
        if self.family_1 is None:
            raise BadRequest

        if self.family_2 == self.family_1:
            self.family_2 = None
        super(Monster, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Evolution(models.Model):
    pre_evolution = models.ForeignKey(Monster, on_delete=models.CASCADE, blank=False, null=False, related_name='preevo')
    next_evolution = models.ForeignKey(Monster, on_delete=models.CASCADE, blank=False, null=False, related_name='nextevo')

    def save(self, *args, **kwargs):
        if self.pre_evolution is self.next_evolution:
            raise models.deletion.IntegrityError

        super(Evolution, self).save(*args, **kwargs)

    def __str__(self):
        return self.pre_evolution.name + ' -> ' + self.next_evolution.name


class Family(models.Model):
    name = models.CharField(max_length=15, null=False, unique=True, blank=False)

    def __str__(self):
        return self.name


class Element(models.Model):
    name = models.CharField(max_length=15, blank=False, null=False, unique=True)

    def __str__(self):
        return self.name


class Effectiveness(models.Model):

    class Rating(float, models.Choices):
        NEUTRAL = 1.0, 'Neutral'
        WEAK = 2.0, 'Weak'
        RESIST = 0.5, 'Resist'
        IMMUNE = 0.0, 'Immune'

    rating = models.FloatField(choices=Rating.choices, default=Rating.NEUTRAL)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, blank=False, null=False)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, blank=False, null=False)

    def rating_to_text(self):
        if self.rating == self.Rating.RESIST:
            return 'Resists'
        return self.get_rating_display() + ' to'

    def save(self, *args, **kwargs):
        existing_eff = Effectiveness.objects.filter(
            family=self.family,
            element=self.element
        )

        if not existing_eff:
            super(Effectiveness, self).save(self, *args, **kwargs)
        else:
            raise models.deletion.IntegrityError

    def __str__(self):
        return self.family.name + ' ' + self.rating_to_text() + ' ' + self.element.name


class Skill(models.Model):
    name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.name
