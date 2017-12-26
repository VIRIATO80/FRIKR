# -*- coding: utf-8 -*-
from photos.settings import BADWORDS
from django.core.exceptions import ValidationError


def badwords_detector(value):
    """Valida si en value se han escrito tacos en la settings.BADWORDS"""

    for badword in BADWORDS:
        if badword.lower() in value.lower():
            raise ValidationError('La palabra {0} no está permitida.'.format(badword))

    # Si todo va bien, devuelvo los datos limpios
    return True
