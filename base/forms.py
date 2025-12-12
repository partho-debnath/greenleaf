from django import forms

CSS_CLASS = "w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition"
PHONE_NUMBER_CSS_CLASS = "flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition"


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if field.label_suffix is None:
                field.label_suffix = ""
            field.widget.attrs.setdefault("class", CSS_CLASS)

    class Meta:
        abstract = True


class BaseModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            if field.label_suffix is None:
                field.label_suffix = ""
            field.widget.attrs.setdefault("class", CSS_CLASS)

    class Meta:
        abstract = True
