
class User:
    def __init__(self, username):
        self.username = username
        self.bookmarks = []

    def add_bookmark(self, food_id):
        if food_id not in self.bookmarks:
            self.bookmarks.append(food_id)
    
    def remove_bookmark(self, food_id):
        if food_id in self.bookmarks:
            self.bookmarks.remove(food_id)