import json  # FIX: was missing, needed by sales_report()


def book_snacks():
    items = [
        ("Popcorn Small", 80),
        ("Popcorn Large", 110),
        ("Nachos", 95),
        ("Fries", 50),
        ("Hot Dog", 85),
        ("Burger", 120),
        ("Pizza Slice", 90),
        ("Pepsi", 40),
        ("Red Bull", 90),
        ("Water", 25),
        ("Chocolate", 35),
        ("Ice Cream", 45)
    ]
    print("_Snacks List_")
    for i, (name, price) in enumerate(items, start=1):
        print(f"{i}. {name} – {price} LE")
    print("0. Finish and print receipt")

    cart = {}
    while True:
        pick = input("Enter item number (0 to finish): ").strip()
        if not pick.isdigit():
            print("Please enter a number.")
            continue
        pick = int(pick)
        if pick == 0:
            break
        if 1 <= pick <= len(items):
            name, price = items[pick - 1]
            qty_txt = input(f"Enter quantity for {name}: ").strip()
            if qty_txt.isdigit() and int(qty_txt) > 0:
                cart[name] = cart.get(name, 0) + int(qty_txt)
                print(f"Added {qty_txt} x {name}.")
            else:
                print("Quantity must be a positive number.")
        else:
            print("Out of range, please try again.")

    print("\n_Receipt_")
    if not cart:
        print("No items selected.\nTotal: 0 LE")
        return 0

    total = 0
    for name, price in items:
        if name in cart:
            qty = cart[name]
            line = price * qty
            total += line
            print(f"- {name}: {qty} x {price} = {line} LE")
    print(f"\nTotal: {total} LE")
    return total


def book_combos():
    combos = [
        ("Pepsi + Fries",        60,  90),
        ("2x Popcorn",          170, 200),
        ("Burger + Pepsi",      140, 160),
        ("Pizza Slice + Pepsi", 120, 130),
        ("Hot Dog + Fries",     120, 135),
    ]
    print("_Cinema Combos Menu_")
    for i, (name, disc, norm) in enumerate(combos, start=1):
        print(f"{i}. {name} – {disc} LE (instead of {norm} LE)")
    print("0. Finish and print receipt")

    cart = {}
    while True:
        pick = input("Enter combo number (0 to finish): ").strip()
        if not pick.isdigit():
            print("Please enter a number.")
            continue
        pick = int(pick)
        if pick == 0:
            break
        if 1 <= pick <= len(combos):
            name, disc, norm = combos[pick - 1]
            qty_txt = input(f"Enter quantity for {name}: ").strip()
            if qty_txt.isdigit() and int(qty_txt) > 0:
                cart[name] = cart.get(name, 0) + int(qty_txt)
                print(f"Added {qty_txt} x {name}.")
            else:
                print("Quantity must be a positive number.")
        else:
            print("Out of range, please try again.")

    print("\n_Receipt_")
    if not cart:
        print("No items selected.\nTotal: 0 LE")
        return 0

    total = 0
    for name, disc, norm in combos:
        if name in cart:
            qty = cart[name]
            line = disc * qty
            total += line
            print(f"- {name}: {qty} x {disc} = {line} LE")
    print(f"\nTotal: {total} LE")
    return total


def sales_report():
    """FIX: added missing 'import json' at top; removed erroneous module-level calls."""
    print("\nTicket Summary:\n")
    with open('movies.json', 'r', encoding='utf-8') as file:
        movies = json.load(file)
    for movie in movies["movies"]:
        print(movie["title"])
        print("  s-tickets:", movie["s-tickets"])
        print("  f-tickets:", movie["f-tickets"])
        print("  -")


def swap():
    with open("movies.json", "r", encoding="utf-8") as file:
        movies = json.load(file)["movies"]

    if len(movies) < 4:
        print("Not enough movies to compare halls.")
        return

    first_three = movies[:3]
    next_two = movies[3:5]

    min_first = min(first_three, key=lambda m: m["s-tickets"] + m["f-tickets"])
    min_first_total = min_first["s-tickets"] + min_first["f-tickets"]

    max_next = max(next_two, key=lambda m: m["s-tickets"] + m["f-tickets"])
    max_next_total = max_next["s-tickets"] + max_next["f-tickets"]

    print(f"Low hall: {min_first['title']} | s={min_first['s-tickets']} f={min_first['f-tickets']} total={min_first_total}")
    print(f"High hall: {max_next['title']} | s={max_next['s-tickets']} f={max_next['f-tickets']} total={max_next_total}")

    if min_first_total < max_next_total:
        print("Recommendation: exchange these films.")
    else:
        print("No exchange needed.")


def assign_halls():
    with open("movies.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    index = int(input("Enter movie number to replace (1 to 5): ")) - 1
    print("Enter new movie details:")
    new_movie = {
        "title":    input("Title: "),
        "genre":    input("Genre: "),
        "duration": int(input("Duration (minutes): ")),
        "rating":   float(input("Rating: ")),
        "price":    int(input("Price: ")),
        "s-tickets": int(input("Single Tickets: ")),
        "f-tickets": int(input("Family Tickets: ")),
        "id":       int(input("Hall ID: ")),
        "name":     input("Hall Name: "),
        "seats":    int(input("Seats: "))
    }
    data["movies"][index] = new_movie
    with open("movies.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
    print("Movie replaced successfully!")


# FIX: removed module-level calls to book_snacks(), book_combos(), sales_report(), swap()
# They were running automatically on import. Call them explicitly when needed.
