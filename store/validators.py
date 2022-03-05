from django.core.exceptions import ValidationError

def vadlidate_file_size(file):
    max_file_size = 100

    if file.size > max_file_size * 1024:
        raise ValidationError(f"Files cannot be larger than {max_file_size}KB")