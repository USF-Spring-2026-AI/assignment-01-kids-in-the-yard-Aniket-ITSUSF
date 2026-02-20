import os
from person_factory import PersonFactory
from family_tree import FamilyTree


def main() -> None:
    # get the directory where the data csv files are
    data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Data directory: {data_dir}")
    
    print("Loading CSV data ...")
    factory = PersonFactory(data_dir)
    

    print("Generating family tree (starting from 1950) ...")
    tree = FamilyTree(factory)
    tree.generate()
    print(f"Done!  {tree.total_people()} people generated.\n")

    menu = (
        "========================================\n"
        "  Family Tree Query Menu\n"
        "========================================\n"
        "  1 — Total number of people\n"
        "  2 — People count by decade\n"
        "  3 — Duplicate names\n"
        "  4 — Exit\n"
        "========================================\n"
    )

    # loop to keep asking for choice until exit
    while True:
        print(menu)
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            print(f"\nTotal people in the tree: {tree.total_people()}\n")

        elif choice == "2":
            print("\nPeople by birth decade:")
            print("-" * 30)
            for decade, count in tree.people_by_decade().items():
                print(f"  {decade}: {count}")
            print()

        elif choice == "3":
            dupes = tree.duplicate_names()
            if dupes:
                print("\nDuplicate names:")
                print("-" * 30)
                for name, count in dupes.items():
                    print(f"  {name}: {count} occurrences")
            else:
                print("\nNo duplicate names found.")
            print()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2, 3, or 4.\n")


# start point
if __name__ == "__main__":
    main()
