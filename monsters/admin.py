from django.contrib import admin

from .models import Monster, Family, Element, Effectiveness, Skill, Evolution


class EvolutionInlines(admin.TabularInline):
    model = Evolution
    fk_name = 'next_evolution'
    max_num = 1


class MonsterAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'family_1', 'family_2')}),
        ('Stats', {'fields': (('hp', 'defense', 'agility'), ('strength', 'dexterity', 'intellect'))})
    )
    inlines = [EvolutionInlines]


admin.site.register(Monster, MonsterAdmin)
admin.site.register(Family)
admin.site.register(Element)
admin.site.register(Effectiveness)
