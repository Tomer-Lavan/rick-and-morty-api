from typing import Dict


def predict_survival_chance(location: str, gender: str, species: str, location_survival: Dict[str, float], gender_survival: Dict[str, float], species_survival: Dict[str, float]) -> float:
    try:
        location_rate = location_survival[location]
    except KeyError:
        raise KeyError(f"No survival rate data found for location: {location}")
    try:
        gender_rate = gender_survival[gender]
    except KeyError:
        raise KeyError(f"No survival rate data found for location: {gender}")
    try:
        species_rate = species_survival[species]
    except KeyError:
        raise KeyError(f"No survival rate data found for location: {species}")

    predicted_survival_chance = (
        location_rate['survival_rate'] + gender_rate['survival_rate'] + species_rate['survival_rate']) / 3

    return predicted_survival_chance
