

def retrieve_context_chunks(user_query: str) -> list:
    """
    Simulate retrieval of relevant knowledge base chunks.
    In production, this would use vector similarity search.
    """
    query = user_query.lower()
    if "co2" in query:
        return [
            "ASHRAE recommends indoor CO₂ levels below 1000 ppm for good air quality.",
            "High CO₂ levels may cause drowsiness and reduce cognitive performance."
        ]
    elif "temperature" in query or "thermal" in query:
        return [
            "ASHRAE Standard 55 suggests maintaining indoor temperatures between 23°C and 26°C for comfort.",
            "Thermal comfort is influenced by air temperature, humidity, and occupant activity." 
        ]
    elif "humidity" in query:
        return [
            "ASHRAE recommends maintaining indoor relative humidity between 30% and 60% to prevent mold and discomfort."
        ]
    elif "energy" in query or "cost" in query:
        return [
            "Energy costs can be reduced by turning off HVAC systems in unoccupied rooms.",
            "Power consumption directly impacts operational costs in smart buildings."
        ]
    else:
        return [
            "Smart building sensors provide real-time data for optimizing energy use and occupant comfort.",
            "Use historical trends and thresholds to trigger alerts and energy-saving actions."
        ]
