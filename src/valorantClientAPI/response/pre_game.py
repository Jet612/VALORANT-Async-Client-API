from enum import Enum
from dataclasses import dataclass
from typing import List, Any
from datetime import datetime


class CharacterSelectionState(Enum):
    EMPTY = ""
    LOCKED = "locked"


@dataclass
class PlayerIdentity:
    subject: str
    player_card_id: str
    player_title_id: str
    account_level: int
    preferred_level_border_id: str
    incognito: bool
    hide_account_level: bool


class PregamePlayerState(Enum):
    JOINED = "joined"


@dataclass
class SeasonalBadgeInfo:
    season_id: str
    number_of_wins: int
    wins_by_tier: None
    rank: int
    leaderboard_rank: int


@dataclass
class Player:
    subject: str
    character_id: str
    character_selection_state: CharacterSelectionState
    pregame_player_state: PregamePlayerState
    competitive_tier: int
    player_identity: PlayerIdentity
    seasonal_badge_info: SeasonalBadgeInfo
    is_captain: bool


@dataclass
class Team:
    team_id: str
    players: List[Player]


@dataclass
class CastedVotes:
    pass


@dataclass
class PreGameDetails:
    id: str
    version: int
    teams: List[Team]
    ally_team: Team
    enemy_team: None
    observer_subjects: List[Any]
    match_coaches: List[Any]
    enemy_team_size: int
    enemy_team_lock_count: int
    pregame_state: str
    last_updated: datetime
    map_id: str
    map_select_pool: List[Any]
    banned_map_i_ds: List[Any]
    casted_votes: CastedVotes
    map_select_steps: List[Any]
    map_select_step: int
    team1: str
    game_pod_id: str
    mode: str
    voice_session_id: str
    muc_name: str
    queue_id: str
    provisioning_flow_id: str
    is_ranked: bool
    phase_time_remaining_ns: int
    step_time_remaining_ns: int
    alt_modes_flag_ada: bool
    tournament_metadata: None
    roster_metadata: None
