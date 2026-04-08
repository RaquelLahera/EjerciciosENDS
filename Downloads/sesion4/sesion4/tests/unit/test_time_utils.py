import pytest
from src.sesion_4.time_utils import calculate_duration, is_valid_shift


@pytest.mark.parametrize(
    "start, end, expected",
    [
        # Casos normales
        ("10:00", "12:00", 120),
        ("08:30", "17:00", 510),
        # Casos borde
        ("10:00", "10:00", 0),
        # Turnos que cruzan medianoche (exigiendo el valor correcto para detectar el error real)
        ("23:00", "01:00", 120),
        ("22:00", "06:00", 480),
        ("14:00", "12:00", 1320), # De 2PM a 12PM del día siguiente
    ]
)
def test_calculate_duration_valid_inputs(start, end, expected):
    # Arrange: Los datos vienen parametrizados

    # Act: Ejecutamos la función a probar
    result = calculate_duration(start, end)

    # Assert: Verificamos el resultado
    assert result == expected


@pytest.mark.parametrize(
    "start, end",
    [
        ("25:00", "12:00"),  # Hora inválida (fuera de 0-23)
        ("10:00", "12:60"),  # Minuto inválido (fuera de 0-59)
        ("10:00", "2 pm"),   # Formato AM/PM en lugar de 24h
        ("1000", "1200"),    # Falta el separador de dos puntos
        ("", "12:00"),       # Cadena vacía
        ("diez", "doce"),    # Texto en lugar de números
        ("24:00", "01:00"),  # El máximo válido es 23:59
        ("09:0", "10:00"),   # Formato incompleto
        ("-1:00", "10:00"),  # Hora negativa
    ]
)
def test_calculate_duration_invalid_inputs(start, end):
    # Arrange: Los datos inválidos vienen parametrizados

    # Act & Assert: Verificamos que se levanta la excepción esperada
    with pytest.raises(ValueError):
        calculate_duration(start, end)


@pytest.mark.parametrize(
    "start, end, expected",
    [
        ("10:00", "14:00", True),   # Caso normal: 4 horas
        ("10:00", "10:30", True),   # Caso borde: exactamente 30 min (límite inferior)
        ("10:00", "18:00", True),   # Caso borde: exactamente 8 horas (límite superior)
        ("10:00", "10:29", False),  # Caso borde: justo por debajo del límite inferior (29 min)
        ("10:00", "18:01", False),  # Caso borde: justo por encima del límite superior (481 min)
        # Turnos cruzando medianoche (detectarán el error real en la validación)
        ("23:00", "01:00", True),   # 2 horas, debería ser válido
        ("22:00", "07:00", False),  # 9 horas, excede el máximo
        ("23:30", "00:00", True),   # Caso borde cruzando medianoche: exactamente 30 min
    ]
)
def test_is_valid_shift(start, end, expected):
    # Arrange: Los datos vienen parametrizados

    # Act
    result = is_valid_shift(start, end)

    # Assert
    assert result == expected