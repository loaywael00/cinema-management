import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

# Initialize global variables
total = 0
combo_total = 0
snacks_total = 0


def load_movies():
    with open('movies.json', 'r', encoding='utf-8') as file:
        return json.load(file)


class CinemaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cinema Management System")
        self.root.geometry("1000x700")

        # Main frame
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Status bar
        self.status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self._build_main_menu()

    def _build_main_menu(self):
        """Build the welcome/role-selection screen inside main_frame."""
        tk.Label(
            self.main_frame,
            text="🎬 Cinema Management System",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        role_frame = tk.Frame(self.main_frame)
        role_frame.pack(pady=30)

        tk.Label(role_frame, text="Select Your Role:", font=("Arial", 14)).pack(pady=10)

        tk.Button(
            role_frame, text="👑 Admin",
            command=self.show_admin_panel,
            font=("Arial", 12), bg="#4CAF50", fg="white",
            padx=30, pady=15, width=15
        ).pack(side=tk.LEFT, padx=20)

        tk.Button(
            role_frame, text="👤 User",
            command=self.show_user_panel,
            font=("Arial", 12), bg="#2196F3", fg="white",
            padx=30, pady=15, width=15
        ).pack(side=tk.LEFT, padx=20)

    def clear_frame(self):
        """Clear all widgets from main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_admin_panel(self):
        self.clear_frame()
        self.create_back_button()

        tk.Label(self.main_frame, text="👑 Admin Panel", font=("Arial", 20, "bold")).pack(pady=20)

        options_frame = tk.Frame(self.main_frame)
        options_frame.pack(pady=30)

        admin_buttons = [
            ("📊 Sales Report", self.sales_report),
            ("🎭 Read Halls", self.read_halls),
            ("➕ Add Movie", self.add_movie),
            ("🔄 Movie Exchange", self.movie_exchange),
            ("🎪 Swap Halls", self.swap_halls),
            ("📋 View Movies", self.view_movies)
        ]

        for text, command in admin_buttons:
            tk.Button(
                options_frame, text=text, command=command,
                font=("Arial", 11), bg="#607D8B", fg="white",
                padx=20, pady=10, width=20
            ).pack(pady=8)

    def show_user_panel(self):
        self.clear_frame()
        self.create_back_button()

        tk.Label(self.main_frame, text="👤 User Panel", font=("Arial", 20, "bold")).pack(pady=20)

        options_frame = tk.Frame(self.main_frame)
        options_frame.pack(pady=30)

        user_buttons = [
            ("🔍 Search Movies", self.search_movies),
            ("📅 Schedule", self.schedule_show),
            ("🎫 Book Single Ticket", self.book_single_ticket),
            ("👨‍👩‍👧‍👦 Book Family Ticket", self.book_family_ticket),
            ("🍿 Book Snacks", self.book_snacks),
            ("🍔 Book Combo", self.book_combos),
            ("❌ Cancel Ticket", self.cancel_tickets),
            ("💰 Calculate Total", self.calculate_total)
        ]

        for text, command in user_buttons:
            tk.Button(
                options_frame, text=text, command=command,
                font=("Arial", 11), bg="#FF9800", fg="white",
                padx=20, pady=10, width=25
            ).pack(pady=8)

    def create_back_button(self):
        """Create back button to return to main menu."""
        tk.Button(
            self.main_frame, text="⬅ Back to Main Menu",
            command=self.show_main_menu,
            font=("Arial", 10), bg="#9E9E9E", fg="white"
        ).pack(anchor=tk.NW, padx=10, pady=10)

    def show_main_menu(self):
        """Return to the main menu without re-calling __init__ (avoids duplicate widgets)."""
        self.clear_frame()
        self._build_main_menu()

    def update_status(self, message):
        self.status_bar.config(text=message)

    # ── Admin Functions ──────────────────────────────────────────────────────

    def sales_report(self):
        self.clear_frame()
        self.create_back_button()

        tk.Label(self.main_frame, text="📊 Sales Report", font=("Arial", 18, "bold")).pack(pady=20)

        text_area = scrolledtext.ScrolledText(self.main_frame, width=80, height=25)
        text_area.pack(padx=20, pady=10)

        movies = load_movies()

        report = "Ticket Summary:\n" + "=" * 50 + "\n\n"
        total_revenue = 0

        for movie in movies["movies"]:
            s_revenue = movie["s-tickets"] * movie.get("price", 200)
            f_revenue = movie["f-tickets"] * int(movie.get("price", 200) * 0.8)
            movie_total = s_revenue + f_revenue
            total_revenue += movie_total

            report += f"🎬 {movie['title']}\n"
            report += f"   Single Tickets: {movie['s-tickets']} → Revenue: {s_revenue} LE\n"
            report += f"   Family Tickets: {movie['f-tickets']} → Revenue: {f_revenue} LE\n"
            report += f"   Total Movie Revenue: {movie_total} LE\n"
            report += "-" * 40 + "\n"

        report += f"\n📈 GRAND TOTAL REVENUE: {total_revenue} LE\n"
        text_area.insert(tk.INSERT, report)
        text_area.config(state=tk.DISABLED)

    def read_halls(self):
        """FIX: iterate data['halls'] not data; use 'seats' key not 'capacity'/'type'."""
        try:
            with open("halls.json", "r") as y:
                data = json.load(y)

            self.clear_frame()
            self.create_back_button()

            tk.Label(self.main_frame, text="🎭 Halls Information", font=("Arial", 18, "bold")).pack(pady=20)

            text_area = scrolledtext.ScrolledText(self.main_frame, width=80, height=20)
            text_area.pack(padx=20, pady=10)

            halls_info = "Cinema Halls:\n" + "=" * 40 + "\n\n"
            # FIX: was iterating 'data' (a dict), must iterate data["halls"]
            for hall in data["halls"]:
                halls_info += f"🎪 Hall ID: {hall['id']}\n"
                halls_info += f"   Name: {hall['name']}\n"
                # FIX: key is 'seats', not 'capacity'; 'type' does not exist
                halls_info += f"   Capacity: {hall['seats']} seats\n"
                halls_info += "-" * 40 + "\n"

            text_area.insert(tk.INSERT, halls_info)
            text_area.config(state=tk.DISABLED)
        except FileNotFoundError:
            messagebox.showerror("Error", "halls.json file not found!")

    def add_movie(self):
        self.clear_frame()
        self.create_back_button()

        tk.Label(self.main_frame, text="➕ Add New Movie", font=("Arial", 18, "bold")).pack(pady=20)

        form_frame = tk.Frame(self.main_frame)
        form_frame.pack(pady=20)

        entries = {}
        labels = [
            "Title", "Genre", "Duration (minutes)", "Rating",
            "Price", "Single Tickets", "Family Tickets",
            "Hall ID", "Hall Name", "Seats"
        ]

        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label + ":", font=("Arial", 10)).grid(
                row=i, column=0, sticky=tk.W, pady=5, padx=10)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5, padx=10)
            entries[label] = entry

        def submit_movie():
            try:
                with open("movies.json", "r") as file:
                    data = json.load(file)

                new_movie = {
                    "title": entries["Title"].get(),
                    "genre": entries["Genre"].get(),
                    "duration": int(entries["Duration (minutes)"].get()),
                    "rating": float(entries["Rating"].get()),
                    "price": int(entries["Price"].get()),
                    "s-tickets": int(entries["Single Tickets"].get()),
                    "f-tickets": int(entries["Family Tickets"].get()),
                    "id": int(entries["Hall ID"].get()),
                    "name": entries["Hall Name"].get(),
                    "seats": int(entries["Seats"].get())
                }

                data["movies"].append(new_movie)

                with open("movies.json", "w") as file:
                    json.dump(data, file, indent=2)

                messagebox.showinfo("Success", f"Movie '{new_movie['title']}' added successfully!")
                self.show_admin_panel()

            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values!")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

        tk.Button(
            self.main_frame, text="Submit Movie", command=submit_movie,
            font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=10
        ).pack(pady=20)

    def movie_exchange(self):
        self.xchange()

    def swap_halls(self):
        self.swap()

    def view_movies(self):
        self.clear_frame()
        self.create_back_button()

        tk.Label(self.main_frame, text="📋 Current Movies", font=("Arial", 18, "bold")).pack(pady=20)

        text_area = scrolledtext.ScrolledText(self.main_frame, width=90, height=25)
        text_area.pack(padx=20, pady=10)

        movies_info = "Current Movies List:\n" + "=" * 60 + "\n\n"
        movies = load_movies()

        for i, movie in enumerate(movies["movies"], 1):
            movies_info += f"{i}. 🎬 {movie['title']}\n"
            movies_info += f"   Genre: {movie['genre']}\n"
            movies_info += f"   Duration: {movie['duration']} mins | Rating: {movie['rating']}/10\n"
            movies_info += f"   Price: {movie['price']} LE | Seats: {movie['seats']}\n"
            movies_info += f"   Hall: {movie['name']} (ID: {movie['id']})\n"
            movies_info += f"   Tickets - Single: {movie['s-tickets']}, Family: {movie['f-tickets']}\n"
            movies_info += "-" * 60 + "\n"

        text_area.insert(tk.INSERT, movies_info)
        text_area.config(state=tk.DISABLED)

    # ── User Functions ───────────────────────────────────────────────────────

    def search_movies(self):
        self.clear_frame()
        self.create_back_button()

        tk.Label(self.main_frame, text="🔍 Search Movies", font=("Arial", 18, "bold")).pack(pady=20)

        search_frame = tk.Frame(self.main_frame)
        search_frame.pack(pady=20)

        tk.Label(search_frame, text="Search by:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)

        search_var = tk.StringVar(value="title")
        for i, (text, value) in enumerate([("Title", "title"), ("Genre", "genre"), ("Rating", "rating")]):
            tk.Radiobutton(search_frame, text=text, variable=search_var, value=value).grid(
                row=0, column=i + 1, padx=10)

        tk.Label(search_frame, text="Search Term:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        search_entry = tk.Entry(search_frame, width=30)
        search_entry.grid(row=1, column=1, columnspan=3, padx=10, pady=10)

        results_text = scrolledtext.ScrolledText(self.main_frame, width=80, height=20)
        results_text.pack(padx=20, pady=10)

        def perform_search():
            search_type = search_var.get()
            term = search_entry.get().lower()
            results_text.delete(1.0, tk.END)

            data = load_movies()
            movies = data["movies"]
            matching = []

            if search_type == "title":
                matching = [m for m in movies if term in m["title"].lower()]
            elif search_type == "genre":
                matching = [m for m in movies if term in m["genre"].lower()]
            elif search_type == "rating":
                try:
                    min_rating = float(term)
                    matching = [m for m in movies if m["rating"] >= min_rating]
                except ValueError:
                    results_text.insert(tk.INSERT, "Please enter a valid number for rating!")
                    return

            if matching:
                results_text.insert(tk.INSERT, f"Found {len(matching)} movie(s):\n\n")
                for i, movie in enumerate(matching, 1):
                    results_text.insert(tk.INSERT,
                        f"{i}. 🎬 {movie['title']}\n"
                        f"   Genre: {movie['genre']} | Duration: {movie['duration']} mins\n"
                        f"   Rating: {movie['rating']}/10 | Price: {movie['price']} LE\n"
                        f"   Available Seats: {movie['seats']}\n"
                        f"{'-' * 50}\n"
                    )
            else:
                results_text.insert(tk.INSERT, "No movies found matching your criteria.")

        tk.Button(
            self.main_frame, text="🔍 Search", command=perform_search,
            font=("Arial", 12), bg="#2196F3", fg="white", padx=20, pady=10
        ).pack(pady=10)

    def schedule_show(self):
        """FIX: schedule.json keys are 'movie', 'hall_id', 'time' — not 'date'/'hall'."""
        try:
            with open("schedule.json") as k:
                data = json.load(k)

            self.clear_frame()
            self.create_back_button()

            tk.Label(self.main_frame, text="📅 Movie Schedule", font=("Arial", 18, "bold")).pack(pady=20)

            text_area = scrolledtext.ScrolledText(self.main_frame, width=80, height=25)
            text_area.pack(padx=20, pady=10)

            schedule_info = "Movie Schedule:\n" + "=" * 50 + "\n\n"
            for entry in data["schedule"]:
                schedule_info += f"🎬 Movie: {entry['movie']}\n"
                # FIX: use 'time' and 'hall_id'; there is no separate 'date' or 'hall' key
                schedule_info += f"   Time: {entry['time']}\n"
                schedule_info += f"   Hall ID: {entry['hall_id']}\n"
                schedule_info += "-" * 40 + "\n"

            text_area.insert(tk.INSERT, schedule_info)
            text_area.config(state=tk.DISABLED)
        except FileNotFoundError:
            messagebox.showwarning("Info", "Schedule file not available at the moment.")

    def book_single_ticket(self):
        self._book_ticket("single")

    def book_family_ticket(self):
        self._book_ticket("family")

    def _book_ticket(self, ticket_type):
        self.clear_frame()
        self.create_back_button()

        title = "🎫 Book Single Ticket" if ticket_type == "single" else "👨‍👩‍👧‍👦 Book Family Ticket"
        tk.Label(self.main_frame, text=title, font=("Arial", 18, "bold")).pack(pady=20)

        movies_frame = tk.Frame(self.main_frame)
        movies_frame.pack(pady=20)

        tk.Label(movies_frame, text="Select Movie:", font=("Arial", 12)).pack()

        movie_listbox = tk.Listbox(movies_frame, width=50, height=6)
        movie_listbox.pack(pady=10)

        movies = load_movies()
        for movie in movies["movies"]:
            movie_listbox.insert(tk.END, f"{movie['title']} - {movie['seats']} seats available")

        tk.Label(self.main_frame, text="Number of Tickets:", font=("Arial", 12)).pack()
        quantity_spin = tk.Spinbox(self.main_frame, from_=1, to=10, width=10)
        quantity_spin.pack(pady=10)

        def book_ticket():
            selection = movie_listbox.curselection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a movie!")
                return

            try:
                movie_index = selection[0]
                quantity = int(quantity_spin.get())
                movie = movies["movies"][movie_index]

                if quantity > movie["seats"]:
                    messagebox.showerror("Error", f"Only {movie['seats']} seats available!")
                    return

                if ticket_type == "single":
                    movie["s-tickets"] += quantity
                    price = quantity * movie.get("price", 200)
                else:
                    movie["f-tickets"] += quantity
                    price = quantity * int(movie.get("price", 200) * 0.8)

                movie["seats"] -= quantity

                with open("movies.json", "w") as f:
                    json.dump(movies, f, indent=2)

                messagebox.showinfo("Success",
                    f"Booked {quantity} {ticket_type} ticket(s) for '{movie['title']}'\n"
                    f"Total: {price} LE")
                self.show_user_panel()

            except ValueError:
                messagebox.showerror("Error", "Please enter a valid number!")

        tk.Button(
            self.main_frame,
            text="Book Now" if ticket_type == "single" else "Book Family Tickets",
            command=book_ticket,
            font=("Arial", 12),
            bg="#4CAF50" if ticket_type == "single" else "#FF5722",
            fg="white", padx=20, pady=10
        ).pack(pady=20)

    def book_snacks(self):
        self._book_items("snacks")

    def book_combos(self):
        self._book_items("combos")

    def _book_items(self, item_type):
        self.clear_frame()
        self.create_back_button()

        title = "🍿 Book Snacks" if item_type == "snacks" else "🍔 Book Combos"
        tk.Label(self.main_frame, text=title, font=("Arial", 18, "bold")).pack(pady=20)

        items_frame = tk.Frame(self.main_frame)
        items_frame.pack(pady=20)

        if item_type == "snacks":
            items = [
                ("Popcorn Small", 80), ("Popcorn Large", 110), ("Nachos", 95),
                ("Fries", 50), ("Hot Dog", 85), ("Burger", 120),
                ("Pizza Slice", 90), ("Pepsi", 40), ("Red Bull", 90),
                ("Water", 25), ("Chocolate", 35), ("Ice Cream", 45)
            ]
        else:
            items = [
                ("Pepsi + Fries", 60), ("2x Popcorn", 170),
                ("Burger + Pepsi", 140), ("Pizza Slice + Pepsi", 120),
                ("Hot Dog + Fries", 120)
            ]

        cart = {}
        for name, price in items:
            frame = tk.Frame(items_frame)
            frame.pack(fill=tk.X, pady=5)
            tk.Label(frame, text=f"{name}: {price} LE", width=25, anchor=tk.W).pack(side=tk.LEFT)
            quantity_var = tk.StringVar(value="0")
            tk.Spinbox(frame, from_=0, to=10, textvariable=quantity_var, width=10).pack(side=tk.LEFT, padx=10)
            cart[name] = (price, quantity_var)

        def calculate_total():
            total = 0
            receipt = f"{'Item':<20} {'Qty':<5} {'Price':<10} {'Total':<10}\n"
            receipt += "=" * 50 + "\n"

            for name, (price, qty_var) in cart.items():
                qty = int(qty_var.get())
                if qty > 0:
                    item_total = price * qty
                    total += item_total
                    receipt += f"{name:<20} {qty:<5} {price:<10} {item_total:<10}\n"

            receipt += "=" * 50 + "\n"
            receipt += f"{'GRAND TOTAL:':<35} {total} LE\n"

            receipt_window = tk.Toplevel(self.root)
            receipt_window.title("Receipt")
            receipt_window.geometry("400x400")
            tk.Label(receipt_window, text="📋 RECEIPT", font=("Arial", 16, "bold")).pack(pady=10)
            receipt_text = scrolledtext.ScrolledText(receipt_window, width=50, height=20)
            receipt_text.pack(padx=10, pady=10)
            receipt_text.insert(tk.INSERT, receipt)
            receipt_text.config(state=tk.DISABLED)

            global snacks_total, combo_total
            if item_type == "snacks":
                snacks_total = total
            else:
                combo_total = total

        tk.Button(
            self.main_frame, text="Calculate Total & Show Receipt",
            command=calculate_total,
            font=("Arial", 12), bg="#FF9800", fg="white", padx=20, pady=10
        ).pack(pady=20)

    def cancel_tickets(self):
        self.clear_frame()
        self.create_back_button()

        tk.Label(self.main_frame, text="❌ Cancel Tickets", font=("Arial", 18, "bold")).pack(pady=20)

        movies = load_movies()

        cancel_frame = tk.Frame(self.main_frame)
        cancel_frame.pack(pady=20)

        tk.Label(cancel_frame, text="Select Movie:", font=("Arial", 12)).pack()
        movie_var = tk.StringVar()
        movie_dropdown = ttk.Combobox(cancel_frame, textvariable=movie_var, width=40, state="readonly")
        movie_dropdown['values'] = [movie['title'] for movie in movies["movies"]]
        movie_dropdown.pack(pady=10)

        tk.Label(cancel_frame, text="Single Tickets to Cancel:", font=("Arial", 12)).pack()
        single_spin = tk.Spinbox(cancel_frame, from_=0, to=50, width=10)
        single_spin.pack(pady=5)

        tk.Label(cancel_frame, text="Family Tickets to Cancel:", font=("Arial", 12)).pack()
        family_spin = tk.Spinbox(cancel_frame, from_=0, to=50, width=10)
        family_spin.pack(pady=5)

        def process_cancellation():
            selected_movie = movie_var.get()
            if not selected_movie:
                messagebox.showwarning("Warning", "Please select a movie!")
                return

            movie_index = next(
                (i for i, m in enumerate(movies["movies"]) if m["title"] == selected_movie), None)
            if movie_index is None:
                messagebox.showerror("Error", "Movie not found!")
                return

            movie = movies["movies"][movie_index]
            s_cancel = int(single_spin.get())
            f_cancel = int(family_spin.get())

            if s_cancel > movie["s-tickets"]:
                messagebox.showerror("Error",
                    f"Cannot cancel {s_cancel} single tickets. Only {movie['s-tickets']} available!")
                return
            if f_cancel > movie["f-tickets"]:
                messagebox.showerror("Error",
                    f"Cannot cancel {f_cancel} family tickets. Only {movie['f-tickets']} available!")
                return

            movie["s-tickets"] -= s_cancel
            movie["f-tickets"] -= f_cancel
            movie["seats"] += (s_cancel + f_cancel)

            with open("movies.json", "w") as f:
                json.dump(movies, f, indent=2)

            refund = (s_cancel * movie.get("price", 200)) + (f_cancel * int(movie.get("price", 200) * 0.8))
            messagebox.showinfo("Success",
                f"Cancellation Successful!\n"
                f"Refund Amount: {refund} LE\n"
                f"Single tickets cancelled: {s_cancel}\n"
                f"Family tickets cancelled: {f_cancel}")
            self.show_user_panel()

        tk.Button(
            self.main_frame, text="Cancel Tickets", command=process_cancellation,
            font=("Arial", 12), bg="#F44336", fg="white", padx=20, pady=10
        ).pack(pady=20)

    def calculate_total(self):
        global total, snacks_total, combo_total

        ticket_cost = 0
        movies = load_movies()
        for movie in movies["movies"]:
            ticket_cost += (movie["s-tickets"] * movie.get("price", 200)) + \
                           (movie["f-tickets"] * int(movie.get("price", 200) * 0.8))

        total = ticket_cost + snacks_total + combo_total

        summary = (
            f"💰 FINAL PRICE SUMMARY\n"
            f"{'=' * 30}\n"
            f"Movie Tickets: {ticket_cost} LE\n"
            f"Snacks: {snacks_total} LE\n"
            f"Combos: {combo_total} LE\n"
            f"{'=' * 30}\n"
            f"TOTAL: {total} LE\n"
            f"{'=' * 30}\n\n"
            f"Thank you for your purchase!"
        )
        messagebox.showinfo("Total Price", summary)

    def xchange(self):
        """Replace a movie at a chosen index (add_movie form reused)."""
        messagebox.showinfo("Info", "Movie exchange: fill in the form to replace a movie.")
        self.add_movie()

    def swap(self):
        """FIX: movies[3:] might be empty — guard against empty lists."""
        try:
            movies = load_movies()["movies"]
            if len(movies) < 4:
                messagebox.showwarning("Warning", "Need at least 4 movies to compare halls.")
                return

            first_three = movies[:3]
            next_two = movies[3:]

            min_first = min(first_three, key=lambda m: m["s-tickets"] + m["f-tickets"])
            max_next = max(next_two, key=lambda m: m["s-tickets"] + m["f-tickets"])

            min_total = min_first["s-tickets"] + min_first["f-tickets"]
            max_total = max_next["s-tickets"] + max_next["f-tickets"]

            if min_total < max_total:
                msg = (f"Recommended exchange:\n\n"
                       f"'{min_first['title']}' (low attendance: {min_total})\n"
                       f"  ↔  '{max_next['title']}' (high attendance: {max_total})")
            else:
                msg = "No exchange needed — current hall assignments are optimal."

            messagebox.showinfo("Hall Swap Analysis", msg)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


def main():
    root = tk.Tk()
    app = CinemaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
