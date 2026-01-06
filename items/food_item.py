#Each Food Item has a name, dining hall, dietary restrictions, and a rating
#Rating should be 0 initially

class Food_item:
    def __init__(self, food_id, name, dining_hall, meal_time, dietary_restrictions, average_rating):
        self.food_id = food_id
        self.name = name
        self.dining_hall = dining_hall
        self.meal_time = meal_time
        self.dietary_restrictions = dietary_restrictions
        self.average_rating = average_rating

    def update_rating(self, new_rating):
        self.average_rating += new_rating
    
    def __str__(self):
        if self.dietary_restrictions:
            restrictions = ", ".join(self.dietary_restrictions)
        else:
            restrictions = "None"
        return f"{self.name} | {self.dining_hall} | {self.meal_time} | {restrictions}"