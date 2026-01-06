# Welcome to UMD Food Recommender!
# This project is put together for credit in INST311 and INST326 at the University of Maryland, College Park.
# To run program do "python Final_Project/main.py" or "python Final_Project/main.py --skip-login"

from dining_hall_menus.sample_foods_251_north_breakfast import sample_foods_251_north_breakfast
from dining_hall_menus.sample_foods_251_north_lunch import sample_foods_251_north_lunch
from dining_hall_menus.sample_foods_251_north_dinner import sample_foods_251_north_dinner
from dining_hall_menus.sample_foods_south_breakfast import sample_foods_south_breakfast
from dining_hall_menus.sample_foods_south_lunch import sample_foods_south_lunch
from dining_hall_menus.sample_foods_south_dinner import sample_foods_south_dinner
from dining_hall_menus.sample_foods_the_y_breakfast import sample_foods_the_y_breakfast
from dining_hall_menus.sample_foods_the_y_lunch import sample_foods_the_y_lunch
from dining_hall_menus.sample_foods_the_y_dinner import sample_foods_the_y_dinner

from items.user import User
from items.review import Review
import argparse
import re

# A collection of all foods from the dining_hall_menus folder
ALL_FOODS = (
    sample_foods_251_north_breakfast + sample_foods_251_north_lunch + sample_foods_251_north_dinner +
    sample_foods_south_breakfast + sample_foods_south_lunch + sample_foods_south_dinner +
    sample_foods_the_y_breakfast + sample_foods_the_y_lunch + sample_foods_the_y_dinner
)

# All foods by name stored in FOOD_BY_NAME
FOOD_BY_NAME = {}
for food in ALL_FOODS:
    FOOD_BY_NAME[food.name] = food

REVIEWS = [] # Stores reviews

# Helper function: Sorts highest rating first and take top n
def top_n_by_rating(food_list, n=10):
    return sorted(food_list, key=lambda food: food.average_rating, reverse=True)[:n]

# Helper function: prints food reviews
def print_reviews_for_food(food_name):
    found = False
    for r in REVIEWS:
        if r.food_name == food_name:
            print(r)
            found = True
    if not found:
        print("No reviews yet.")

'''Remove Temp Tag''''''Write a test case maybe'''
# Helper function: Uses Regular Expressions to guide user inputs
def normalize_choice(user_text):
    """Extracts the first number from the input (if any) and returns it.
    Otherwise returns the cleaned lowercase text.
    Examples:
      "1" -> "1"
      "1)" -> "1"
      "Option 2" -> "2"
      "Breakfast" -> "breakfast"
    """
    text = user_text.strip().lower()
    match = re.search(r"\d+", text)
    if match:
        return match.group()
    return text

# This is the menu aspect, referencing an applications Global Navigation
def globalNav(skip_login=False):
    logged_in = False
    current_user = None

    # Login prompt
    if not skip_login:
        initial_input = input("Would you like to login? (yes/no) ").strip().lower()
    else:
        initial_input = "no"

    if initial_input == "yes":
        username_input = input("User Terpmail: ").strip()

        if username_input.endswith("@terpmail.umd.edu"): # only allows terpmail accounts
            password_input = input("User Password: ").strip()

            if password_input == "GoTerps!": # for temporary reasons, the only recognized password is GoTerps!
                logged_in = True # If True, unlocks bookmark, comment, and like/dislike functionality
                current_user = User(username_input)
                print("Login successful!")
            else:
                print("Invalid password")
        else:
            print("Invalid email: must be a Terpmail address")
    
    # Global Navigation Menu
    while True:
        globalNav_input = normalize_choice(input("\n\nWhat would you like to do?\n" \
                                "1. Overall Ranking\n" \
                                "2. What's on the Menu?\n" \
                                "3. Individual Rankings\n" \
                                "4. Bookmarks\n" \
                                "5. quit\n\n").strip().lower()) #terminates program
        
        # Switch Statement
        # 1. Overall Ranking
        if (globalNav_input == "1") or (globalNav_input == "overall ranking"):
            
            print("Navigating to the Overall Ranking")
            user_input = normalize_choice(input("What Meal Time would you like to see?\n" \
                                "1. Breakfast\n" \
                                "2. Lunch\n" \
                                "3. Dinner\n\n").strip().lower())
            
            if (user_input == "1") or (user_input == "breakfast"):
                combined = (sample_foods_south_breakfast + sample_foods_251_north_breakfast + sample_foods_the_y_breakfast)
                title = "Overall Breakfast Top 10"
            elif (user_input == "2") or (user_input == "lunch"):
                combined = (sample_foods_south_lunch + sample_foods_251_north_lunch + sample_foods_the_y_lunch)
                title = "Overall Lunch Top 10"
            elif (user_input == "3") or (user_input == "dinner"):
                combined = (sample_foods_south_dinner + sample_foods_251_north_dinner + sample_foods_the_y_dinner)
                title = "Overall Dinner Top 10"
            else:
                print("Invalid meal time selection.")
                continue
            
            # Get the top 10
            top10 = top_n_by_rating(combined, 10)

            # print results
            print(f"\n{title}")
            print("-" * len(title))

            count = 1
            for food in top10:
                print(f"{count}. {food.name} | {food.dining_hall} | Rating: {food.average_rating} | {food.dietary_restrictions}")
                count += 1
            
        # 2. What's on the Menu?
        elif (globalNav_input == "2") or (globalNav_input == "what's on the menu?"):

            # Asks Which Dining Hall and What Meal Time.
            user_input1 = normalize_choice(input("Which Dining Hall?\n" \
                                "1. 251 North\n" \
                                "2. South\n" \
                                "3. The Y\n\n").strip().lower())

            user_input2 = normalize_choice(input("What Meal Time?\n" \
                                "1. Breakfast\n" \
                                "2. Lunch\n" \
                                "3. Dinner\n\n").strip().lower())

            # Uses the questions to accurately print the correct menu 
            if (user_input1 == "251 north" or user_input1 == "1") and (user_input2 == "breakfast" or user_input2 == "1"):
                for food in sample_foods_251_north_breakfast:
                    print(food)
            elif (user_input1 == "251 north" or user_input1 == "1") and (user_input2 == "lunch" or user_input2 == "2"):
                for food in sample_foods_251_north_lunch:
                    print(food)
            elif (user_input1 == "251 north" or user_input1 == "1") and (user_input2 == "dinner" or user_input2 == "3"):
                for food in sample_foods_251_north_dinner:
                    print(food)
            elif (user_input1 == "south" or user_input1 == "2") and (user_input2 == "breakfast" or user_input2 == "1"):
                for food in sample_foods_south_breakfast:
                    print(food)
            elif (user_input1 == "south" or user_input1 == "2") and (user_input2 == "lunch" or user_input2 == "2"):
                for food in sample_foods_south_lunch:
                    print(food)
            elif (user_input1 == "south" or user_input1 == "2") and (user_input2 == "dinner" or user_input2 == "3"):
                for food in sample_foods_south_dinner:
                    print(food)
            elif (user_input1 == "the y" or user_input1 == "3") and (user_input2 == "breakfast" or user_input2 == "1"):
                for food in sample_foods_the_y_breakfast:
                    print(food)
            elif (user_input1 == "the y" or user_input1 == "3") and (user_input2 == "lunch" or user_input2 == "2"):
                for food in sample_foods_the_y_lunch:
                    print(food)
            elif (user_input1 == "the y" or user_input1 == "3") and (user_input2 == "dinner" or user_input2 == "3"):
                for food in sample_foods_the_y_dinner:
                    print(food)
            else:
                print("Invalid dining hall or meal time selection.")
                
            print()

            # If user is not logged in, they cannot access the bookmark and commenting features

            # Bookmarking
            if logged_in:
                choice = input("Type an item name to bookmark it, or press Enter: ").strip()
                if choice != "":
                    if choice in FOOD_BY_NAME:
                        current_user.add_bookmark(choice)
                        print("Bookmarked!")
                    else:
                        print("That item name was not found.")
            else:
                print("Login to bookmark items.")

            # Commenting
            if logged_in and current_user is not None:
                choice = input("Type an item name to review it, or press Enter: ").strip()
                if choice != "":
                    if choice in FOOD_BY_NAME:
                        rating_input = input("Do you like, dislike, or other for the item?\n").strip().lower()
                        if rating_input == "like":
                            food = FOOD_BY_NAME[choice]
                            food.update_rating(food.average_rating + 0.25)
                        elif rating_input == "dislike":
                            food = FOOD_BY_NAME[choice]
                            food.update_rating(food.average_rating - 0.25)
                        else:
                            continue
                        
                        comment_text = input("Feel free to leave a comment. Otherwise press Enter. ").strip()

                        new_review = Review(user=current_user.username, food_name=choice, comment=comment_text)
                        REVIEWS.append(new_review)

                        print("Review submitted.\n")
                        print("Current reviews for that item:")
                        print_reviews_for_food(choice)
                else:
                    print("That item name was not found.")
            else:
                print("Login to leave ratings and comments.")

        # 3. Individual Rankings
        elif (globalNav_input == "3") or (globalNav_input == "individual rankings"):

            # Asks Which Dining Hall and What Meal Time.
            user_input1 = normalize_choice(input("Which Dining Hall?\n" \
                                "1. 251 North\n" \
                                "2. South\n" \
                                "3. The Y\n\n").strip().lower())

            user_input2 = normalize_choice(input("What Meal Time?\n" \
                                "1. Breakfast\n" \
                                "2. Lunch\n" \
                                "3. Dinner\n\n").strip().lower())
            
            # Uses the questions to accurately print the correct individual leaderboard
            if (user_input1 == "1" or user_input1 == "251 north") and (user_input2 == "1" or user_input2 == "breakfast"):
                data = sample_foods_251_north_breakfast
                title = "251 North Breakfast Top 10"
            elif (user_input1 == "1" or user_input1 == "251 north") and (user_input2 == "2" or user_input2 == "lunch"):
                data = sample_foods_251_north_lunch
                title = "251 North Lunch Top 10"
            elif (user_input1 == "1" or user_input1 == "251 north") and (user_input2 == "3" or user_input2 == "dinner"):
                data = sample_foods_251_north_dinner
                title = "251 North Dinner Top 10"
            elif (user_input1 == "2" or user_input1 == "south") and (user_input2 == "1" or user_input2 == "breakfast"):
                data = sample_foods_south_breakfast
                title = "South Breakfast Top 10"
            elif (user_input1 == "2" or user_input1 == "south") and (user_input2 == "2" or user_input2 == "lunch"):
                data = sample_foods_south_lunch
                title = "South Lunch Top 10"
            elif (user_input1 == "2" or user_input1 == "south") and (user_input2 == "3" or user_input2 == "dinner"):
                data = sample_foods_south_dinner
                title = "South Dinner Top 10"
            elif (user_input1 == "3" or user_input1 == "the y") and (user_input2 == "1" or user_input2 == "breakfast"):
                data = sample_foods_the_y_breakfast
                title = "The Y Breakfast Top 10"
            elif (user_input1 == "3" or user_input1 == "the y") and (user_input2 == "2" or user_input2 == "lunch"):
                data = sample_foods_the_y_lunch
                title = "The Y Lunch Top 10"
            elif (user_input1 == "3" or user_input1 == "the y") and (user_input2 == "3" or user_input2 == "dinner"):
                data = sample_foods_the_y_dinner
                title = "The Y Dinner Top 10"
            else:
                print("Invalid dining hall or meal time selection.")
                continue
            
            # Get the top 10
            top10 = top_n_by_rating(data, 10)

            # print results
            print(f"\n{title}")
            print("-" * len(title))

            count = 1
            for food in top10:
                print(f"{count}. {food.name} | {food.dining_hall} | Rating: {food.average_rating} | {food.dietary_restrictions}")
                count += 1

        # 4. Bookmarks
        elif (globalNav_input == "4") or (globalNav_input == "bookmarks"):
                # If user isn't logged in, they cannot access this function
                if not logged_in or current_user is None:
                    print("You must be logged in to view bookmarks.")
                    continue
                else:
                    print("Current Bookmarks")
                    print("--------------------")

                    if not current_user.bookmarks:
                        print("No bookmarks yet.")
                    else:
                        for food_name in current_user.bookmarks:
                            food = FOOD_BY_NAME.get(food_name)
                            if food:
                                print(food)
                                print()
                            else:
                                print(f"item name: {food_name}")
                
                if current_user.bookmarks:
                    remove_choice = input("Type an item name to remove it, or press Enter: ").strip()
                    if remove_choice != "":
                        if remove_choice in current_user.bookmarks:
                            current_user.remove_bookmark(remove_choice)
                            print("Removed bookmark.")
                        else:
                            print("That item name is not in your bookmarks.")

        # 5. quit
        elif (globalNav_input == "5") or (globalNav_input == "quit"):
            # Wil close the program
            print("Quitting. Goodbye!")
            break
        
        else:
            print("Not an option. Try again.")

'''Remove Temp Tag''''''Make a test case'''
def parse_args():
    parser = argparse.ArgumentParser(description="UMD Food Recommender (terminal app)")
    parser.add_argument("--skip-login", action="store_true", help="Skip the login prompt")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    print("Welcome to the UMD Food Recommender App!\n")
    
    print("Here, we do not require login to start exploring. " \
    "Feel free to browse the menus, recommendations, and dining hall" \
    " leaderboards. However, if you'd like to bookmark dishes, leave comments," \
    " or like/dislike posts, you'll need to login to do so.\n")
    
    print("We hope you discover a new favorite meal during your next visit to" \
    " one of UMD's dining halls!\n")
    
    globalNav(skip_login=args.skip_login)