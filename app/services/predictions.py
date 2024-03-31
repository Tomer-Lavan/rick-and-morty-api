from typing import Dict


def predict_survival_chance(location: str, gender: str, species: str, location_survival: Dict[str, float], gender_survival: Dict[str, float], species_survival: Dict[str, float]) -> float:
    """
    Predicts the survival chance of a character based on location, gender, and species survival rates.
    Currently the weights of each feature (location, gender and species) is equal, 
    in the future we can improve that by running machine learniing/satistics models to get more accurate weights.
    Args:
        location (str): The location of the character.
        gender (str): The gender of the character.
        species (str): The species of the character.
        location_survival (Dict[str, float]): Dictionary with locations as keys and survival rates as values.
        gender_survival (Dict[str, float]): Dictionary with genders as keys and survival rates as values.
        species_survival (Dict[str, float]): Dictionary with species as keys and survival rates as values.
    Returns:
        float: The predicted survival chance of the character.
    Raises:
        KeyError: If survival rate data is not found for the given location, gender, or species.
    """
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
