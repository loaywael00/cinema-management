import json

# Load movies at module level (read-only, safe to import)
with open("movies.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    movies = data["movies"]


def read_movies():
    with open("movies.json") as file:
        mv = json.load(file)
        for movie in mv["movies"]:
            print(movie["title"])


def read_halls():
    with open("halls.json") as file:
        halls = json.load(file)
        for hall in halls["halls"]:
            print(hall["name"])


def search_movie():
    """Search movies by title, genre, or minimum rating."""
    print("\nChoose search method:")
    print("1. By title")
    print("2. By genre")
    print("3. By rating (minimum)")

    choice = input("Enter choice (1/2/3): ").strip()
    matching = []

    if choice == "1":
        keyword = input("Enter movie title or part of it: ").lower()
        matching = [m for m in movies if keyword in m["title"].lower()]

    elif choice == "2":
        genre = input("Enter genre: ").lower()
        matching = [m for m in movies if genre in m["genre"].lower()]

    elif choice == "3":
        try:
            rating = float(input("Enter minimum rating: "))
            matching = [m for m in movies if m["rating"] >= rating]
        except ValueError:
            print("Rating must be a number.")
            return None
    else:
        print("Invalid choice.")
        return None

    if matching:
        print(f"\nMatching movies ({len(matching)} found):")
        for i, movie in enumerate(matching, start=1):
            print(
                f"{i}. {movie['title']} | Genre: {movie['genre']} | "
                f"Duration: {movie['duration']} min | Rating: {movie['rating']}"
            )
    else:
        print("No movies matched your search.")

    return matching
