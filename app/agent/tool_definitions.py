# Metadata definitions for the AI Agent to understand available tools

TOOLS_SCHEMA = {
    "calculate_hit_factor": {
        "name": "calculate_hit_factor",
        "description": "Calculates the official IPSC Hit Factor to determine an athlete's efficiency in a stage. Use this whenever the user provides a score and a time to evaluate performance.",
        "parameters": {
            "total_points": {
                "type": "integer",
                "description": "The sum of points from all targets in the stage (A=5, C=3/4, D=1/2). Must be a positive integer.",
                "min_value": 0
            },
            "time_seconds": {
                "type": "float",
                "description": "The total time recorded by the shot timer from the start signal to the last shot. Critical for efficiency calculation.",
                "min_value": 0.01
            }
        },
        "output": "A dictionary containing the HF with 4 decimal places and a performance status."
    },
    
    "check_power_factor": {
        "name": "check_power_factor",
        "description": "Validates if the ammunition meets IPSC safety and power requirements. Use this to determine if a competitor is Major, Minor, or disqualified (Sub-Minor).",
        "parameters": {
            "bullet_weight_grains": {
                "type": "float",
                "description": "The mass of the projectile in Grains. Common values range from 115 to 147 for 9mm.",
            },
            "velocity_fps": {
                "type": "float",
                "description": "The speed of the bullet in Feet Per Second (FPS) as measured by a chronograph.",
            }
        },
        "output": "A dictionary with the Power Factor value, the category (Major/Minor), and qualification status."
    }
}