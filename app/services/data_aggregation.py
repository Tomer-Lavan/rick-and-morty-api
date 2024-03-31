import numpy as np
from typing import List, Dict, Any, Tuple, Union
from collections import Counter
from itertools import combinations
import numpy as np
from app.models import CharacterFilter, Character, SurvivalRate, Episode


def most_common_species(characters: List[Character]) -> List[Tuple[str, int]]:
    species_count = {}
    for character in characters:
        species = character["species"]
        if species in species_count:
            species_count[species] += 1
        else:
            species_count[species] = 1

    sorted_species = sorted(species_count.items(),
                            key=lambda x: x[1], reverse=True)
    return sorted_species


def group_characters_by_origin(characters: List[Character]) -> Dict[str, SurvivalRate]:
    origin_groups = {}

    for char in characters:
        origin = char["origin"]["name"]

        if origin not in origin_groups:
            origin_groups[origin] = []

        origin_groups[origin].append(char)

    return origin_groups


def analyze_charcters_apearences(characters: List[Character]) -> List[Character]:
    character_appearances = {}
    for character in characters:
        for episode_url in character['episode']:
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
    return top_characters_info


def analyze_location_survival_rate(characters: List[Character]) -> Dict[str, SurvivalRate]:
    location_info = {}

    for char in characters:
        location = char["location"]["name"]
        status = char["status"]

        if location not in location_info:
            location_info[location] = {"Alive": 0,
                                       "Dead": 0, "unknown": 0, "total": 0}

        if status in ["Alive", "Dead", "unknown"]:
            location_info[location][status] += 1
            location_info[location]["total"] += 1

    location_survival_rate = {}
    for location, counts in location_info.items():
        alive_rate = (counts["Alive"] / counts["total"]) * \
            100 if counts["total"] > 0 else 0
        location_survival_rate[location] = {
            "survival_rate": alive_rate, "total_characters": counts["total"]
        }

    return location_survival_rate


def analyze_gender_survival_rates(characters: List[Character]) -> Dict[str, Dict[str, SurvivalRate]]:
    gender_info = {}

    for char in characters:
        gender = char["gender"]
        status = char["status"]

        if gender not in gender_info:
            gender_info[gender] = {"Alive": 0,
                                   "Dead": 0, "unknown": 0, "total": 0}

        gender_info[gender][status] += 1
        gender_info[gender]["total"] += 1

    survival_rates = {}
    for gender, counts in gender_info.items():
        alive_rate = (counts["Alive"] / counts["total"]) * \
            100 if counts["total"] > 0 else 0
        survival_rates[gender] = {
            "survival_rate": alive_rate, "total_characters": counts["total"]
        }

    return survival_rates


def analyze_species_survival_rates(characters: List[Character]) -> Dict[str, Dict[str, SurvivalRate]]:
    species_info = {}

    for char in characters:
        species = char["species"]
        status = char["status"]

        if species not in species_info:
            species_info[species] = {"Alive": 0,
                                     "Dead": 0, "unknown": 0, "total": 0}

        species_info[species][status] += 1
        species_info[species]["total"] += 1

    survival_rates = {}
    for species, counts in species_info.items():
        alive_rate = (counts["Alive"] / counts["total"]) * \
            100 if counts["total"] > 0 else 0
        survival_rates[species] = {
            "survival_rate": alive_rate, "total_characters": counts["total"]}

    return survival_rates


def analyze_episode_relationships(episodes: List[Episode]) -> List[Dict[str, Any]]:
    """Analyzes episode character appearances and identifies atypical relationships."""
    all_pairings = Counter()

    for episode in episodes:
        character_ids = {url.split('/')[-1] for url in episode["characters"]}
        all_pairings.update(combinations(character_ids, 2))

    median_frequency = np.median(list(all_pairings.values()))
    atypical_episodes = []

    for episode in episodes:
        character_ids = {url.split('/')[-1] for url in episode["characters"]}
        novel_pairings = sum(1 for pair in combinations(
            character_ids, 2) if all_pairings[pair] <= median_frequency)

        if novel_pairings > 0:
            atypical_episodes.append({
                "id": episode["id"],
                "name": episode["name"],
                "novel_pairings": novel_pairings
            })

    return atypical_episodes


async def analyze_origin_inconsistencies(characters: List[Character]) -> List[Dict[str, Any]]:
    inconsistencies = []
    for character in characters:
        origin_id = character["origin"]["url"].split(
            "/")[-1]
        location_id = character["location"]["url"].split(
            "/")[-1]
        if origin_id != location_id:
            inconsistencies.append({
                "name": character["name"],
                "origin": character["origin"]["name"],
                "location": character["location"]["name"]
            })
    return inconsistencies
