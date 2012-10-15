from django import forms

from documents.parsers.django_orm import DjangoORMParser
from documents.parsers.dummy import DummyParser
from documents.parsers.exceptions import ParseError

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
    create_from = forms.CharField(label="Create from", widget=forms.Select(
        choices=DOCUMENT_PARSER_CHOICES), required=False)
    entities = forms.CharField(label="Template", widget=forms.Textarea(),
        initial=EXAMPLE_DJANGO_MODEL, required=False)

    def clean_entities(self):

        if self.cleaned_data.get("create_from"):

            try:
                parser_class = DOCUMENT_PARSERS[self.cleaned_data.get("create_from")]
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