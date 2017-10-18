from django import forms


class SearchInput(forms.TextInput):
    input_type = "search"

    def __init__(self, attrs=None, placeholder=None):
        super(SearchInput, self).__init__(attrs)

        if placeholder is not None:
            self.attrs["placeholder"] = placeholder
