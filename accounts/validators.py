
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _ 


phone_regex = re.compile(r"^(?:\+98|0)9\d{2}\d{7}$")

def validate_iranian_phone(value):
    if not phone_regex.match(value):
        raise ValidationError(_('Enter a valid Iranian cellphone number.'))