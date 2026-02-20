class Person:
    # initialize a person object with basic info
    def __init__(
        self,
        first_name: str,
        last_name: str,
        gender: str,
        year_born: int,
        year_died: int,
        is_direct_descendant: bool = False,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.year_born = year_born
        self.year_died = year_died
        self.is_direct_descendant = is_direct_descendant
        # set partner and children to empty at first
        self.partner: "Person | None" = None
        self.children: list["Person"] = []

    @property
    def full_name(self) -> str:
        # just combine first and last name
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        # print out the person's info nicely
        partner_info = (
            self.partner.full_name if self.partner else "None"
        )
        return (
            f"{self.full_name} | {self.gender} | "
            f"born {self.year_born} | died {self.year_died} | "
            f"partner: {partner_info} | "
            f"children: {len(self.children)}"
        )
