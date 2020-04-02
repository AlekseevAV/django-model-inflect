from collections import Iterable
import typing

from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import fields
from django.db.models.base import ModelBase

from .cases import InflectCases


SUPPORTED_FIELDS = (
    fields.CharField,
    # Above implies also CommaSeparatedIntegerField, EmailField, FilePathField, SlugField
    # and URLField as they are subclasses of CharField.
    fields.TextField,
)


class InflectMeta(ModelBase):
    inflect_fields_attr_name = 'inflect_fields'

    def __new__(mcs, name, bases, attrs, **kwargs):
        fields_to_inflect = mcs._get_fields_to_inflect(name, attrs)
        mcs._set_inflect_fields(attrs, fields_to_inflect)
        attrs['inflect_fields_attr_name'] = mcs.inflect_fields_attr_name
        return super().__new__(mcs, name, bases, attrs, **kwargs)

    @classmethod
    def _get_fields_to_inflect(mcs, name: str, attrs: dict) -> dict:
        fields_to_inflect = dict()
        inflected_fields = attrs.get(mcs.inflect_fields_attr_name)
        if inflected_fields:
            # inflect_fields = {'some_field_name': ['nomn', 'gent']}
            if isinstance(inflected_fields, dict):
                for field_name, cases in inflected_fields.items():
                    mcs._validate_cases(name, cases)
                    fields_to_inflect[field_name] = tuple(cases)
            # inflect_fields = ['some_field_name']
            elif isinstance(inflected_fields, Iterable):
                for field_name in inflected_fields:
                    fields_to_inflect[field_name] = tuple(dict(InflectCases.DEFAULT_CASES).keys())
        mcs._validate_field_types(name, fields_to_inflect.keys(), attrs)
        return fields_to_inflect

    @classmethod
    def _validate_cases(mcs, name: str, cases: typing.Iterable):
        for case in cases:
            if case not in dict(InflectCases.AVAILABLE_CASES):
                raise ImproperlyConfigured(
                    'Invalid case "{}" in {}. Known cases: {}'.format(case, name, InflectCases.AVAILABLE_CASES))

    @classmethod
    def _validate_field_types(mcs, name: str, field_names_to_validate: typing.Iterable, attrs: dict):
        for field_name in field_names_to_validate:
            if field_name not in attrs:
                raise ImproperlyConfigured('Field "{}" not found in {}.'.format(field_name, name))
            if not isinstance(attrs[field_name], SUPPORTED_FIELDS):
                raise ImproperlyConfigured('Field "{}" in {} type supported.'.format(field_name, name))

    @classmethod
    def _set_inflect_fields(mcs, attrs: dict, fields_to_inflect: dict) -> None:
        for field_name, cases in fields_to_inflect.items():
            for case in cases:
                inflect_field_name = '{}_{}'.format(field_name, case)
                orig_field = attrs[field_name]
                attrs[inflect_field_name] = mcs._create_inflected_field(orig_field, case)

    @classmethod
    def _create_inflected_field(mcs, orig_field, case_code: str):
        case = InflectCases.get_case_by_code(case_code)
        field_attrs = {'null': True, 'blank': True, 'help_text': case.description}
        if getattr(orig_field, 'verbose_name', None):
            field_attrs['verbose_name'] = '{} ({})'.format(getattr(orig_field, 'verbose_name'), case.name)
        field_attrs['max_length'] = getattr(orig_field, 'max_length', None)
        orig_field_type = orig_field.__class__
        return orig_field_type(**field_attrs)


class InflectModel(models.Model, metaclass=InflectMeta):

    class Meta:
        abstract = True
