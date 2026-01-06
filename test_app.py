from items.food_item import Food_item
from items.user import User
from items.review import Review
import main
import builtins
import io
import sys
import pytest

# To run this file do "pytest .\Final_Project\test_app.py"

# Tests the Regular Expressions function
def test_normalize_choice_extracts_number():
    assert main.normalize_choice("1") == "1"
    assert main.normalize_choice("1)") == "1"
    assert main.normalize_choice("Option 2") == "2"
    assert main.normalize_choice("   Breakfast  ") == "breakfast"

# TOP-N RANKING TESTS
# These tests verify the behavior of the top_n_by_rating()
def test_top_n_empty_list():
    """If the input list is empty, the function should return an empty list without crashing."""

    assert main.top_n_by_rating([], 10) == []

def test_top_n_by_rating_sorts_desc():
    """Ensures foods are sorted in descending order by rating and that the top N items are returned correctly."""

    foods = [
        Food_item("1", "Apple", "South", "Breakfast", [], 2.0),
        Food_item("2", "Banana", "South", "Breakfast", [], 5.0),
        Food_item("3", "Cupcake", "South", "Breakfast", [], 3.5),
    ]

    top2 = main.top_n_by_rating(foods, 2)

    assert top2[0].name == "Banana"
    assert top2[1].name == "Cupcake"

def test_top_n_more_than_length():
    """If N is larger than the list size, the function should simply return all available items."""

    foods = [
        Food_item("1", "Apple", "South", "Breakfast", [], 2.0),
        Food_item("2", "Banana", "South", "Breakfast", [], 5.0),
    ]
    top10 = main.top_n_by_rating(foods, 10)
    assert len(top10) == 2

def test_top_n_ties_does_not_crash():
    """Ensures that ties in ratings are handled correctly and do not cause errors or incorrect filtering."""

    foods = [
        Food_item("1", "Apple", "South", "Breakfast", [], 5.0),
        Food_item("2", "Banana", "South", "Breakfast", [], 5.0),
        Food_item("3", "Cupcake", "South", "Breakfast", [], 4.0),
    ]

    top2 = main.top_n_by_rating(foods, 2)

    assert top2[0].name == "Apple"
    assert top2[0].average_rating == 5.0
    assert top2[1].name == "Banana"
    assert top2[1].average_rating == 5.0


# FOOD RATING TESTS
# These tests verify that food ratings are updated correctly.
def test_food_update_rating_increase():
    """Confirms that updating a food's rating sets the new value correctly."""

    food = Food_item("T", "Test", "The Y", "Lunch", [], 4.0)
    food.update_rating(4.25)
    assert food.average_rating == 8.25

def test_food_update_rating_decrease():
    """Confirms that ratings can also be updated to lower values."""

    food = Food_item("Y", "Test", "The Y", "Lunch", [], 4.0)
    food.update_rating(-2.25)
    assert food.average_rating == 1.75

# REVIEW TESTS
# These tests verify review display behavior.
def test_print_reviews_for_food_none(capsys):
    """If no reviews exist for a food item, the function should print an appropriate message."""

    main.REVIEWS.clear()

    main.print_reviews_for_food("anything")
    out = capsys.readouterr().out
    assert "No reviews yet." in out

def test_print_reviews_for_food_with_one_review(capsys):
    """Confirms that an existing review is printed correctly."""

    main.REVIEWS.clear()

    r = Review(user="test@terpmail.umd.edu", food_name="X", comment="Great")
    main.REVIEWS.append(r)

    main.print_reviews_for_food("X")
    out = capsys.readouterr().out
    assert "Great" in out

# BOOKMARK TESTS
# These tests verify bookmark add/remove logic and duplication prevention.
def test_user_bookmarks_add_remove_no_duplicates():
    """Ensures bookmarks can be added, duplicates are prevented, and bookmarks can be removed."""

    user = User("test@terpmail.umd.edu")

    user.add_bookmark("Smash Burger")
    assert "Smash Burger" in user.bookmarks

    user.add_bookmark("Smash Burger")
    assert user.bookmarks.count("Smash Burger") == 1

    user.remove_bookmark("Smash Burger")
    assert "Smash Burger" not in user.bookmarks

# DATA STRUCTURE TESTS
# These tests verify global data mappings.
def test_food_by_name_lookup_contains_expected_key():
    """Ensures FOOD_BY_NAME is populated and maps food names to Food_item objects correctly."""

    assert isinstance(main.FOOD_BY_NAME, dict)
    assert len(main.FOOD_BY_NAME) > 0

    some_name = next(iter(main.FOOD_BY_NAME.keys()))
    assert main.FOOD_BY_NAME[some_name].name == some_name

# USER INPUT TESTS
# These tests simulate user input flows through the app.
def run_globalNav_with_inputs(inputs, skip_login=False):
    """Helper function that simulates user input for globalNav() and captures printed output."""

    input_iter = iter(inputs)

    def fake_input(prompt=""):
        try:
            return next(input_iter)
        except StopIteration:
            return "5"

    old_input = builtins.input
    old_stdout = sys.stdout

    try:
        builtins.input = fake_input
        sys.stdout = io.StringIO()
        main.globalNav(skip_login=skip_login)
        return sys.stdout.getvalue()
    finally:
        builtins.input = old_input
        sys.stdout = old_stdout

# Test for parse-args --skip_login
def test_skip_login_starts_without_login_prompt():
    out = run_globalNav_with_inputs([
        "5"   # quit immediately
    ], skip_login=True)

    # It should NOT ask "Would you like to login?"
    assert "Would you like to login?" not in out
    assert "Quitting. Goodbye!" in out

def test_login_no_then_quit():
    """User chooses not to log in and exits the application."""

    out = run_globalNav_with_inputs(["no", "5"])
    assert "Quitting. Goodbye!" in out

def test_invalid_global_option_then_quit():
    """Invalid menu option should display an error message."""

    out = run_globalNav_with_inputs(["no", "99", "5"])
    assert "Not an option" in out

def test_overall_ranking_breakfast_then_quit():
    """Tests overall breakfast leaderboard display."""

    out = run_globalNav_with_inputs(["no", "1", "1", "5"])
    assert "Overall Breakfast Top 10" in out

def test_overall_ranking_invalid_meal_then_quit():
    """Invalid meal selection should display an error."""

    out = run_globalNav_with_inputs(["no", "1", "9", "5"])
    assert "Invalid meal time selection." in out

def test_whats_on_menu_no_login():
    """Verifies that non-logged-in users cannot bookmark or review items."""

    out = run_globalNav_with_inputs(["no", "2", "1", "1", "5"])
    assert "Login to bookmark items." in out
    assert "Login to leave ratings and comments." in out

def test_whats_on_menu_invalid_hall_then_quit():
    """Invalid dining hall selection should be handled gracefully."""

    out = run_globalNav_with_inputs(["no", "2", "9", "1", "5"])
    assert "Invalid dining hall or meal time selection." in out

def test_whats_on_menu_accepts_weird_number_input():
    out = run_globalNav_with_inputs([
        "no",
        "2",
        "1)",   # should parse to "1"
        "1)",   # should parse to "1"
        "5"
    ])
    assert "Login to bookmark items." in out

def test_login_yes_then_whats_on_menu_skip_bookmark_and_review_then_quit():
    """Logged-in user navigates menu but skips bookmarking and reviewing."""

    out = run_globalNav_with_inputs([
        "yes",
        "test@terpmail.umd.edu",
        "GoTerps!",
        "2",
        "1",
        "1",
        "",
        "",
        "5"
    ])
    assert "Login successful!" in out

def test_login_yes_then_bookmarks_menu_then_quit():
    """Logged-in user accesses bookmarks menu."""

    out = run_globalNav_with_inputs([
        "yes",
        "test@terpmail.umd.edu",
        "GoTerps!",
        "4",
        "",
        "5"
    ])
    assert "Current Bookmarks" in out

def test_login_wrong_email_then_quit():
    """Login should fail if email domain is invalid."""

    out = run_globalNav_with_inputs(["yes", "notumd@gmail.com", "5"])
    assert "Invalid email" in out

def test_login_wrong_password_then_quit():
    """Login should fail if password is incorrect."""

    out = run_globalNav_with_inputs([
        "yes",
        "test@terpmail.umd.edu",
        "wrongpass",
        "5"
    ])
    assert "Invalid password" in out

def test_login_then_bookmark_item_then_view_bookmarks():
    """Full integration test: login to bookmark item to view bookmarks."""

    some_item = next(iter(main.FOOD_BY_NAME.keys()))

    out = run_globalNav_with_inputs([
        "yes",
        "test@terpmail.umd.edu",
        "GoTerps!",
        "2",
        "1",
        "1",
        some_item,
        "",
        "4",
        "",
        "5"
    ])
    assert "Bookmarked!" in out
    assert "Current Bookmarks" in out