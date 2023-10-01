import pandas as pd
import numpy as np
import pickle
import streamlit as st

class Player:
    def __init__(self, name= None, weight= None, club= None, country = None) -> None:
        self.name = name
        self.weight = weight
        self.club = club
        self.country = country
        self.matches = []
    
    def get_player_df(self):
        return pd.DataFrame({'Name':[self.name],
                             'Weight':[self.weight],
                             'Club':[self.club],
                             'Country': [self.country]})

class Match:
    def __init__(self, player1, player2,  tournament, date, match_round) -> None:
        self.player1 = player1
        self.player2 = player2
        self.tournament = tournament
        self.date = date
        self.match_round = match_round
        self.match_id = ' '.join([self.player1.name, self.player2.name, self.tournament, str(self.date.year), str(self.date.month), str(self.date.day), self.match_round])
        self.winner = None
        self.loser = None
        self.events = []
        self.scores = {player1: 0, player2: 0}

    def get_match_df(self):
        return pd.DataFrame({'Player1':[self.player1.name],
                             'Player2':[self.player2.name],
                             'Tournament': [self.tournament],
                             'Date': [self.date],
                             'Match_Round':[self.match_round],
                             'Winner' :[self.winner],
                             'Loser' : [self.loser]
                             })


class Tournament:
    def __init__(self, tournament_name, date_start, date_end, country, lat, long, matches: list[Match]) -> None:
        self.name = tournament_name
        self.date_start = date_start
        self.date_end = date_end
        self.country = country
        self.lat = lat
        self.long = long
        self.matches = []  # This will hold Match objects

    def add_match(self, match: Match):
        self.matches.append(match)


class MatchPlayer(Player):
    def __init__(self, name, weight, club, country, match: Match) -> None:
        super().__init__(name, weight, club, country)
        self.match = match
        self.warnings = 0
        self.cautions = 0
        self.attacks = []
        self.defenses = []
        self.positions = []
        self.control_ties = []
        self.points = 0

class Event:
    def __init__(self, clock_start, match: Match):
        self.clock_start = clock_start
        self.match = match
        self.preceding_event = None
        self.subsequent_event = None

class PlayerEvent(Event):
    def __init__(self, clock_start, clock_end, match: Match):
        super().__init__(clock_start, match)
        self.clock_end = clock_end
        self.shot_clock_player = None
        self.shot_clock_time = None


class Position(PlayerEvent):
    def __init__(self, clock_start, clock_end, player1: MatchPlayer, player2: MatchPlayer, position_name, match: Match):
        super().__init__(clock_start, clock_end, match)
        self.player1 = player1
        self.player2 = player2
        self.position_name = position_name

class Attack(PlayerEvent):
    def __init__(self, clock_start, clock_end, attack_name, finish, depth, side, points, setup, offender: MatchPlayer, stance, match: Match, point_type):
        super().__init__(clock_start, clock_end, match)
        self.attack_name = attack_name
        self.finish = finish
        self.depth = depth
        self.side = side
        self.setup = setup
        self.offender = offender
        self.stance = stance
        self.points = points
        self.point_type = point_type
        
        if self.points > 0:
            offender.points+=1
            match.scores[offender] += 1
            
        

class Defense(PlayerEvent):
    def __init__(self, clock_start, clock_end, defense_name, side,defender: MatchPlayer, stance, points, point_type, match: Match):
        super().__init__(clock_start, clock_end, match)
        self.defense_name = defense_name
        self.side = side
        self.defender = defender
        self.points = points
        self.point_type = point_type

        if self.points > 0:
            defender.points +=1
            match.scores[defender] +=1

class ControlTies(PlayerEvent):
    def __init__(self, clock_start, clock_end, tie_name, offender, side, match: Match):
        super().__init__(clock_start, clock_end, match)
        self.name = tie_name
        self.offender = offender
        self.side = side

class Whistle(Event):
    def __init__(self, clock_start, clock_end, reason, match: Match):
        super().__init__(clock_start, match)
        self.clock_end = clock_end
        self.reason = reason

class Warning(Whistle):
    def __init__(self, clock_start, clock_end, reason, warned_player: MatchPlayer, match: Match):
        super().__init__(clock_start, clock_end, reason, match)
        self.warned_player = warned_player
        warned_player.warnings+=1

class Caution(Whistle):
    def __init__(self, clock_start, clock_end, reason, cautioned_player: MatchPlayer, match: Match):
        super().__init__(clock_start, clock_end, reason, match)
        self.cautioned_player = cautioned_player
        cautioned_player.cautions += 1
class CautionAnd1(Caution):
    def __init__(self, clock_start, clock_end, reason, cautioned_player: MatchPlayer, points, awarded_player: MatchPlayer, match: Match):
        super().__init__(clock_start, clock_end, reason, cautioned_player, match)
        self.awarded_player = awarded_player
        self.points = points

        if self.points > 0:
            awarded_player.points +=1
            match.scores[awarded_player]+=1
