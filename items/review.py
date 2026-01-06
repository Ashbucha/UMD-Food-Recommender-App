#File for both Comment and Rating which are tied to each food item

class Review:
    def __init__(self, user, food_name, comment=""):
        self.user = user
        self.food_name = food_name
        self.comment = comment

    def __str__(self):
        return f"{self.user} | {self.food_name} | {self.comment}"