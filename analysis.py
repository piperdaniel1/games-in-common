from typing import List, Union
from fuzzywuzzy import fuzz as fw

class Game:
    def __init__(self, name: str, year: Union[int, None] = None, score: Union[int, None] = None):
        self.name = name
        self.year = year
        self.score = score

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"Game('{self.name}', {self.year}, {self.score})"
    
    def __eq__(self, other: 'Game'):
        iname = self.name
        oname = other.name

        iname = iname.lower()
        oname = oname.lower()

        iname.strip("\n.!?,;:()[]{} ")
        oname.strip("\n.!?,;:()[]{} ")

        ratio = fw.ratio(iname, oname)
        return ratio > 85

class GameList:
    def __init__(self, player_name : str, game_list : List[Game]):
        self.player_name = player_name
        self.game_list = game_list

    def __str__(self):
        str = f"{self.player_name} wants to play {len(self.game_list)} games"
        #for game in self.game_list:
        #    str += f"\n{game}"
        return str

    def print_overlap(self, other: 'GameList'):
        overlaps = 0
        for game in self.game_list:
            for other_game in other.game_list:
                if game == other_game:
                    print(f"{self.player_name} and {other.player_name} both want to play {game}")
                    overlaps += 1

        if overlaps == 0:
            print(f"{self.player_name} and {other.player_name} do not have any games in common")

    def double_print_overlap(self, other: 'GameList', other2: 'GameList'):
        prelim = []
        overlaps = 0
        for game in self.game_list:
            for other_game in other.game_list:
                if game == other_game:
                    prelim.append(game)

        for game in other2.game_list:
            for other_game in prelim:
                if game == other_game:
                    print(f"{self.player_name}, {other.player_name}, and {other2.player_name} all want to play {game}")
                    overlaps += 1

        if overlaps == 0:
            print(f"{self.player_name}, {other.player_name}, and {other2.player_name} do not have any games in common")

    def triple_print_overlap(self, other: 'GameList', other2: 'GameList', other3: 'GameList'):
        prelim = []
        overlaps = 0
        for game in self.game_list:
            for other_game in other.game_list:
                if game == other_game:
                    prelim.append(game)

        prelim2 = []
        for game in other2.game_list:
            for other_game in prelim:
                if game == other_game:
                    prelim2.append(game)

        for game in other3.game_list:
            for other_game in prelim2:
                if game == other_game:
                    print(f"{self.player_name}, {other.player_name}, {other2.player_name}, and {other3.player_name} all want to play {game}")
                    overlaps += 1
        
        if overlaps == 0:
            print(f"{self.player_name}, {other.player_name}, {other2.player_name}, and {other3.player_name} do not have any games in common")

    def unique_games(self, others: List['GameList']):
        unique_games = []
        overlaps = 0
        for game in self.game_list:
            for other in others:
                for o_game in other.game_list:
                    if game == o_game:
                        overlaps += 1
                        break
                    if overlaps > 0:
                        break
            if overlaps == 0:
                unique_games.append(game)
            overlaps = 0

        for game in unique_games:
            print(f"{self.player_name} doesn't have anyone to play {game} with.")

        if len(unique_games) == 0:
            print(f"{self.player_name} has no unique games.")

with open('games.txt', 'r') as f:
    games : List[str] = f.readlines()
    game_lists : List[GameList] = []

    player_name : Union[str, None] = None
    game_list : List[Game] = []

    for line in games:
        if line[0] == '>':
            if player_name is not None:
                game_lists.append(GameList(player_name, game_list))
                game_list = []

            player_name = line[1:].strip()
        else:
            if line != '\n':
                game_list.append(Game(line.strip()))

    if player_name is not None:
        game_lists.append(GameList(player_name, game_list))
        game_list = []

print(f"Imported {len(game_lists)} game lists")
game_lists[0].print_overlap(game_lists[1])
print()
game_lists[0].print_overlap(game_lists[2])
print()
game_lists[1].print_overlap(game_lists[2])
print()
game_lists[0].double_print_overlap(game_lists[1], game_lists[2])
print()
game_lists[1].double_print_overlap(game_lists[2], game_lists[3])
print()
game_lists[0].triple_print_overlap(game_lists[1], game_lists[2], game_lists[3])
print("\n")

others = [game_lists[3], game_lists[1], game_lists[2]]
game_lists[0].unique_games(others)

print()

others = [game_lists[0], game_lists[3], game_lists[2]]
game_lists[1].unique_games(others)

print()

others = [game_lists[0], game_lists[1], game_lists[3]]
game_lists[2].unique_games(others)

print()

others = [game_lists[0], game_lists[1], game_lists[2]]
game_lists[3].unique_games(others)

print()

for elem in game_lists:
    print(elem)
