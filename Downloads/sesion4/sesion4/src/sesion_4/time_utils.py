# src/time_utils.py

import re
from datetime import datetime, timedelta

def calculate_duration(start: str, end: str) -> int:
    """
    Calcula la duración en minutos entre dos horas en formato HH:MM
    """
    if not re.match(r"^\d{2}:\d{2}$", start) or not re.match(r"^\d{2}:\d{2}$", end):
        raise ValueError("Las horas deben tener el formato estricto HH:MM")

    fmt = "%H:%M"
    start_dt = datetime.strptime(start, fmt)
    end_dt = datetime.strptime(end, fmt)

    delta = end_dt - start_dt
    
    if delta.total_seconds() < 0:
        delta += timedelta(days=1)
        
    return int(delta.total_seconds() / 60)


def is_valid_shift(start: str, end: str) -> bool:
    """
    Un turno es válido si dura entre 30 minutos y 8 horas
    """
    if not re.match(r"^\d{2}:\d{2}$", start) or not re.match(r"^\d{2}:\d{2}$", end):
        raise ValueError("Las horas deben tener el formato estricto HH:MM")

    duration = calculate_duration(start, end)
    return 30 <= duration <= 480