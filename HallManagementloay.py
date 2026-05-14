import json

# FIX: removed 'from run import *' — that caused a circular import
#      (run.py imports this file, so this file must NOT import run.py)

with open("halls.json") as file:
    halls = json.load(file)

with open("movies.json") as file:
    movies = json.load(file)

# Build movie list for display
m = []
for c, i in enumerate(movies["movies"]):
    m.append(f"{c + 1}_{i['title']}")


def book_single_ticket():
    """Ask the user to pick a movie and number of tickets. Returns (movie_entry, ticket_num)."""
    print("Movies:", m)
    movie_num = input("Please choose the number of the movie: ")

    # FIX: validate digit BEFORE comparing to len(m)
    while not movie_num.isdigit():
        movie_num = input("Wrong input, please enter a number: ")
    while int(movie_num) < 1 or int(movie_num) > len(m):
        movie_num = input("Wrong, please choose from the list: ")
        while not movie_num.isdigit():
            movie_num = input("Wrong input, please enter a number: ")

    # FIX: was m[int(movie_num)] — off-by-one; correct is m[int(movie_num) - 1]
    f_chosen_movie = m[int(movie_num) - 1]

    ticket_num = input("How many tickets do you want: ")
    while not ticket_num.isdigit():
        ticket_num = input("Wrong input, please enter a number: ")

    return f_chosen_movie, int(ticket_num)


def book_family_ticket():
    """Book a family ticket (kids + optional kids area)."""
    kid_num = input("How many kids do you have? ")
    while not kid_num.isdigit():
        kid_num = input("Wrong, please enter a number: ")

    kids_area = input("Do you want to reserve a kids area for them? (y/n): ").lower()
    while kids_area not in ["y", "n"]:
        kids_area = input("Wrong, please choose (y/n): ").lower()

    if kids_area == "y":
        kids = f"Number of kids tickets in kids area: {kid_num}"
    else:
        kids = "No kids area reserved."

    return int(kid_num), kids


def cancel_tickets():
    """Cancel single and/or family tickets for a chosen movie."""
    titles = [m_entry.get("title", "Untitled") for m_entry in movies["movies"]]
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

    mv = movies["movies"][movie_index]
    s_now = int(mv.get("s-tickets", 0))
    f_now = int(mv.get("f-tickets", 0))
    seats_available = 80 - (s_now + f_now)
    if seats_available < 0:
        seats_available = 0

    print(f"Current s-tickets: {s_now}, f-tickets: {f_now}, seats available: {seats_available}")

    while True:
        s_txt = input("How many single tickets do you want to cancel? ").strip()
        if s_txt.isdigit():
            s_cancel = int(s_txt)
            if s_cancel <= s_now:
                break
            print(f"You cannot cancel more than current s-tickets ({s_now}). Try again.")
        else:
            print("Please enter a non-negative integer.")

    while True:
        f_txt = input("How many family tickets do you want to cancel? ").strip()
        if f_txt.isdigit():
            f_cancel = int(f_txt)
            if f_cancel <= f_now:
                break
            print(f"You cannot cancel more than current f-tickets ({f_now}). Try again.")
        else:
            print("Please enter a non-negative integer.")

    s_new = s_now - s_cancel
    f_new = f_now - f_cancel
    seats_new = max(0, 80 - (s_new + f_new))

    mv["s-tickets"] = s_new
    mv["f-tickets"] = f_new
    mv["seats"] = seats_new

    with open("movies.json", "w", encoding="utf-8") as file:
        json.dump(movies, file, ensure_ascii=False, indent=2)

    print(
        f"Updated '{mv.get('title', '')}': "
        f"s-tickets={s_new} (cancelled {s_cancel}), "
        f"f-tickets={f_new} (cancelled {f_cancel}), "
        f"seats available={seats_new} [capacity=80]"
    )


def calculate_price(f_chosen_movie, ticket_num, kid_num, combo_total=0, snacks_total=0):
    """
    FIX: was using undefined globals combo_total/snacks_total/ticket_num/kid_num.
         Now accepts them as parameters.
    """
    cost = 0
    # Strip the leading "N_" prefix from f_chosen_movie if present
    if "_" in f_chosen_movie and f_chosen_movie.split("_", 1)[0].isdigit():
        chosen_title = f_chosen_movie.split("_", 1)[1].strip().lower()
    else:
        chosen_title = f_chosen_movie.strip().lower()

    for movie in movies["movies"]:
        if movie["title"].lower() == chosen_title:
            cost = movie['price'] * (ticket_num + 0.5 * kid_num) + combo_total + snacks_total
            break

    print(f"The final price is {cost} LE")
    return cost


def replace_movie():
    """Replace a movie in movies.json (previously misplaced inside Calculate_Price)."""
    with open("movies.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    index = int(input("Enter movie number to replace (1 to 5): ")) - 1
    print("Enter new movie details:")
    new_movie = {
        "title":     input("Title: "),
        "genre":     input("Genre: "),
        "duration":  int(input("Duration (minutes): ")),
        "rating":    float(input("Rating: ")),
        "price":     int(input("Price: ")),
        "s-tickets": int(input("Single Tickets: ")),
        "f-tickets": int(input("Family Tickets: ")),
        "id":        int(input("Hall ID: ")),
        "name":      input("Hall Name: "),
        "seats":     int(input("Seats: "))
    }
    data["movies"][index] = new_movie
    with open("movies.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print("Movie replaced successfully!")
