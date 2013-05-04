from django import forms
from django.forms import RadioSelect

from documents.fields import SearchInput
from documents.parsers import ParseError
from documents.parsers.django_orm import DjangoORMParser
from documents.parsers.dummy import DummyParser

DOCUMENT_PARSER_BLANK = ""
DOCUMENT_PARSER_DJANGO_ORM = "django-orm"

DOCUMENT_PARSER_CHOICES = (
    (DOCUMENT_PARSER_BLANK, "Empty Document"),
    (DOCUMENT_PARSER_DJANGO_ORM, "Django Models"),
)

DOCUMENT_PARSERS = {
    DOCUMENT_PARSER_BLANK: DummyParser,
    DOCUMENT_PARSER_DJANGO_ORM: DjangoORMParser
}

EXAMPLE_DJANGO_MODEL = """
class Foo(models.Model):
    bar = models.CharField(max_length=255)


class Bar(models.Model):
    foo =  models.CharField(max_length=255)
"""


class DocumentForm(forms.Form):
    title = forms.CharField(label="Document title")
    is_public = forms.BooleanField(
        widget=forms.RadioSelect(
            choices=[(True, 'Public'), (False, 'Private')]),
        required=False,
        initial=True,
        label="The visibility of document")
    create_from = forms.CharField(
        label="Create from",
        widget=forms.Select(choices=DOCUMENT_PARSER_CHOICES),
        required=False)
    entities = forms.CharField(
        label="Template",
        widget=forms.Textarea(),
        initial=EXAMPLE_DJANGO_MODEL,
        required=False)
    # TODO: The initial value solution is temporary. Change it.

    def clean_entities(self):
        create_from = self.cleaned_data.get("create_from")
        if create_from:
            try:
                parser_class = DOCUMENT_PARSERS[create_from]
            except KeyError:
                raise forms.ValidationError("Invalid parser.")
            else:
                parser = parser_class(self.cleaned_data.get("entities"))
            try:
                parser.is_valid()
            except ParseError:
                raise forms.ValidationError("Syntax error.")
            else:
                return parser.parsed
        return []


class ForkDocumentForm(forms.Form):
    title = forms.CharField(label="Document title")


class SearchForm(forms.Form):
    keyword = forms.CharField(
        widget=SearchInput(placeholder="Type a keyword"))