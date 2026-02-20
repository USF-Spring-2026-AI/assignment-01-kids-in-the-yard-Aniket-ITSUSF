import csv
import math
import os
import random
from person import Person


class PersonFactory:
    # loads csv data on init
    def __init__(self, data_dir: str = ".") -> None:
        self._data_dir = data_dir
        self._life_expectancy = self._load_life_expectancy()
        self._first_names = self._load_first_names()
        self._gender_prob = self._load_gender_probability()
        self._birth_marriage = self._load_birth_marriage_rates()
        self._last_names, self._rank_probs = self._load_last_names()

    # join folder path with filename
    def _csv_path(self, filename: str) -> str:
        return os.path.join(self._data_dir, filename)

    # get life expectancy by year
    def _load_life_expectancy(self) -> dict[int, float]:
        table: dict[int, float] = {}
        with open(self._csv_path("life_expectancy.csv"), newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                year = int(row["Year"])
                expectancy = float(row["Period life expectancy at birth"])
                table[year] = expectancy
        return table

    # get first names
    def _load_first_names(
        self,
    ) -> dict[str, dict[str, list[tuple[str, float]]]]:
        table: dict[str, dict[str, list[tuple[str, float]]]] = {}
        with open(self._csv_path("first_names.csv"), newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                decade = row["decade"]
                gender = row["gender"]
                name = row["name"]
                freq = float(row["frequency"])
                table.setdefault(decade, {}).setdefault(gender, []).append(
                    (name, freq)
                )
        return table

    # get gender probabilities
    def _load_gender_probability(self) -> dict[str, dict[str, float]]:
        table: dict[str, dict[str, float]] = {}
        with open(
            self._csv_path("gender_name_probability.csv"), newline=""
        ) as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                decade = row["decade"]
                gender = row["gender"]
                prob = float(row["probability"])
                table.setdefault(decade, {})[gender] = prob
        return table

    # get birth and marriage rates
    def _load_birth_marriage_rates(
        self,
    ) -> dict[str, dict[str, float]]:
        table: dict[str, dict[str, float]] = {}
        with open(
            self._csv_path("birth_and_marriage_rates.csv"), newline=""
        ) as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                decade = row["decade"]
                table[decade] = {
                    "birth_rate": float(row["birth_rate"]),
                    "marriage_rate": float(row["marriage_rate"]),
                }
        return table

    # get last names and probabilities for ranks
    def _load_last_names(
        self,
    ) -> tuple[dict[str, list[str]], list[float]]:
        names_by_decade: dict[str, list[str]] = {}
        with open(self._csv_path("last_names.csv"), newline="") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                decade = row["Decade"]
                names_by_decade.setdefault(decade, []).append(
                    row["LastName"]
                )

        with open(
            self._csv_path("rank_to_probability.csv"), newline=""
        ) as fh:
            line = fh.readline().strip()
            rank_probs = [float(p) for p in line.split(",")]

        return names_by_decade, rank_probs

    @staticmethod
    def get_decade_str(year: int) -> str:
        # just returns the decade from the year like 1950s
        return f"{(year // 10) * 10}s"

    def _pick_gender(self, decade_str: str) -> str:
        # random choose male or female based on prob
        probs = self._gender_prob.get(decade_str, {"male": 0.5, "female": 0.5})
        genders = list(probs.keys())
        weights = list(probs.values())
        return random.choices(genders, weights=weights, k=1)[0]

    def _pick_first_name(self, decade_str: str, gender: str) -> str:
        # picks a random first name by freq
        name_list = self._first_names.get(decade_str, {}).get(gender, [])
        if not name_list:
            return "Unknown"
        names, freqs = zip(*name_list)
        return random.choices(names, weights=freqs, k=1)[0]

    def _pick_last_name(self, decade_str: str) -> str:
        # pick a random last name weighted by its rank
        names = self._last_names.get(decade_str)
        if not names:
            return "Doe"
        weights = self._rank_probs[: len(names)]
        return random.choices(names, weights=weights, k=1)[0]

    def _calc_year_died(self, year_born: int) -> int:
        # figure out when they died based on birth year + expectancy +/- 10 years
        expectancy = self._life_expectancy.get(year_born)
        if expectancy is None:
            closest = min(
                self._life_expectancy.keys(),
                key=lambda y: abs(y - year_born),
            )
            expectancy = self._life_expectancy[closest]
        offset = random.randint(-10, 10)
        return year_born + int(expectancy) + offset

    def create_person(
        self,
        year_born: int,
        last_name: str | None = None,
        is_direct_descendant: bool = False,
    ) -> Person:
        # creates a person and figures out all their stats
        decade = self.get_decade_str(year_born)
        gender = self._pick_gender(decade)
        first_name = self._pick_first_name(decade, gender)

        if last_name is None:
            last_name = self._pick_last_name(decade)

        year_died = self._calc_year_died(year_born)

        return Person(
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            year_born=year_born,
            year_died=year_died,
            is_direct_descendant=is_direct_descendant,
        )

    def create_partner(self, person: Person) -> Person:
        # creates a partner born around the same time
        partner_birth = person.year_born + random.randint(-10, 10)
        partner = self.create_person(
            year_born=partner_birth,
            last_name=None,
            is_direct_descendant=False,
        )
        person.partner = partner
        partner.partner = person
        return partner

    def get_marriage_rate(self, decade_str: str) -> float:
        # gets the marriage chance
        rates = self._birth_marriage.get(decade_str)
        if rates is None:
            return 0.0
        return rates["marriage_rate"]

    def get_birth_rate(self, decade_str: str) -> float:
        # gets how many kids they have on avg
        rates = self._birth_marriage.get(decade_str)
        if rates is None:
            return 0.0
        return rates["birth_rate"]
