from collections import defaultdict

from django.core.exceptions import ValidationError


class BaseValidator:
    def __init__(
        self,
        data,
        errors=None,
        ErrorClass=None,
        partial_update=False,
        fields=[],
    ):
        self.errors = defaultdict(list) if errors is None else errors
        self.ErrorClass = ValidationError if ErrorClass is None else ErrorClass
        self.data = data
        self.partial_update = partial_update
        self.fields = fields
        self.ignore_fields = tuple()
        self.validator()

    def methods_call_manager(self):
        my_validate_methods = [
            method_name
            for method_name in dir(self)
            if method_name.startswith("validate_")
        ]

        if self.partial_update:
            methods_to_call = [
                method_name
                for method_name in my_validate_methods
                if method_name[9:] not in self.ignore_fields
            ]
        else:
            methods_to_call = [
                method_name for method_name in my_validate_methods
            ]

        for method in methods_to_call:
            method_select = getattr(self, method)
            method_select()

    def ignore_fields_manage(self):
        self.ignore_fields = tuple(
            [field for field in self.fields if field not in self.data]
        )

    def validator(self):
        if self.partial_update:
            self.ignore_fields_manage()

        self.methods_call_manager()

        if self.errors:
            raise self.ErrorClass(self.errors)
