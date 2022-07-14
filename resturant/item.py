from resturant.connection import MyDB


class Item:
    def __init__(self):
        self.my_db = MyDB()
        self.all_items = []

    def add_item(self, name, type, rate):
        qry = "INSERT INTO items(name,type,price) VALUES (%s,%s,%s)"
        value = (name, type, rate)
        self.my_db.iud(qry, value)
        return True

    def show_items(self):
        self.all_items = []
        qry = "SELECT * FROM items"
        items_here = self.my_db.show_data(qry)
        for i in items_here:
            self.all_items.append(i)
        return self.all_items

    def update_item(self, name, type, rate, index):
        qry = "UPDATE items SET name =%s, type=%s, price=%s WHERE id= %s"
        value = (name, type, rate, index)
        self.my_db.iud(qry, value)
        return True

    def delete_item(self, index):
        qry = "DELETE FROM items WHERE id = %s"
        value = (index,)
        self.my_db.iud(qry, value)
        return True
