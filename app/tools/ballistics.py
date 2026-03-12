import logging

logger = logging.getLogger(__name__)


def check_power_factor(bullet_weight_grains: float, velocity_fps: float):
    """
    Valida se a munição atende aos requisitos de Power Factor do IPSC.
    Use quando o usuário informar peso do projétil (grains) e velocidade (fps)
    para classificar em Major, Minor ou Sub-Minor.
    """
    logger.info(
        "Tool acionada: check_power_factor | bullet_weight_grains=%s velocity_fps=%s",
        bullet_weight_grains,
        velocity_fps,
    )

    power_factor = (bullet_weight_grains * velocity_fps) / 1000

    if power_factor >= 160:
        category = "Major"
        is_qualified = True
    elif power_factor >= 125:
        category = "Minor"
        is_qualified = True
    else:
        category = "Sub-Minor"
        is_qualified = False
        power_factor = 0.0

    return {
        "power_factor": round(power_factor, 2),
        "category": category,
        "is_qualified": is_qualified,
    }


def calculate_hit_factor(total_points: int, time_seconds: float):
    """
    Calcula o Hit Factor oficial do IPSC para uma etapa (stage).
    Use quando o usuário fornecer pontuação total e tempo em segundos
    para avaliar a eficiência do atleta na etapa.
    """
    logger.info(
        "Tool acionada: calculate_hit_factor | total_points=%s time_seconds=%s",
        total_points,
        time_seconds,
    )

    if time_seconds <= 0:
        return {
            "hit_factor": 0.0,
            "status": "error",
            "message": "Time must be greater than zero.",
        }

    hf = total_points / time_seconds
    return {
        "hit_factor": round(hf, 4),
        "status": "success",
        "points": total_points,
        "time": time_seconds,
    }
