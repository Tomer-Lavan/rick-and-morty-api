from fastapi import APIRouter, Depends, HTTPException, status
from app.services import (
    fetch_all_data,
    group_characters_by_origin,
    analyze_origin_inconsistencies,
    analyze_episode_relationships,
    analyze_species_survival_rates,
    analyze_gender_survival_rates
)
from app.models import CharacterFilter, Character, SurvivalRate

router = APIRouter()


def convert_filter_to_dict(filters: CharacterFilter) -> dict:
    """
    Converts a CharacterFilter object to a dictionary, excluding None values.
    Converts enum fields to their value.
    """
    filter_dict = filters.dict(exclude_none=True)
    if filters.status:
        filter_dict['status'] = filters.status.value
    if filters.gender:
        filter_dict['gender'] = filters.gender.value

    return filter_dict


@router.get("/", response_model=list[Character])
async def get_characters(filters: CharacterFilter = Depends()):
    """
    Retrieves a list of characters based on the provided filters.
    Args:
        filters (CharacterFilter, optional): Filter parameters. Defaults to Depends().
    Returns:
        list[Character]: List of characters.
    """
    query_params = convert_filter_to_dict(filters)
    characters = await fetch_all_data("character", query_params)
    if not characters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No characters found"
        )
    return characters


@router.get("/groups_by_origin")
async def get_characters_groups_by_origin():
    """
    Groups characters by their origin.
    Returns:
        dict: Characters grouped by origin.
    """
    characters = await fetch_all_data("character")
    if not characters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No characters found"
        )
    characters_by_origin = group_characters_by_origin(characters)
    return characters_by_origin


@router.get("/origin_inconsistencies")
async def get_origin_inconsistencies():
    """
    Identifies characters with inconsistencies between their origin and current location.
    Returns:
        list: List of characters with inconsistencies.
    """
    characters = await fetch_all_data("character")
    if not characters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No characters found"
        )
    inconsistencies = await analyze_origin_inconsistencies(characters)
    return inconsistencies


@router.get("/analysis/character_appearances")
async def character_appearances():
    """
    Analyzes the number of appearances of characters across episodes.
    Returns:
        dict: Top 10 characters by appearances.
    """
    characters = await fetch_all_data("character")
    if not characters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No characters found"
        )

    character_appearances = {}
    for character in characters:
        for episode_url in character['episode']:
            episode_id = episode_url.split('/')[-1]
            character_appearances[character['id']] = character_appearances.get(
                character['id'], 0) + 1

    sorted_characters = sorted(
        character_appearances.items(), key=lambda x: x[1], reverse=True)
    top_characters_info = []
    for char_id, _ in sorted_characters[:10]:
        for character in characters:
            if character['id'] == char_id:
                top_characters_info.append(character)
                break

    return {"top_characters_by_appearances": top_characters_info}


@router.get("/analysis/species_survival_rates", response_model=dict[str, SurvivalRate])
async def species_survival_rates():
    """
    Analyzes the survival rates of characters by species.
    Returns:
        dict[str, SurvivalRate]: Survival rates by species.
    """
    characters = await fetch_all_data("character")
    if not characters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No characters found"
        )
    survival_rates = analyze_species_survival_rates(characters)
    return survival_rates


@router.get("/analysis/gender_survival_rates", response_model=dict[str, SurvivalRate])
async def gender_survival_rates():
    """
    Analyzes the survival rates of characters by gender.
    Returns:
        dict[str, SurvivalRate]: Survival rates by gender.
    """
    characters = await fetch_all_data("character")
    if not characters:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No characters found"
        )
    survival_rates = analyze_gender_survival_rates(characters)
    return survival_rates
