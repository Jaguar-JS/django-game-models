import init_django_orm  # noqa: F401

import json
from typing import Any, Optional
from db.models import Race, Skill, Guild, Player


def load_players_from_file() -> dict[str, Any]:
    with open('players.json') as f:
        return json.load(f)


def create_race(race_info: dict[str, Any]) -> Race:
    race_name = race_info['name']
    race, _ = Race.objects.get_or_create(
        name=race_name,
        defaults={'description': race_info.get('description', '')})
    return race


def create_skills(skills_info: dict[str, Any], race: Race) -> None:
    print(skills_info)
    for skill in skills_info:
        Skill.objects.get_or_create(
            name=skill["name"],
            bonus=skill["bonus"],
            race=race)


def create_guild(guild_info: Optional[dict[str, Any]]) -> Optional[Guild]:
    if guild_info:
        guild_name = guild_info['name']
        guild, _ = Guild.objects.get_or_create(
            name=guild_name,
            defaults={'description': guild_info.get('description', '')})
        return guild
    return None


def create_player(
        player: str,
        player_info: dict[str, Any],
        race: Race,
        guild: Optional[Guild]
) -> None:
    Player.objects.get_or_create(
        nickname=player,
        defaults={
            'email': player_info['email'],
            'bio': player_info['bio'],
            'race': race,
            'guild': guild
        }
    )


def main() -> None:
    players = load_players_from_file()
    for player, player_info in players.items():
        race = create_race(player_info.get("race"))
        create_skills(player_info.get("race").get("skills"), race)
        guild = create_guild(player_info.get("guild"))
        create_player(player, player_info, race, guild)


if __name__ == "__main__":
    main()
