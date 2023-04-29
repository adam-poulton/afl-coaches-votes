from bs4 import BeautifulSoup
import requests


class VoteScraper:
    def __init__(self):
        self.year = 2023
        self.url_base = f"https://aflcoaches.com.au/awards/the-aflca-champion-player-of-the-year-award/leaderboard/"
        self.suffix = "/2024010"
        self.result = requests.get(self.make_url())
        self.doc = BeautifulSoup(self.result.text, "html.parser")
        self.current_round = self._current_round()

    def _current_round(self) -> int:
        return int(self.doc.find(id="v-pills-round1").contents[1].find_next("h2").string.split()[-1])

    def get_season(self):
        result = []
        for i in range(self.current_round):
            result.append(self.get_round(i + 1))
        return result

    def get_round(self, rnd):
        url = self.make_url(rnd)
        result = requests.get(url)
        doc = BeautifulSoup(result.text, "html.parser")
        votes = doc.find_all("div", "col-10")
        last = 0
        index = -1
        result = []
        for i, vote in enumerate(votes):
            parent = votes[i].parent
            # get the vote value
            value = parent.find("strong").string
            name = parent.find("div", "col-10").contents[0].get_text().strip()
            if value[0:5] != "Votes":
                value = int(value)
                # split each game into separate entry
                if value > last:
                    index += 1
                    result.append([])
                last = value
                result[index].append((name, value))
        return result

    def make_url(self, rnd: int = 0) -> str:
        if rnd == 0:
            return f'{self.url_base}{self.year}/'
        return f'{self.url_base}{self.year}{self.suffix}{rnd}'


def main():
    s = VoteScraper()
    print(s.get_season())


if __name__ == "__main__":
    main()

