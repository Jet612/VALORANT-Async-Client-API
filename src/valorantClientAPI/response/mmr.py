# Dataclass for FetchMMRHistory

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class History:
    match_id: str
    game_start_time: int
    queue_id: str
    start_time_unixtimestamp: datetime = field(default=False, init=False)

    def __post_init__(self):
        """
        The original value needs to divided by 1000 to get the unixtimstamp 
        I don't know yet as to why. 
        Also I didn't wanted to do extra processing of the raw data, hence
        added this additional field.
        """
        self.start_time = self.game_start_time//1000 
    
#this is the top layer class to be imported
@dataclass
class MatchHistory:
    httpStatus = 200
    subject: str
    begin_index: int
    end_index: int
    total: int
    history: List[History]


# Match Details DTO
@dataclass
class PlayerLocation:
    subject: str
    view_radians: float
    location: Dict[str, int]


@dataclass
class MatchInfo:
    match_id: str
    map_id: str
    game_pod_id: str
    game_loop_zone: str
    game_server_address: str
    game_version: str
    game_length_millis: int
    game_start_millis: int
    provisioning_flow_id: str
    is_completed: bool
    custom_game_name: str
    force_post_processing: bool
    queue_id: str
    game_mode: str
    is_ranked: bool
    is_match_sampled: bool
    season_id: str
    completion_state: str
    platform_type: str
    party_rr_penalties: Dict[str, int]
    should_match_disable_penalties: bool


@dataclass
class Player:
    subject: str
    game_name: str
    tag_line: str
    platform_info: Dict[str, str]
    team_id: str
    party_id: str
    character_id: str
    stats: Dict[str, Any]
    competitive_tier: int
    is_observer: bool
    player_card: str
    player_title: str
    account_level: int
    behavior_factors: Dict
    new_player_experience_details: Dict[str, Dict[str, Any]]
    round_damage: Optional[List[Dict]] = None
    session_playtime_minutes: Optional[int] = 0
    preferred_level_border: Optional[str] = None
    xp_modifications: Optional[List[Dict[str, Any]]] = None


@dataclass
class Team:
    team_id: str
    won: bool
    rounds_played: int
    rounds_won: int
    num_points: int


@dataclass
class Kill:
    game_time: int
    round_time: int
    killer: str
    victim: str
    victim_location: Dict
    assistants: List[str]
    player_locations: List[PlayerLocation]
    finishing_damage: Dict
    round: Optional[int] = None


@dataclass()
class PlayerStat:
    subject: str
    kills: List[Dict]
    damage: List[Dict]
    score: int
    economy: Dict
    ability: Dict
    wasAfk: bool
    wasPenalized: bool
    stayedInSpawn: bool


@dataclass
class RoundResults:
    round_num: int
    round_result: str
    round_ceremony: str
    winning_team: str
    plant_round_time: int
    plant_location: Dict
    plant_site: str
    defuse_round_time: int
    defuse_location: Dict
    round_result_code: str
    player_stats: List[PlayerStat] = None
    player_scores: Optional[List[Dict]] = None
    player_economies: Optional[List[Dict]] = None
    bomb_planter: Optional[str] = None
    bomb_defuser: Optional[str] = None
    plant_player_locations: Optional[List[PlayerLocation]] = None
    defuse_player_locations: Optional[List[PlayerLocation]] = None


@dataclass
class MatchDetails:
    """
    The match details of a given match_id
    """
    httpStatus = 200
    match_info: MatchInfo
    players: List[Player]
    bots: List[Any]
    coaches: List[Any]
    teams: List[Team]
    round_results: List[RoundResults]
    kills: List[Kill]
