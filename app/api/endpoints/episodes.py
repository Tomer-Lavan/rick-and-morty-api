from fastapi import APIRouter, Query, HTTPException, status
from app.services import fetch_all_data
from app.models import Episode

router = APIRouter()


@router.get("/episodes_with_most_characters", response_model=list[Episode])
async def get_episodes_with_most_characters(
    k: int = Query(10, alias="top",
                   description="Number of episodes to retrieve")
):
    episodes = await fetch_all_data("episode")
    if not episodes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No episodes found"
        )
    episodes_with_count = [
        {"count": len(episode["characters"]), "episode": episode} for episode in episodes
    ]
    episodes_with_count.sort(key=lambda x: x["count"], reverse=True)
    top_episodes = [item["episode"] for item in episodes_with_count[:k]]
    return top_episodes
