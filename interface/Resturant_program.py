from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from resturant.item import Item
from resturant.order import Order


class ItemView:
    def __init__(self):
        # Item View Interface
        self.window = Tk()
        self.window.title('Add Item')
        self.window.geometry('400x400')
        self.item = Item()

        # Variables used
        self.all_items = []
        self.selected_id = ""

        # Menu
        my_menu = Menu(self.window)
        self.window.config(menu=my_menu)
        test_menu = Menu(my_menu)
        my_menu.add_cascade(label="Order", menu=test_menu)
        test_menu.add_command(label="Add",
                              command=lambda: (self.window.withdraw(), OrderView(self.window, self.all_items)))
        test_menu.add_command(label="View")
        test_menu.add_separator()
        test_menu.add_command(label="Exit", command=self.window.quit)

        my_menu.add_cascade(label="Edit", menu=test_menu)
        my_menu.add_cascade(label="Help", menu=test_menu)

        # Labels and entries for Items
        Label(self.window, text="Name: ").grid(row=0, column=0, padx=10, pady=(5,))

        self.entry_name = Entry(self.window)
        self.entry_name.grid(row=0, column=1)

        Label(self.window, text="Type: ").grid(row=1, column=0, padx=10, pady=(5,))

        self.entry_type = Entry(self.window)
        self.entry_type.grid(row=1, column=1)

        Label(self.window, text="Rate: ").grid(row=2, column=0, padx=10, pady=(5,))

        self.entry_rate = Entry(self.window)
        self.entry_rate.grid(row=2, column=1)

        # Buttons
        Button(self.window, text="Add Item", command=self.add_item).grid(row=3, column=0, padx=(50, 5), pady=5)

        Button(self.window, text="Update Item", command=self.update_item).grid(row=3, column=1, padx=(15, 5), pady=5)

        Button(self.window, text="Delete Item", command=self.delete_item).grid(row=4, column=0, columnspan=2, padx=15,
                                                                               pady=5)

        # Tree view for items list
        self.item_tree = ttk.Treeview(self.window, columns=("name", "type", "rate"))
        self.item_tree.grid(row=5, column=0, columnspan=3, padx=50)
        self.item_tree['show'] = 'headings'
        self.item_tree.heading("name", text='Name')
        self.item_tree.heading("type", text='Type')
        self.item_tree.heading("rate", text='Rate')
        self.item_tree.column("name", width=100)
        self.item_tree.column("type", width=100)
        self.item_tree.column("rate", width=100)

        # default showing the list
        self.show_item_tree()

        # Closing window
        self.window.mainloop()

    # Adding item to the list
    def add_item(self):
        name = self.entry_name.get()
        type = self.entry_type.get()
        rate = self.entry_rate.get()
        if self.item.add_item(name, type, rate):
            self.show_item_tree()
        else:
            messagebox.showerror("Error", "Item cannot be added")

    # Updating existing item
    def update_item(self):
        # print(self.id)
        name = self.entry_name.get()
        type = self.entry_type.get()
        rate = self.entry_rate.get()
        if self.item.update_item(name, type, rate, self.selected_id):
            self.show_item_tree()
        else:
            messagebox.showerror("Error", "Item cannot be updated")

    # Deleting existing item
    def delete_item(self):
        if self.item.delete_item(self.selected_id):
            self.entry_name.delete(0, END)
            self.entry_type.delete(0, END)
            self.entry_rate.delete(0, END)
            self.show_item_tree()
        else:
            messagebox.showwarning("Warning", "Couldn't delete")

    # Show Item list
    def show_item_tree(self):
        self.item_tree.delete(*self.item_tree.get_children())
        self.all_items = self.item.show_items()
        for i in self.all_items:
            self.item_tree.insert("", "end", text=i[0], values=(i[1], i[2], i[3]))

        self.item_tree.bind("<Double-1>", self.on_select)

    # Double click function
    def on_select(self, event):
        selected_id = self.item_tree.selection()[0]
        self.selected_id = self.item_tree.item(selected_id, 'text')
        selected_data = self.item_tree.item(selected_id, 'values')
        self.entry_name.delete(0, END)
        self.entry_name.insert(0, selected_data[0])
        self.entry_type.delete(0, END)
        self.entry_type.insert(0, selected_data[1])
        self.entry_rate.delete(0, END)
        self.entry_rate.insert(0, selected_data[2])


class OrderView(ItemView):
    def __init__(self, mainwin, items):
        self.items = items
        self.added_item = IntVar()

        self.orders = Order()

        # Variable used
        self.ordered_item = []
        self.item_to_add = []
        self.tbl_view = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.tbl_id = self.orders.show_order_id()
        self.tbl_id = [i[0] for i in self.tbl_id]
        self.tbl_id = ["Bill No", ] + self.tbl_id

        self.selected_id = ""
        self.selected_data = ()

        # Order interface
        self.master = Toplevel(mainwin)
        self.master.title('Order View')
        self.master.geometry('550x450')

        # Menu
        my_menu = Menu(self.master)
        self.master.config(menu=my_menu)
        test_menu = Menu(my_menu)
        my_menu.add_cascade(label="File", menu=test_menu)
        test_menu.add_command(label="Back", command=lambda: (self.master.destroy(), mainwin.deiconify()))
        test_menu.add_separator()
        test_menu.add_command(label="Exit", command=mainwin.destroy)

        # Frame for Menu
        self.window = LabelFrame(self.master, padx=10, pady=10)
        self.window.place(anchor=NW)

        self.show_order_button()

        # Insert data
        self.tbl_no = Label(self.window, text="Table", padx=10, pady=10)
        self.tbl_no.grid(row=4, column=0)

        self.combo_tbl = ttk.Combobox(self.window, state='readonly')
        self.combo_tbl.grid(row=4, column=1, padx=10, pady=10)
        self.combo_tbl['value'] = self.tbl_view

        self.label_qty = Label(self.window, text="Qty")
        self.label_qty.grid(row=2, column=0, pady=5)

        self.entry_qty = Entry(self.window)
        self.entry_qty.grid(row=2, column=1, pady=5)

        self.item_name = Label(self.window, text="Items")
        self.item_name.grid(row=0, column=0)

        self.item_entry = Entry(self.window)
        self.item_entry.grid(row=0, column=1)

        # Tree view for ordering
        self.item_tree = ttk.Treeview(self.window, columns=("name", "type", "rate"))
        self.item_tree.grid(row=1, column=0, columnspan=2)
        self.item_tree['show'] = 'headings'
        self.item_tree.heading("name", text='Name')
        self.item_tree.heading("type", text='Type')
        self.item_tree.heading("rate", text='Rate')
        self.item_tree.column("name", width=100)
        self.item_tree.column("type", width=100)
        self.item_tree.column("rate", width=100)
        for i in self.items:
            self.item_tree.insert("", "end", text=i[0], values=(i[1], i[2], i[3]))

        self.item_tree.bind("<Double-1>", self.trythis)

        self.combo_tbl.bind("<<ComboboxSelected>>")  # Single click event

        # Frame for Order
        self.label = LabelFrame(self.master, padx=10, pady=10)
        self.label.place(anchor=N)

        # Buttons
        Button(self.window, text="Add Order", command=self.adding_order).grid(row=3, column=0, columnspan=2)
        Button(self.window, text="Confirm Order", command=self.confirming_order).grid(row=5, column=0, columnspan=2)

        # Closing window
        self.master.mainloop()

    def show_order_button(self):
        # Show Order Button
        clicked = IntVar()
        OptionMenu(self.window, clicked, *self.tbl_id).grid(row=6, column=0, sticky="EW")
        Button(self.window, text="Show Order", command=lambda: self.treeview_order(clicked)).grid(row=6, column=1)

    def trythis(self, event):  # Store the Id and values of single selected item
        selected_id = self.item_tree.selection()
        self.selected_id = self.item_tree.item(selected_id, 'text')
        self.selected_data = self.item_tree.item(selected_id, 'values')
        self.item_entry.delete(0, END)
        self.item_entry.insert(0, self.selected_data[-2::-1])

    def adding_order(self):
        qty = self.entry_qty.get()
        self.ordered_item.append(((self.selected_id,) + self.selected_data + (qty,)))
        self.showing_order()

    def showing_order(self):
        self.label.destroy()
        self.label = LabelFrame(self.master)
        self.label.place(x="350", y="10")
        self.A = 0
        self.Lb = Label(self.label, text='')
        self.Lb.pack()
        try:

            for i in range(len(self.ordered_item)):
                self.Rd = Radiobutton(self.label,
                                      text="{} {} {}".format(self.ordered_item[i][-3], self.ordered_item[i][-4],
                                                             self.ordered_item[i][-1]),
                                      variable=self.added_item,
                                      value=i).pack()
                self.A = self.A + 1
            self.bt1 = Button(self.label, text="Delete Order",
                              command=lambda: self.delete_single_order((self.added_item.get())))
            self.bt1.pack()

        except IndexError:
            self.Lb.config(text='Select The Item To be Ordered')
            self.ordered_item.clear()

    def delete_single_order(self, item):
        try:

            self.ordered_item.pop(item)
            self.A = self.A - 1

            self.showing_order()
            if self.A == 0:
                self.label.destroy()

        except IndexError:

            self.Lb.config(text='None Selected')

    def confirming_order(self):
        tbl = self.combo_tbl.get()
        remain = self.orders.no_remain(tbl)
        print(remain)
        number = self.orders.show_order_tbl()
        if (int(tbl),) in number and remain[-1] == (None,):
            messagebox.showerror("already", "Bhayena bhai")
        else:
            self.showing_order()
            if self.orders.add_order(tbl, self.ordered_item):
                messagebox.showinfo("Added Order", "Your order as been added")
                number = self.orders.show_order_tbl()
                print(number)
                self.tbl_id = self.orders.show_order_id()
                self.tbl_id = [i[0] for i in self.tbl_id]
                self.show_order_button()
            else:
                messagebox.showerror("Error", "We couldn't add your order")

    def treeview_order(self, selected_tbl_id):
        window = Toplevel(self.master)
        OptionMenu(window, selected_tbl_id, *self.tbl_id, command=self.treeview_order_next).pack()

        # Simple frame
        self.a = LabelFrame(window, width=10)
        self.a.pack()

        # Interface to Show Orders
        self.order_tree = ttk.Treeview(window, columns=("name", "type", "rate", "qty", "amount"))
        self.order_tree.pack(padx=10, pady=10)
        self.order_tree['show'] = 'headings'
        self.order_tree.heading("name", text='Name')
        self.order_tree.heading("type", text='Type')
        self.order_tree.heading("rate", text='Rate')
        self.order_tree.heading("qty", text='Qty')
        self.order_tree.heading("amount", text='Amount')
        self.order_tree.column("name", width=100)
        self.order_tree.column("type", width=100)
        self.order_tree.column("rate", width=100)
        self.order_tree.column("qty", width=100)
        self.order_tree.column("amount", width=100)
        self.tbl = selected_tbl_id.get()
        try:
            a = self.orders.show_order_by_order_id(self.tbl)
            Label(self.a, text="Table").grid(row=0, column=0)
            Label(self.a, text=a[0][2]).grid(row=0, column=1)
        except Exception:
            a = []
        for i in a:
            self.order_tree.insert("", "end", text=i[0], values=i[3:])

        self.order_tree.bind("<Double-1>", self.on_select)

        self.cancel = Button(window, text="Cancel Order", state=NORMAL,
                             command=lambda: self.cancel_order(self.tbl))
        self.cancel.pack()
        self.complete = Button(window, text="Complete", state=NORMAL, command=lambda: self.running(self.tbl))
        self.complete.pack()
        self.gone = Button(window, text="Gone", state=DISABLED, command=lambda: self.not_running(self.tbl))
        self.gone.pack()
        if self.orders.not_disable(self.tbl)[0][0] == "A":
            self.cancel["state"] = DISABLED
            self.complete["state"] = DISABLED
            self.gone["state"] = NORMAL

    def treeview_order_next(self, selected_tbl_id):
        self.tbl = selected_tbl_id
        self.order_tree.delete(*self.order_tree.get_children())
        try:
            a = self.orders.show_order_by_order_id(self.tbl)
            Label(self.a, text="Table").grid(row=0, column=0)
            Label(self.a, text=a[0][2]).grid(row=0, column=1)
        except Exception:
            a = []
        for i in a:
            self.order_tree.insert("", "end", text=i[0], values=i[3:])
        self.cancel["state"] = NORMAL
        self.complete["state"] = NORMAL
        self.gone["state"] = DISABLED
        if self.orders.not_disable(selected_tbl_id)[0][0] == "A":
            self.cancel["state"] = DISABLED
            self.complete["state"] = DISABLED
            self.gone["state"] = NORMAL
        if self.orders.not_remain(selected_tbl_id)[0][0]:
            self.cancel["state"] = DISABLED
            self.complete["state"] = DISABLED
            self.gone["state"] = DISABLED

    def on_select(self, event):
        selected_id = self.order_tree.selection()[0]
        selected_id = self.order_tree.item(selected_id, 'text')
        if self.orders.delete_order(selected_id):
            self.treeview_order_next(self.tbl)
        else:
            messagebox.showwarning("Warning", "Couldn't delete")

    def not_running(self, selected_id):
        self.orders.other_remain(selected_id)
        self.treeview_order_next(selected_id)

    def running(self, selected_id):
        self.orders.disable(selected_id)
        self.treeview_order_next(selected_id)

    def cancel_order(self, selected_id):
        pass


ItemView()
