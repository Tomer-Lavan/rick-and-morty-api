from fastapi import APIRouter, HTTPException, status
from app.services import fetch_all_data
from app.services import (
    most_common_species,
    analyze_location_survival_rate,
    analyze_gender_survival_rates,
    analyze_species_survival_rates,
    predict_survival_chance,
)
from app.models import SurvivalPrediction

router = APIRouter()


@router.get("/most_common_species")
async def get_most_common_species():
    """
    Retrieves the most common species among characters.
    Returns:
        dict: Dictionary with species as keys and their counts as values.
    """
    characters = await fetch_all_data("character")
    return {"most_common_species": most_common_species(characters)}


@router.get("/analysis/predict_survival_chance", response_model=SurvivalPrediction)
async def get_survival_chance_prediction(location: str, gender: str, species: str):
    """
    Predicts the survival chance of a character based on location, gender, and species.
    Currently the weights of each feature is equal, 
    in the future we can improve that by running machine learniing/satistics models to get more accurate weights.
    Args:
        location (str): The location of the character.
        gender (str): The gender of the character.
        species (str): The species of the character.
    Returns:
        SurvivalPrediction: Object containing the predicted survival chance.
    """
    characters = await fetch_all_data("character")
    if not characters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No characters found"
        )

    location_survival_rates = analyze_location_survival_rate(characters)
    gender_survival_rates = analyze_gender_survival_rates(characters)
    species_survival_rates = analyze_species_survival_rates(characters)

    try:
        survival_chance = predict_survival_chance(
            location, gender, species, location_survival_rates, gender_survival_rates, species_survival_rates)
    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )

    return {"location": location, "gender": gender, "species": species, "predicted_survival_chance": survival_chance}
