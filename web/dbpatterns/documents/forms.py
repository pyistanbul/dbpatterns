from django import forms

from documents.parsers.django_orm import DjangoORMParser
from documents.parsers.dummy import DummyParser
from documents.parsers.exceptions import ParseError

DOCUMENT_PARSER_BLANK = ""
DOCUMENT_PARSER_DJANGO_ORM = "django-orm"

DOCUMENT_PARSER_CHOICES = (
    (DOCUMENT_PARSER_BLANK, "Empty Document"),
    (DOCUMENT_PARSER_DJANGO_ORM, "Django ORM"),
)

DOCUMENT_PARSERS = {
    DOCUMENT_PARSER_BLANK: DummyParser,
    DOCUMENT_PARSER_DJANGO_ORM: DjangoORMParser
}

class DocumentForm(forms.Form):
    title = forms.CharField("Document title")
    create_from = forms.CharField("Create from", widget=forms.Select(
        choices=DOCUMENT_PARSER_CHOICES), required=False)
    entities = forms.CharField("Template", widget=forms.Textarea(), required=False)

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