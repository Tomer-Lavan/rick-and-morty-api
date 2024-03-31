from fastapi import APIRouter, Request
from urllib.parse import unquote
from app.services import fetch_all_data, fetch_multiple_items
from app.services import analyze_location_survival_rate
from typing import List, Dict, Union
from app.models import SurvivalRate

router = APIRouter()


@router.get("/resident_counts",  response_model=List[Dict[str, Union[str, int]]])
async def get_locations_with_resident_counts(request: Request):
    query_string = unquote(str(request.query_params)).split(']')[0] + ']'
    location_ids_str = query_string.strip("[]")
    location_ids = [int(id_str)
                    for id_str in location_ids_str.split(",") if id_str.isdigit()]

    if location_ids:
        locations = await fetch_multiple_items('location', location_ids)
    else:
        locations = await fetch_all_data("location")

    locations_with_counts = [
        {
            "location": location.get("name", ""),
            "resident_count": len(location["residents"])
        }
        for location in locations
    ]
    return locations_with_counts


@router.get("/analysis/location_survival_rates", response_model=dict[str, SurvivalRate])
async def location_survival_rate():
    characters = await fetch_all_data("character")
    survival_rates = analyze_location_survival_rate(characters)
    return survival_rates
