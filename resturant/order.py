from resturant.connection import MyDB


class Order:
    def __init__(self):
        self.my_db = MyDB()
        self.all_items = None

    def add_order(self, tbl, ordered_items):  # ordered_items = [(1,2),(5,2)]
        qry = "INSERT INTO orders (tbl_no) values (%s)"
        values = (tbl,)
        order_id = self.my_db.return_id(qry, values)
        for i in ordered_items:
            qry = "INSERT INTO ordered_items (order_id, item_id, qty) values (%s, %s, %s)"
            values = (order_id, i[0], i[-1])
            self.my_db.iud(qry, values)

        return True

    def update_order(self):
        pass

    def show_order(self):
        self.all_items = []
        qry = "SELECT * FROM items"
        items_here = self.my_db.show_data(qry)
        for i in items_here:
            self.all_items.append(i)
        return self.all_items

    def show_order_id(self):
        qry = "SELECT id from orders"
        order_ids = self.my_db.show_data(qry)
        return order_ids

    def show_order_by_order_id(self, order_id):
        qry = """SELECT ordered_items.id, orders.id as customer_id, orders.tbl_no, items.name, items.type,
                    items.price, ordered_items.qty, (items.price*ordered_items.qty) as amount FROM ordered_items
                    JOIN items ON ordered_items.item_id = items.id
                    JOIN orders ON ordered_items.order_id = orders.id
                    WHERE ordered_items.order_id = %s"""
        vals = (order_id,)
        orders = self.my_db.show_data_p(qry, vals)
        return orders

    def cancel_order(self, index):
        qry = """delete from ordered_items where order_id = %s"""
        value = (index,)
        self.my_db.iud(qry, value)
        return True

    def delete_order(self, index):
        qry = "DELETE FROM ordered_items WHERE id = %s"
        value = (index,)
        self.my_db.iud(qry, value)
        return True

    def disable(self, id):
        qry = "UPDATE orders SET status='A' where id=%s"
        value = (id,)
        return self.my_db.iud(qry, value)

    def not_disable(self, id):
        qry = "select status from orders where id=%s"
        value = (id,)
        return self.my_db.show_data_p(qry, value)

    def remain(self, id):
        qry = "UPDATE orders SET remain='A' where id=%s"
        value = (id,)
        return self.my_db.iud(qry, value)

    def other_remain(self, id):
        qry = "UPDATE orders SET remain='A' where id=%s"
        value = (id,)
        return self.my_db.iud(qry, value)

    def not_remain(self, id):
        qry = "select remain from orders where id=%s"
        value = (id,)
        return self.my_db.show_data_p(qry, value)

    def no_remain(self, tbl):
        qry = "select remain from orders where tbl_no=%s"
        value = (tbl,)
        return self.my_db.show_data_p(qry, value)

    def show_order_tbl(self):
        qry = "SELECT tbl_no from orders"
        return self.my_db.show_data(qry)
