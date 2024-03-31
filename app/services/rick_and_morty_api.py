import httpx
from typing import List, Dict, Any
from fastapi import HTTPException
from app.services.cache_decorator import cache_data

BASE_URL = "https://rickandmortyapi.com/api"


@cache_data(key_format="fetch_data:{endpoint}:{params}")
async def fetch_data(endpoint: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    url = f"{BASE_URL}/{endpoint}"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()["results"]
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@cache_data(key_format="fetch_all_data:{endpoint}:{params}")
async def fetch_all_data(endpoint: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    url = f"{BASE_URL}/{endpoint}"
    results = []
    next_page = url

    async with httpx.AsyncClient() as client:
        while next_page:
            response = await client.get(next_page,  params=params)
            data = response.json()
            results.extend(data['results'])
            next_page = data['info']['next']

        return results


@cache_data(key_format="fetch_multiple_items:{endpoint}:{ids}")
async def fetch_multiple_items(endpoint, ids: List[str]) -> List[Dict[str, Any]]:
    ids_string = ','.join(map(str, ids))
    url = f"{BASE_URL}/{endpoint}/{ids_string}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return data


@cache_data(key_format="fetch_single_item:{endpoint}:{id}")
async def fetch_single_item(endpoint, id: str) -> List[Dict[str, Any]]:
    url = f"{BASE_URL}/{endpoint}/{id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()
        return data
