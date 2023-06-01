import os
import requests
import pprint

from bs4 import BeautifulSoup


class Round:
    def __init__(self, num):
        self.num = num
        self.games = []

    def __str__(self):
        result = f'Round: {self.num}\n'
        for game in self.games:
            result += str(game)
        return result

    def create_game(self, teams):
        game = Game(teams)
        self.games.append(game)
        return game

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.games):
            raise StopIteration
        result = self.games[self.i]
        self.i += 1
        return result


class Game:
    def __init__(self, teams):
        self.teams = teams
        self.votes = []

    def __str__(self):
        result = ''
        if len(self.teams) > 1:
            result += f'{self.teams[0]} vs {self.teams[1]}\n'
        for vote in self.votes:
            result += f'{str(vote)}\n'
        return result

    def as_dict(self):
        d = {}
        for vote in self.votes:
            d[f'{vote.name} {vote.club}'] = vote.value
        return d

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i >= len(self.votes):
            raise StopIteration
        vote = self.votes[self.i]
        result = (f'{vote.name} {vote.club}', vote.value)
        self.i += 1
        return result


class Vote:
    def __init__(self, name, value, club):
        self.name = name
        self.value = value
        self.club = club

    def __str__(self):
        return f'{self.value} {self.name} {self.club}'

    def __hash__(self):
        return hash((self.name, self.club))


class VoteScraper:
    def __init__(self):
        self.year = 2023
        self.url_base = "https://aflcoaches.com.au/awards/the-aflca-champion-player-of-the-year-award/leaderboard/"
        self.suffix = "/202401"
        self.result = requests.get(self.make_url())
        self.doc = BeautifulSoup(self.result.text, "html.parser")
        self.current_round = self._current_round()
        self.season = None
        self.totals = {}

    def _current_round(self) -> int:
        return int(self.doc.find(id="v-pills-round1").contents[1].find_next("h2").string.split()[-1])

    def get_season(self):
        if self.season is None:
            result = []
            for i in range(self.current_round):
                result.append(self.get_round(i + 1))
            self.season = result
        return self.season

    def get_round(self, rnd):
        url = self.make_url(rnd)
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        votes = doc.find_all("div", "col-10")
        clubs = doc.find_all("img", {"class": "club_logo"})
        matches = []
        for i in range(0, len(clubs), 2):
            matches.append((clubs[i].get('alt'), clubs[i+1].get('alt')))
        index = 0
        vote_round = Round(rnd)
        game = None
        for i, vote in enumerate(votes):
            parent = votes[i].parent
            # get the vote value
            value = parent.find("strong").string
            club = parent.find("div", "col-10").contents[1].get_text().strip()[1:-1]
            name = parent.find("div", "col-10").contents[0].get_text().strip()
            if value[0:5] != "Votes" and game is not None:
                value = int(value)
                vote = Vote(name, value, club)
                game.votes.append(vote)
                key = f'{name} {club}'
                if key in self.totals:
                    self.totals[key] += value
                else:
                    self.totals[key] = value
            else:
                # split each game into separate entry
                try:
                    game = vote_round.create_game(matches[index])
                    index += 1
                except IndexError:
                    pass
        return vote_round

    def make_url(self, rnd: int = 0) -> str:
        if rnd == 0:
            return f'{self.url_base}{self.year}/'
        if len(str(rnd)) == 1:
            rnd = f'0{rnd}'
        return f'{self.url_base}{self.year}{self.suffix}{rnd}'

    def write_to_file(self):
        with open(os.path.join('output', 'output.txt'), 'w') as f:
            for rnd in self.get_season():
                f.write(str(rnd))

    def leaderboard(self, top=10):
        self.get_season()
        totals = list(self.totals.items())
        return sorted(totals, key=lambda x: x[1], reverse=True)[0:10]


def main():
    s = VoteScraper()
    s.write_to_file()
    print(s.leaderboard(), sep='\n')


if __name__ == "__main__":
    main()

