import math
import random
from collections import Counter

from person import Person
from person_factory import PersonFactory


class FamilyTree:
    MAX_YEAR = 2120

    def __init__(self, factory: PersonFactory) -> None:
        self._factory = factory
        self.all_people: list[Person] = []

    def generate(self) -> None:
        # start with 2 founders in 1950 and keep making kids
        founder_last_name = self._factory.pick_last_name(
            PersonFactory.get_decade_str(1950)
        )

        founder_a = self._factory.create_person(
            year_born=1950,
            last_name=founder_last_name,
            is_direct_descendant=True,
        )
        founder_b = self._factory.create_person(
            year_born=1950,
            last_name=founder_last_name,
            is_direct_descendant=True,
        )
        founder_a.partner = founder_b
        founder_b.partner = founder_a

        self.all_people.extend([founder_a, founder_b])

        current_generation: list[Person] = [founder_a]

        # go through generations until we hit the year limit
        while current_generation:
            next_generation: list[Person] = []
            for person in current_generation:
                children = self._generate_children(person)
                next_generation.extend(children)
            current_generation = next_generation

    def _generate_children(self, person: Person) -> list[Person]:
        # figure out how many kids they get and make them
        decade = PersonFactory.get_decade_str(person.year_born)

        # check if they need a partner
        has_partner = person.partner is not None
        if not has_partner:
            marriage_rate = self._factory.get_marriage_rate(decade)
            if random.random() < marriage_rate:
                partner = self._factory.create_partner(person)
                self.all_people.append(partner)
                has_partner = True

        base_rate = self._factory.get_birth_rate(decade)
        offset = random.uniform(-1.5, 1.5)
        num_children = max(0, round(base_rate + offset))

        # grad student requirement: 1 less kid if no spouse
        if not has_partner:
            num_children = max(0, num_children - 1)

        if num_children == 0:
            return []

        if person.partner is not None:
            elder_birth = min(person.year_born, person.partner.year_born)
        else:
            elder_birth = person.year_born

        start_year = elder_birth + 25
        end_year = elder_birth + 45

        if num_children == 1:
            birth_years = [(start_year + end_year) // 2]
        else:
            step = (end_year - start_year) / (num_children - 1)
            birth_years = [
                round(start_year + i * step) for i in range(num_children)
            ]

        children: list[Person] = []
        for by in birth_years:
            if by > self.MAX_YEAR:
                continue

            child = self._factory.create_person(
                year_born=by,
                last_name=person.last_name if person.is_direct_descendant
                else None,
                is_direct_descendant=person.is_direct_descendant,
            )
            children.append(child)
            person.children.append(child)
            if person.partner is not None:
                person.partner.children.append(child)
            self.all_people.append(child)

        return children

    def total_people(self) -> int:
        # simply get the length of the list
        return len(self.all_people)

    def people_by_decade(self) -> dict[str, int]:
        # count how many people were born each decade
        counter: Counter[str] = Counter()
        for person in self.all_people:
            decade = PersonFactory.get_decade_str(person.year_born)
            counter[decade] += 1
        return dict(sorted(counter.items()))

    def duplicate_names(self) -> dict[str, int]:
        # spot check for names that appeared more than once
        name_counts: Counter[str] = Counter(
            person.full_name for person in self.all_people
        )
        return {
            name: count
            for name, count in sorted(name_counts.items())
            if count > 1
        }
