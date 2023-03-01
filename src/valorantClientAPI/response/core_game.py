from dataclasses import dataclass
from typing import List, Dict
from enum import Enum


@dataclass
class ConnectionDetails:
    game_server_hosts: List[str]
    game_server_host: str
    game_server_port: int
    game_server_obfuscated_ip: int
    game_client_hash: int
    player_key: str


@dataclass
class MatchmakingData:
    queue_id: str
    is_ranked: bool


@dataclass
class PlayerIdentity:
    subject: str
    player_card_id: str
    player_title_id: str
    account_level: int
    preferred_level_border_id: str
    incognito: bool
    hide_account_level: bool


@dataclass
class SeasonalBadgeInfo:
    season_id: str
    number_of_wins: int
    wins_by_tier: None
    rank: int
    leaderboard_rank: int


class TeamID(Enum):
    BLUE = "Blue"
    RED = "Red"


@dataclass
class Player:
    subject: str
    team_id: TeamID
    character_id: str
    player_identity: PlayerIdentity
    seasonal_badge_info: SeasonalBadgeInfo
    is_coach: bool
    is_associated: bool


@dataclass
class CoreGameDetails:
    httpStatus = 200
    match_id: str
    version: int
    state: str
    map_id: str
    mode_id: str
    provisioning_flow: str
    game_pod_id: str
    all_muc_name: str
    team_muc_name: str
    team_voice_id: str
    is_reconnectable: bool
    connection_details: ConnectionDetails
    post_game_details: None
    players: List[Player]
    matchmaking_data: MatchmakingData


# Fetch match loadout
@dataclass
class SocketItem:
    id: str
    type_id: str


@dataclass
class Socket:
    id: str
    item: SocketItem


@dataclass
class ItemValue:
    id: str
    type_id: str
    sockets: Dict[str, Socket]


@dataclass
class SpraySelection:
    socket_id: str
    spray_id: str
    level_id: str


@dataclass
class Sprays:
    spray_selections: List[SpraySelection]


@dataclass
class LoadoutLoadout:
    sprays: Sprays
    items: Dict[str, ItemValue]


@dataclass
class LoadoutElement:
    character_id: str
    loadout: LoadoutLoadout


@dataclass
class CoreGameMatchLoadout:
    httpStatus = 200
    loadouts: List[LoadoutElement]