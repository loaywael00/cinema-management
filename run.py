import json

# FIX: removed circular imports.
#      run.py imported HallManagementloay which imported run.py → crash.
#      Instead, import functions directly from the fixed modules.
from HallManagementloay import book_single_ticket, book_family_ticket
from Ticketingseif import book_combos, book_snacks

user_name = input("Please enter your name: ")
print(f"Welcome, {user_name}!")

# FIX: admin_choise was used before assignment → initialise it first
admin_choise = input("Are you admin or user? (1=Admin / 2=User): ")

# FIX: 'while not admin_choise.isdigit()' loop was missing; added proper validation
while not admin_choise.isdigit() or int(admin_choise) not in [1, 2]:
    admin_choise = input("Wrong input, please choose (1/2): ")

admin_choise = int(admin_choise)

if admin_choise == 1:
    # Admin branch — extend as needed
    print("Admin panel selected. (Add admin features here.)")

elif admin_choise == 2:
    user_choice = input("Do you want a family or single ticket? (1=Single / 2=Family): ")
    while not user_choice.isdigit() or int(user_choice) not in [1, 2]:
        user_choice = input("Wrong input, please choose (1/2): ")
    user_choice = int(user_choice)

    if user_choice == 1:
        f_chosen_movie, ticket_num = book_single_ticket()
        kid_num = 0
    else:
        kid_num, kids = book_family_ticket()
        f_chosen_movie, ticket_num = None, 0

    # FIX: 'while combo != "y" or combo != "n"' is ALWAYS True (logical error).
    #      Correct condition is 'not in ["y", "n"]'.
    combo = input("Do you want a combo? (y/n): ").lower()
    while combo not in ["y", "n"]:
        combo = input("Please choose (y/n): ").lower()

    combo_total = 0
    if combo == "y":
        combo_total = book_combos()

    # FIX: same 'or' bug for snacks; also was reassigning 'combo' instead of 'snacks'
    snacks = input("Do you want snacks? (y/n): ").lower()
    while snacks not in ["y", "n"]:
        snacks = input("Please choose (y/n): ").lower()

    snacks_total = 0
    if snacks == "y":
        snacks_total = book_snacks()

    print(f"\nSummary for {user_name}:")
    print(f"  Combo total : {combo_total} LE")
    print(f"  Snacks total: {snacks_total} LE")
    print(f"  Grand total : {combo_total + snacks_total} LE")
