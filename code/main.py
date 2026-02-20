import os
from person_factory import PersonFactory
from family_tree import FamilyTree


def main() -> None:
    # get the directory where the data csv files are
    data_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"Data directory: {data_dir}")

    try:
        print("Loading CSV data ...")
        factory = PersonFactory(data_dir)
    except FileNotFoundError as e:
        print(f"Startup failed — a required data file is missing: {e}")
        return
    except Exception as e:
        print(f"Startup failed while loading data: {e}")
        return

    try:
        print("Generating family tree (starting from 1950) ...")
        tree = FamilyTree(factory)
        tree.generate()
        print(f"Done!  {tree.total_people()} people generated.\n")
    except Exception as e:
        print(f"Failed to generate family tree: {e}")
        return

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
        try:
            print(menu)
            choice = input("Enter your choice (1-4): ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

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
