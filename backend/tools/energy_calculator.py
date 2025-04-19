def calculate_energy_cost(room: str, power_kw: float, hours: float = 1.0, cost_per_kwh: float = 5.5) -> str:
    estimated_cost = power_kw * hours * cost_per_kwh
    return f"Estimated energy cost for {hours} hour(s) in {room} is ฿{round(estimated_cost, 2)}."

