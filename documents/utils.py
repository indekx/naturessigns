from django.core.exceptions import ValidationError


#File size validation utility
def validate_file_size(value):
    file_size = value.size
    if file_size > 5242880:
        raise ValidationError('Allowed maximum file size is 5MB')
    else:
        return value