# Django model inflect

Some abstract models and helpers to add inflect fields to django models.

## Install

Install with pip:

    pip install -U django-model-inflect
    
Add to INSTALLED_APPS:

    INSTALLED_APPS = [
        ...
        'model_inflect.apps.ModelInflectConfig',
        ...
    ]

## Work with models

You have some simple model:

    class TestModel(models.Model):
        name = models.CharField(max_length=100, verbose_name='имя', null=True, blank=True)

At first change inheritance to `InflectModel` class:

    from model_inflect.models import InflectModel

    class TestModel(InflectModel):
        name = models.CharField(max_length=100, verbose_name='имя', null=True, blank=True)

Then you need to set `inflect_fields` with fields that you want to have inflected.
If you set `inflect_fields` as list, default inflect cases will be used:

    class TestModel(InflectModel):
        inflect_fields = ['name']  # cases: nomn, gent, datv, accs, ablt, loct 
    
        name = models.CharField(max_length=100, verbose_name='имя', null=True, blank=True)
    
Or you can specify `inflect_fields` as dict to select some of available cases:

    from model_inflect.cases import InflectCases

    class TestModel(InflectModel):
        inflect_fields = {'name': [InflectCases.NOMN, InflectCases.GENT, InflectCases.DATV]}
    
        name = models.CharField(max_length=100, verbose_name='имя', null=True, blank=True)

Create and apply new migration with inflected fields:

    python manage.py makemigrations
    python manage.py migrate

Now you have original field and some extra fields for every of case that you specified in `inflect_fields`
with names like `<orig_field_name>_<case>`:

    # models.py
    from model_inflect.models import InflectModel

    class TestModel(InflectModel):
        inflect_fields = ['name']  # cases: nomn, gent, datv, accs, ablt, loct
    
        name = models.CharField(max_length=100, verbose_name='имя', null=True, blank=True)

    # any other code
    test = TestModel.objects.last()
    test.name
    test.name_nomn
    test.name_gent
    test.name_datv
    ...


## Inflector

`Inflector` - singleton class to inflect strings

    from model_inflect.inflector import Inflector
    
    i = Inflector()

You can inflect word to one case
    
    i.inflect_to_case('Иван', 'gent')
    'ивана'
    i.inflect_to_case('Иван', 'datv')
    'ивану'

Or to multiple cases at once:

    i.inflect_to_cases('Иван', ['gent', 'datv'])
    {'gent': 'ивана', 'datv': 'ивану'}

And you can pass multiple words:

    i.inflect_to_case('Иванов Иван Иванович', 'datv')
    'иванову ивану ивановичу'
