import json

DEFAULT_CAPACITY = 80  # used if movie['capacity'] is missing


def add_single_tickets():
    """Add single tickets to a chosen movie and update movies.json."""
    with open("movies.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    titles = [m.get("title", "Untitled") for m in data["movies"]]
    print("Movies:")
    for i, t in enumerate(titles, start=1):
        print(f"{i}. {t}")

    movie_index = -1
    while True:
        choice = input(f"Choose movie number (1..{len(titles)}): ").strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(titles):
                movie_index = num - 1
                break
        print("Please enter a valid number from the list.")

    while True:
        s = input("How many SINGLE tickets do you want to add? ").strip()
        if s.isdigit():
            add_count = int(s)
            break
        print("Please enter a non-negative integer (e.g., 0, 1, 2, ...).")

    movie = data["movies"][movie_index]
    s_now = int(movie.get("s-tickets", 0))
    f_now = int(movie.get("f-tickets", 0))
    capacity = int(movie.get("capacity", DEFAULT_CAPACITY))

    s_new = s_now + add_count
    seats_new = max(0, capacity - (s_new + f_now))

    movie["s-tickets"] = s_new
    movie["seats"] = seats_new

    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(
        f"Updated '{movie.get('title', '')}': "
        f"s-tickets={s_new} (+{add_count}), "
        f"f-tickets={f_now}, "
        f"seats available={seats_new} [capacity={capacity}]"
    )
    return s_new


def add_family_tickets():
    """Add family tickets to a chosen movie and update movies.json."""
    with open("movies.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    titles = [m.get("title", "Untitled") for m in data["movies"]]
    print("Movies:")
    for i, t in enumerate(titles, start=1):
        print(f"{i}. {t}")

    movie_index = -1
    while True:
        choice = input(f"Choose movie number (1..{len(titles)}): ").strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(titles):
                movie_index = num - 1
                break
        print("Please enter a valid number from the list.")

    while True:
        s = input("How many FAMILY tickets do you want to add? ").strip()
        if s.isdigit():
            add_count = int(s)
            break
        print("Please enter a non-negative integer (e.g., 0, 1, 2, ...).")

    movie = data["movies"][movie_index]
    s_now = int(movie.get("s-tickets", 0))
    f_now = int(movie.get("f-tickets", 0))
    capacity = int(movie.get("capacity", DEFAULT_CAPACITY))

    f_new = f_now + add_count
    seats_new = max(0, capacity - (s_now + f_new))

    movie["f-tickets"] = f_new
    movie["seats"] = seats_new

    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(
        f"Updated '{movie.get('title', '')}': "
        f"s-tickets={s_now}, "
        f"f-tickets={f_new} (+{add_count}), "
        f"seats available={seats_new} [capacity={capacity}]"
    )
    return f_new


# FIX: removed module-level call add_single_tickets()
# Call explicitly when running as a script:
if __name__ == "__main__":
    print("1. Add single tickets\n2. Add family tickets")
    choice = input("Choose (1/2): ").strip()
    if choice == "1":
        add_single_tickets()
    elif choice == "2":
        add_family_tickets()
    else:
        print("Invalid choice.")
