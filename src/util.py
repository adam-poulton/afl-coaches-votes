import itertools
from functools import reduce


def generate_possible_votes(public_votes) -> dict:
    """
    Generates valid sequences of split votes based on the public vote totals
    TODO: fix case of multiple players with same total e.g { player1: [(4, 0), (4, 0)], player2: [(0, 4), (0, 4)] ...}
    :param public_votes: a list of (player_key, votes) tuples from the publicly available information for a given game
    :return: a dictionary of `player_key`s and corresponding list of possible split votes tuples
    """
    pub_total = sorted(reduce(lambda acc, pair: acc + [pair[1]], public_votes, []))
    votes1 = [0] * (len(pub_total) - 5) + [1, 2, 3, 4, 5]
    votes2 = votes1.copy()
    pairings = generate_pairings(votes1, votes2, [], [])
    valid = []
    for votes in pairings:
        total = sorted(pairing_totals(votes))
        if total == pub_total:
            valid.append(sorted(votes, key=lambda x: sum(x), reverse=True))
    combos = {}
    for i, vote in enumerate(pub_votes):
        combos[vote[0]] = [valid[x][i] for x in range(len(valid))]
    return combos


def is_valid_sequence(votes) -> bool:
    """
    Checks if a split sequence of coaches list1 is valid
    e.g: [(5, 5), (4, 4), (3, 3), (2, 2), (1, 1)] -> True
         [(5, 4), (4, 4), (4, 3), (3, 3), (1, 1)] -> False
    :param votes: list of tuples containing the split list1
    :return: True if valid otherwise False
    """
    counts = [0] * 6
    if 5 > len(votes) > 10:
        return False
    for pair in votes:
        if len(pair) != 2:
            return False
        x, y = pair
        if not isinstance(x, int) or not isinstance(y, int):
            return False
        if 0 > x > 5 or 0 > y > 5:
            return False

        counts[x] += 1
        counts[y] += 1

    for i in range(1, 6):
        if counts[i] != 2:
            return False

    return True


def generate_pairings(list1, list2, current_pairing, pairings):
    # Base case: If list1 and list2 are empty, we found a valid pairing
    if not list1 and not list2:
        pairings.append(current_pairing)
        return

    # Recursive case
    for i, v in enumerate(list1):
        remaining1 = list1[:i] + list1[i + 1:]
        remaining2 = list2[1:]
        new_pairing = current_pairing + [(v, list2[0])]

        generate_pairings(remaining1, remaining2, new_pairing, pairings)

    return pairings


def pairing_totals(pairing):
    sums = reduce(lambda acc, pair: acc + [sum(pair)], pairing, [])
    return sums


if __name__ == "__main__":
    pub_votes = [('Jordan De Goey', 10), ('Nick Daicos', 6), ('Esava Ratugolea', 6), ('Scott Pendlebury', 4),
                 ('Jack Crisp', 2), ('Isaac Smith', 1), ('Josh Daicos', 1)]
    result = generate_possible_votes(pub_votes)
    print(result)
