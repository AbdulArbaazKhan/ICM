from tkinter import *
from tkinter import ttk, messagebox
import sqlite3




def label(frame, x, y, **kwargs):
    Label(frame, kwargs, font="lucinda 12 bold",
          bg="#23292E", fg="white", width=12, anchor="w", padx=2).grid(row=x, column=y, sticky="w", padx=10, pady=5)


def entry(frame, r, c, **kwargs):
    ent = Entry(frame, kwargs, font="lucida 12", width=20, bd=2, relief=GROOVE)
    ent.grid(row=r, column=c, padx=10, pady=5, ipady=1)


def Customer():
    def show_records():
        """ This will fill the records in tree view """
        try:
            cursr.execute("SELECT * FROM employee ORDER BY eid;")
            records = cursr.fetchall()
            employee_tv.delete(*employee_tv.get_children())
            for record in records:
                employee_tv.insert('', END, text="GAME", values=record)
        except EXCEPTION as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent=root2)

    def add():
        """ This will add the records in database and show in tree view """

        try:
            if All_strings_var[0].get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=root2)
            elif All_strings_var[6].get() == "Choose" or All_strings_var[7].get() == "Select":
                messagebox.showerror("Error", "Some more info required", parent=root2)

            elif All_strings_var[0].get().isnumeric():
                cursr.execute(f"SELECT * FROM `employee` where eid={All_strings_var[0].get()};")
                row = cursr.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID has already be assigned, try different",
                                         parent=root2)
                else:
                    cursr.execute(
                        f"""INSERT INTO `employee` (`eid`, `name`, `email`, `passw`, `contact`, `dob`, `address`, `doj`, `gender`, `usertype`) VALUES ("{All_strings_var[0].get()}", "{All_strings_var[1].get()}", "{All_strings_var[2].get()}", "{All_strings_var[3].get()}", "{All_strings_var[4].get()}", "{All_strings_var[5].get()}", "{text_area.get(str(1.0), END)}", current_timestamp , "{All_strings_var[6].get()}", "{All_strings_var[7].get()}");""")
                    conct.commit()
                    messagebox.showinfo("Success", "Employee Added successfully", parent=root2)
                    show_records()
            else:
                messagebox.showerror("Error", "Employee ID must be integer", parent=root2)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent=root2)

    def get_record_from_tv(event):
        """ This will get the record from the tree view """

        f = employee_tv.focus()
        record = (employee_tv.item(f))['values']  # here is the record by click

        if record != "":
            text_area.delete("1.0", END)
            text_area.insert(END, record[6])
            t = 0
            for i in range(len(record)):
                if i == 6 or i == 7:
                    continue
                All_strings_var[t].set(record[i])
                t += 1

    def clear():
        """ This will clear all the fields """

        text_area.delete('1.0', END)
        for v in All_strings_var:
            v.set("")
        combo1.set("Choose")
        combo2.set("Select")
        show_records()
        search_query.set("")
        search_var.set("Select")

    def delete():
        """ This will delete a particular record from the database and show in tree view """

        try:
            if All_strings_var[0].get() == "":
                messagebox.showerror("Error", "Employee ID must be required", parent=root2)
            if All_strings_var[0].get().isnumeric():
                cursr.execute(f"SELECT * FROM `employee` where eid={All_strings_var[0].get()};")
                row = cursr.fetchone()
                if row is not None:
                    permission = messagebox.askyesno("Confirm", "Are you sure?", parent=root2)
                    if permission:
                        cursr.execute(f"DELETE FROM employee WHERE eid={All_strings_var[0].get()}")
                        conct.commit()
                        messagebox.showinfo("Deletion", f"Employee has been deleted successfully!", parent=root2)
                        # show_records()
                        clear()
                else:
                    messagebox.showerror("Error", "Invalid Employee ID!", parent=root2)
        except Exception as e:
            messagebox.showerror("Error", f"{str(e)}", parent=root2)

    def edit():
        """ This will edit the fields, save the changes and show in tree view"""

        try:
            if All_strings_var[0].get() == "":
                messagebox.showerror("Error", "Employee ID must be unique", parent=root2)
            elif All_strings_var[0].get().isnumeric():
                cursr.execute(f"SELECT * FROM `employee` where eid={All_strings_var[0].get()};")
                row = cursr.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid Employee ID", parent=root2)
                else:
                    cursr.execute(
                        f"UPDATE `employee` SET `name`='{All_strings_var[1].get()}',`email`='{All_strings_var[2].get()}',`passw`='{All_strings_var[3].get()}',`contact`='{All_strings_var[4].get()}',`dob`='{All_strings_var[5].get()}',`address`='{text_area.get(str(1.0), END)}',`doj`='{row[7]}',`gender`='{All_strings_var[6].get()}',`usertype`='{All_strings_var[7].get()}' WHERE eid={All_strings_var[0].get()}")
                    conct.commit()
                    messagebox.showinfo("Success", "Employee updated successfully", parent=root2)
                    show_records()
            else:
                messagebox.showerror("Error", "Employee ID must be integer", parent=root2)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent=root2)

    def search():
        """ This will search record(or records) by the option you'll select """

        if search_var.get() == "Select":
            messagebox.showinfo("Error", "Search by the search option", parent=root2)
        elif search_query.get() == "":
            messagebox.showerror("Error", "Search entry must be filled")
        else:
            if search_var.get() != "ID":
                cursr.execute(
                    f"SELECT * FROM employee WHERE {(search_var.get()).lower()} LIKE '%{search_query.get()}%' ORDER  BY eid;")
            else:
                cursr.execute(
                    f"SELECT * FROM employee WHERE e{(search_var.get()).lower()} LIKE '%{search_query.get()}%' ORDER  BY eid;")
            rows = cursr.fetchall()
            if len(rows) == 0:
                messagebox.showinfo("Search", "Sorry, No result found!", parent=root2)
            else:
                employee_tv.delete(*employee_tv.get_children())
                for row in rows:
                    employee_tv.insert('', END, values=row)

    root2 = Toplevel(root)
    root2.geometry("980x700+240+166")
    root2.title("Customer Management")
    root2.focus_force()
    employee_frame = LabelFrame(root2, text="Employee Details", font="goudyoldstyle 10 bold", bd=2, relief=GROOVE,
                                pady=40)
    r = 0
    c = 0
    All_strings_var.clear()
    for txt in ["Employee ID", "Name", "Email", "Password", "Contact No", "D O B", "Address", "Gender",
                "User Type"]:
        var = StringVar()
        label(employee_frame, r, c, text=txt, )
        if r == 6:
            text_area = Text(employee_frame, font="goudyoldstyle 10", height=4, width=26, bd=2, relief=GROOVE)
            text_area.grid(row=r, column=c + 1)
            r += 1
            continue
        All_strings_var.append(var)
        if r == 7:
            combo1 = ttk.Combobox(employee_frame, cursor="hand2", values=("Male", "Female", "Other"),
                                  state="readonly",
                                  justify=CENTER, textvariable=var, width=20, font="guodyoldstyle 10")
            combo1.grid(row=r, column=c + 1)
            combo1.set("Choose")
            r += 1
            continue
        if r == 8:
            combo2 = ttk.Combobox(employee_frame, cursor="hand2", values=("Admin", "Cutomer"), state="readonly",
                                  justify=CENTER, textvariable=var, width=20, font="guodyoldstyle 10")
            combo2.grid(row=r, column=c + 1)
            combo2.set("Select")
            r += 1
            continue
        if r == 3:
            entry(employee_frame, r, c + 1, textvariable=var, show="*")
            r += 1
            continue
        entry(employee_frame, r, c + 1, textvariable=var)
        r += 1
    Button(employee_frame, text="Add", command=add, bg="#155C73", fg="white", height=2, width=10, cursor="hand2",
           overrelief=FLAT, ).grid(
        row=9,
        column=0,
        pady=4)
    Button(employee_frame, text="Edit", command=edit, bg="#734B66", fg="white", height=2, width=10, cursor="hand2",
           overrelief=FLAT, ).grid(row=9,
                                   column=1,
                                   pady=4)
    Button(employee_frame, text="Delete", command=delete, bg="#474B73", fg="white", height=2, width=10, cursor="hand2",
           overrelief=SOLID, ).grid(row=10,
                                    column=0,
                                    pady=4)
    Button(employee_frame, text="Clear", command=clear, bg="#733823", fg="white", height=2, width=10, overrelief=SOLID,
           cursor="hand2").grid(row=10,
                                column=1,
                                pady=4)
    employee_frame.pack(side=LEFT, fill=Y, padx=2, pady=2)

    search_frame = LabelFrame(root2, text="Search Customer", font="goudyoldstyle 10 bold")
    search_var = StringVar()
    search_query = StringVar()
    combo3 = ttk.Combobox(search_frame, width=20, values=("Name", "Email", "Contact", "ID"), font="lucida 12 bold",
                          justify=CENTER,
                          textvariable=search_var, state="readonly")
    combo3.set("Select")
    combo3.pack(side=LEFT, padx=20)

    Entry(search_frame, width=20, font="lucida 12", textvariable=search_query, relief=RIDGE, bd=2).pack(side=LEFT,
                                                                                                        ipady=4,
                                                                                                        padx=20)
    Button(search_frame, text="Search", command=search, bg="#155C73", fg="white", font="lucida 12", width=10,
           cursor="hand2").pack(
        side=LEFT, padx=20)
    search_frame.pack(ipady=10)

    employee_details_frame = Frame(root2, bd=2, relief=GROOVE)

    scrolly = Scrollbar(employee_details_frame, orient=VERTICAL)
    scrollx = Scrollbar(employee_details_frame, orient=HORIZONTAL)
    employee_tv = ttk.Treeview(employee_details_frame, columns=(
        'eid', "name", "email", "passw", "contact", "dob", "address", "doj", "gender", "usertype"), show="headings",
                               yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrollx.config(command=employee_tv.xview)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.config(command=employee_tv.yview)
    scrolly.pack(side=RIGHT, fill=Y)

    #TODO: This will increase your lines of code only see column can be added below in heading
    # employee_tv.column("eid", width=90)
    # employee_tv.column("name", width=90)
    # employee_tv.column("email", width=90)
    # employee_tv.column("passw", width=90)
    # employee_tv.column("contact", width=90)
    # employee_tv.column("dob", width=90)
    # employee_tv.column("address", width=90)
    # employee_tv.column("doj", width=90)
    # employee_tv.column("gender", width=90)
    # employee_tv.column("usertype", width=90)

    employee_tv.heading(column="eid", text="EMP ID", anchor=CENTER)
    employee_tv.heading("name", text="Name", anchor=CENTER)
    employee_tv.heading("email", text="Email", anchor=CENTER)
    employee_tv.heading("passw", text="Password", anchor=CENTER)
    employee_tv.heading("contact", text="Contact", anchor=CENTER)
    employee_tv.heading("dob", text="D.O.B", anchor=CENTER)
    employee_tv.heading("address", text="Address", anchor=CENTER)
    employee_tv.heading("doj", text="D.O.J", anchor=CENTER)
    employee_tv.heading("gender", text="Gender", anchor=CENTER)
    employee_tv.heading("usertype", text="Authority", anchor=CENTER)

    employee_tv.pack(fill=BOTH, expand=1, side=BOTTOM)
    employee_details_frame.pack(fill=BOTH, expand=1, side=BOTTOM)
    employee_tv.bind("<ButtonRelease-1>", get_record_from_tv)
    show_records()
    root2.mainloop()


def Product():
    def add():
        for v in All_strings_var:
            print(v.get())
    root2 = Toplevel(root)
    root2.geometry("1100x500+100+100")
    root2.focus_force()
    product_frame = LabelFrame(root2, text="Product Details", font="goudyoldstyle 10 bold", bd=2, relief=GROOVE,
                                pady=40)

    #Fetching Categories and Suppliers
    all_categories_details = cursr.execute("SELECT * FROM category ORDER BY cid")
    categories_name = []
    for ct in all_categories_details.fetchall():
        categories_name.append(ct[1])
    all_suppliers_details = cursr.execute("SELECT * FROM supplier ORDER BY invoice")
    supplier_name = []
    for sp in all_suppliers_details.fetchall():
        supplier_name.append(sp[1])


    r = 0
    c = 0
    All_strings_var.clear()
    for txt in ["Category", "Supplier", "Name", "Price", "Quantity", "Status"]:
        var = StringVar()
        label(product_frame, r, c, text=txt, )
        All_strings_var.append(var)
        if r ==0:
            combo1 = ttk.Combobox(product_frame, cursor="hand2", values=categories_name,
                                  state="readonly",
                                  justify=CENTER, textvariable=var, width=20, font="guodyoldstyle 10")
            combo1.grid(row=r, column=c + 1)
            combo1.set("Choose")
            r += 1
            continue
        if r == 1:
            combo2 = ttk.Combobox(product_frame, cursor="hand2", values=supplier_name, state="readonly",
                                  justify=CENTER, textvariable=var, width=20, font="guodyoldstyle 10")
            combo2.grid(row=r, column=c + 1)
            combo2.set("Select")
            r += 1
            continue
        if r == 5:
            combo2 = ttk.Combobox(product_frame, cursor="hand2", values=("Active", "Close"), state="readonly",
                                  justify=CENTER, textvariable=var, width=20, font="guodyoldstyle 10")
            combo2.grid(row=r, column=c + 1)
            combo2.set("Select")
            r += 1
            continue
        entry(product_frame, r, c + 1, textvariable=var)
        r += 1
    Button(product_frame, text="Add", command=add, bg="#155C73", fg="white", height=2, width=10, cursor="hand2",
           overrelief=FLAT, ).grid(
        row=9,
        column=0,
        pady=4)
    Button(product_frame, text="Edit",  bg="#734B66", fg="white", height=2, width=10, cursor="hand2",
           overrelief=FLAT, ).grid(row=9,
                                   column=1,
                                   pady=4)
    Button(product_frame, text="Delete",  bg="#474B73", fg="white", height=2, width=10, cursor="hand2",
           overrelief=SOLID, ).grid(row=10,
                                    column=0,
                                    pady=4)
    Button(product_frame, text="Clear", bg="#733823", fg="white", height=2, width=10, overrelief=SOLID,
           cursor="hand2").grid(row=10,
                                column=1,
                                pady=4)

    product_frame.pack(side=LEFT, fill=Y, padx=2, pady=2)

    search_frame = LabelFrame(root2, text="Search Customer", font="goudyoldstyle 10 bold")
    search_var = StringVar()
    search_query = StringVar()
    combo3 = ttk.Combobox(search_frame, width=20, values=("Name", "ID", "Category"), font="lucida 12 bold",
                          justify=CENTER,
                          textvariable=search_var, state="readonly")
    combo3.set("Select")
    combo3.pack(side=LEFT, padx=20)

    Entry(search_frame, width=20, font="lucida 12", textvariable=search_query, relief=RIDGE, bd=2).pack(side=LEFT,
                                                                                                        ipady=4,
                                                                                                        padx=20)
    Button(search_frame, text="Search", bg="#155C73", fg="white", font="lucida 12", width=10,
           cursor="hand2").pack(
        side=LEFT, padx=20)
    search_frame.pack(ipady=10)

    product_details_frame = Frame(root2, bd=2, relief=GROOVE)

    scrolly = Scrollbar(product_details_frame, orient=VERTICAL)
    scrollx = Scrollbar(product_details_frame, orient=HORIZONTAL)
    product_tv = ttk.Treeview(product_details_frame, columns=(
        'pid','ctegry', 'splir', "name", "price", "qnty", "status", ), show="headings",
                               yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrollx.config(command=product_tv.xview)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.config(command=product_tv.yview)
    scrolly.pack(side=RIGHT, fill=Y)

    product_tv.heading(column="pid", text="P ID", anchor=CENTER)
    product_tv.heading("ctegry", text="Category", anchor=CENTER)
    product_tv.heading("splir", text="Supplier", anchor=CENTER)
    product_tv.heading("name", text="Name", anchor=CENTER)
    product_tv.heading("price", text="Price", anchor=CENTER)
    product_tv.heading("qnty", text="Quantity", anchor=CENTER)


    product_tv.pack(fill=BOTH, expand=1, side=BOTTOM)
    product_details_frame.pack(fill=BOTH, expand=1, side=BOTTOM)
    # product_tv.bind("<ButtonRelease-1>", get_record_from_tv)
    root2.mainloop()


def Categories():
    def show_records():
        try:
            cursr.execute("SELECT * FROM category ORDER BY cid;")
            records = cursr.fetchall()
            ctegry_tv.delete(*ctegry_tv.get_children())
            for record in records:
                ctegry_tv.insert('', END, text="Aim", values=record)
        except EXCEPTION as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent=root2)

    def get_record_from_tv(event):
        f = ctegry_tv.focus()
        record = (ctegry_tv.item(f))['values']
        if record != "":
            ctegry_name.set(record[1])
            ctegry_id.set(record[0])

    def delete():
        try:
            if ctegry_name.get() == "":
                messagebox.showerror("Error", "Category name must be required", parent=root2)
            else:
                cursr.execute(f"SELECT * FROM `category` where name='{ctegry_name.get()}';")
                row = cursr.fetchone()
                if row is not None:
                    permission = messagebox.askyesno("Confirm", "Are you sure?", parent=root2)
                    if permission:
                        cursr.execute(f"DELETE FROM category WHERE name='{ctegry_name.get()}'")
                        conct.commit()
                        messagebox.showinfo("Deletion", f"Category has been deleted successfully!", parent=root2)
                        show_records()
                        ctegry_name.set("")
                else:
                    messagebox.showerror("Error", "Invalid Category!", parent=root2)
        except Exception as e:
            messagebox.showerror("Error", f"{str(e)}", parent=root2)

    def add():
        try:
            if ctegry_name.get() == "":
                messagebox.showerror("Error", "Category Name must be required", parent=root2)

            else:
                cursr.execute(f"SELECT * FROM `category` where name='{ctegry_name.get()}';")
                row = cursr.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This category name has already be assigned, try different",
                                         parent=root2)
                else:
                    cursr.execute(
                        f"""INSERT INTO `category` (`name`) VALUES ("{ctegry_name.get()}");""")
                    conct.commit()
                    messagebox.showinfo("Success", "Category added successfully", parent=root2)
                    show_records()
        except Exception as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent=root2)

    root2 = Toplevel(root)
    root2.geometry("1100x500+100+100")
    root2.focus_force()
    root2.title("Categories")
    ctegry_name = StringVar()
    ctegry_id = IntVar()
    ctegry_frame = LabelFrame(root2, text="Categories Details", font="goudyoldstyle 10 bold", bd=2, relief=GROOVE,
                              width=150,
                              pady=40)

    Label(ctegry_frame, text="Enter Category Name", font="lucinda 16 bold",

          bg="#23292E", fg="white", anchor="w", padx=2).pack(anchor="nw", fill=X)
    ent = Entry(ctegry_frame, font="lucida 14", bd=2, relief=GROOVE, textvariable=ctegry_name)
    ent.pack(anchor="nw", fill=X, pady=70)

    Button(ctegry_frame, text="Add", command=add, bg="#155C73", fg="white", height=2, width=10, cursor="hand2",
           overrelief=FLAT, ).pack(anchor="nw", pady=20, padx=40)
    Button(ctegry_frame, text="Delete", command=delete, bg="#155C73", fg="white", height=2, width=10, cursor="hand2",
           overrelief=FLAT, ).pack(anchor="nw", pady=20, padx=40)

    ctegry_frame.pack(fill=Y, side=LEFT)

    ctegry_details_frame = Frame(root2, bd=2, relief=GROOVE)

    scrolly = Scrollbar(ctegry_details_frame, orient=VERTICAL)
    scrollx = Scrollbar(ctegry_details_frame, orient=HORIZONTAL)
    ctegry_tv = ttk.Treeview(ctegry_details_frame, columns=(
        'cid', "name",), show="headings",
                             yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrollx.config(command=ctegry_tv.xview)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.config(command=ctegry_tv.yview)
    scrolly.pack(side=RIGHT, fill=Y)

    ctegry_tv.heading(column="cid", text="C ID", anchor=CENTER)
    ctegry_tv.heading("name", text="Name", anchor=CENTER)

    ctegry_tv.pack(fill=BOTH, expand=1, side=BOTTOM)
    ctegry_details_frame.pack(fill=BOTH, expand=1, side=BOTTOM)
    ctegry_tv.bind("<ButtonRelease-1>", get_record_from_tv)
    show_records()
    root2.mainloop()


def Supplier():
    def show_records():
        try:
            cursr.execute("SELECT * FROM supplier ORDER BY invoice;")
            records = cursr.fetchall()
            supplier_tv.delete(*supplier_tv.get_children())
            for record in records:
                supplier_tv.insert('', END, text="GAME", values=record)
        except EXCEPTION as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent=root2)

    def add():
        try:
            if All_strings_var[0].get() == "":
                messagebox.showerror("Error", "Invoice must be required", parent=root2)

            elif All_strings_var[0].get().isnumeric():
                cursr.execute(f"SELECT * FROM `supplier` where invoice={All_strings_var[0].get()};")
                row = cursr.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Invoice no. has already be assigned, try different",
                                         parent=root2)
                else:
                    cursr.execute(
                        f"""INSERT INTO `supplier` (`invoice`, `name`, `contact`, `desc`) VALUES ("{All_strings_var[0].get()}", "{All_strings_var[1].get()}", "{All_strings_var[2].get()}", "{desc_area.get(str(1.0), END)}");""")
                    conct.commit()
                    messagebox.showinfo("Success", "Supplier Added successfully", parent=root2)
                    show_records()
            else:
                messagebox.showerror("Error", "Invoice must be integer", parent=root2)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent=root2)

    def get_record_from_tv(event):
        f = supplier_tv.focus()
        record = (supplier_tv.item(f))['values']
        print(record)
        if record != "":
            desc_area.delete("1.0", END)
            desc_area.insert(END, record[3])
            t = 0
            for i in range(len(record) - 1):
                All_strings_var[t].set(record[i])
                t += 1

    def clear():
        desc_area.delete('1.0', END)
        for v in All_strings_var:
            v.set("")

        show_records()
        search_query.set("")
        search_var.set("Select")

    def delete():
        try:
            if All_strings_var[0].get() == "":
                messagebox.showerror("Error", "Supplier Invoice must be required", parent=root2)
            if All_strings_var[0].get().isnumeric():
                cursr.execute(f"SELECT * FROM `supplier` where invoice={All_strings_var[0].get()};")
                row = cursr.fetchone()
                if row is not None:
                    permission = messagebox.askyesno("Confirm", "Are you sure?", parent=root2)
                    if permission:
                        cursr.execute(f"DELETE FROM supplier WHERE invoice={All_strings_var[0].get()}")
                        conct.commit()
                        messagebox.showinfo("Deletion", f"Supplier has been deleted successfully!", parent=root2)
                        show_records()
                        clear()
                else:
                    messagebox.showerror("Error", "Invalid Invoice!", parent=root2)
        except Exception as e:
            messagebox.showerror("Error", f"{str(e)}", parent=root2)

    def edit():
        try:
            if All_strings_var[0].get() == "":
                messagebox.showerror("Error", "Invoice must be unique", parent=root2)
            elif All_strings_var[0].get().isnumeric():
                cursr.execute(f"SELECT * FROM `supplier` where invoice={All_strings_var[0].get()};")
                row = cursr.fetchone()
                print(row)
                if row is None:
                    messagebox.showerror("Error", "Invalid Invoice!", parent=root2)
                else:
                    cursr.execute(
                        f"UPDATE `supplier` SET `name`='{All_strings_var[1].get()}',`contact`='{All_strings_var[2].get()}', `desc`='{desc_area.get(str(1.0), END)}' WHERE invoice={All_strings_var[0].get()}")
                    conct.commit()
                    messagebox.showinfo("Success", "Supplier updated successfully", parent=root2)
                    show_records()
            else:
                messagebox.showerror("Error", "Invoice must be integer", parent=root2)
        except Exception as e:
            messagebox.showerror("Error", f"Error due to : {str(e)}", parent=root2)

    def search():
        if search_var.get() == "Select":
            messagebox.showinfo("Error", "Search by the search option", parent=root2)
        elif search_query.get() == "":
            messagebox.showerror("Error", "Search entry must be filled")
        else:
            if search_var.get() != "Invoice":

                cursr.execute(
                    f"SELECT * FROM supplier WHERE {(search_var.get()).lower()} LIKE '%{search_query.get()}%' ORDER  BY invoice;")
            else:
                cursr.execute(
                    f"SELECT * FROM supplier WHERE {(search_var.get()).lower()} LIKE '%{search_query.get()}%' ORDER  BY invoice;")
            rows = cursr.fetchall()
            if len(rows) == 0:
                messagebox.showinfo("Search", "Sorry, No result found!", parent=root2)
            else:
                supplier_tv.delete(*supplier_tv.get_children())
                for row in rows:
                    supplier_tv.insert('', END, values=row)

    root2 = Toplevel(root)
    root2.geometry("1100x500+100+100")
    root2.focus_force()

    # root2 = Toplevel(root)
    # root2.geometry("980x700+240+166")
    root2.title("Supplier Management")
    # root2.focus_force()
    splyr_frame = LabelFrame(root2, text="Supplier Details", font="goudyoldstyle 10 bold", bd=2, relief=GROOVE,
                             pady=40)
    r = 0
    c = 0
    All_strings_var.clear()
    # if len(sAll_strings_var) == 0:
    for txt in ["Invoice No", "Supplier Name", "Contact", "Description"]:
        var = StringVar()
        label(splyr_frame, r, c, text=txt, )

        if r == 3:
            desc_area = Text(splyr_frame, font="goudyoldstyle 10", height=4, width=26, bd=2, relief=GROOVE)
            desc_area.grid(row=r, column=c + 1)
            r += 1
            continue
        All_strings_var.append(var)
        # if r == 3:
        #     entry(employee_frame, r, c + 1, textvariable=var, show="*")
        #     r += 1
        #     continue
        entry(splyr_frame, r, c + 1, textvariable=var)
        r += 1
    Button(splyr_frame, text="Add", command=add, bg="#155C73", fg="white", height=2, width=10, cursor="hand2",
           overrelief=FLAT, ).grid(
        row=9,
        column=0,
        pady=4)
    Button(splyr_frame, text="Edit", command=edit, bg="#734B66", fg="white", height=2, width=10, cursor="hand2",
           overrelief=FLAT, ).grid(row=9,
                                   column=1,
                                   pady=4)
    Button(splyr_frame, text="Delete", command=delete, bg="#474B73", fg="white", height=2, width=10, cursor="hand2",
           overrelief=SOLID, ).grid(row=10,
                                    column=0,
                                    pady=4)
    Button(splyr_frame, text="Clear", command=clear, bg="#733823", fg="white", height=2, width=10, overrelief=SOLID,
           cursor="hand2").grid(row=10,
                                column=1,
                                pady=4)
    splyr_frame.pack(side=LEFT, fill=Y, padx=2, pady=2)

    search_frame = LabelFrame(root2, text="Search Customer", font="goudyoldstyle 10 bold")
    search_var = StringVar()
    search_query = StringVar()
    combo3 = ttk.Combobox(search_frame, width=20, values=("Invoice", "Name"), font="lucida 12 bold",
                          justify=CENTER,
                          textvariable=search_var, state="readonly")
    combo3.set("Select")
    combo3.pack(side=LEFT, padx=20)

    Entry(search_frame, width=20, font="lucida 12", textvariable=search_query, relief=RIDGE, bd=2).pack(side=LEFT,
                                                                                                        ipady=4,
                                                                                                        padx=20)
    Button(search_frame, text="Search", command=search, bg="#155C73", fg="white", font="lucida 12", width=10,
           cursor="hand2").pack(
        side=LEFT, padx=20)
    search_frame.pack(ipady=10)

    supplier_details_frame = Frame(root2, bd=2, relief=GROOVE)

    scrolly = Scrollbar(supplier_details_frame, orient=VERTICAL)
    scrollx = Scrollbar(supplier_details_frame, orient=HORIZONTAL)
    supplier_tv = ttk.Treeview(supplier_details_frame, columns=(
        'invoice', "name", "contact", "desc"), show="headings",
                               yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
    scrollx.config(command=supplier_tv.xview)
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.config(command=supplier_tv.yview)
    scrolly.pack(side=RIGHT, fill=Y)

    supplier_tv.heading(column="invoice", text="Invoice", anchor=CENTER)
    supplier_tv.heading("name", text="Name", anchor=CENTER)
    supplier_tv.heading("contact", text="contact", anchor=CENTER)
    supplier_tv.heading("desc", text="Description", anchor=CENTER)

    supplier_tv.pack(fill=BOTH, expand=1, side=BOTTOM)
    supplier_details_frame.pack(fill=BOTH, expand=1, side=BOTTOM)
    supplier_tv.bind("<ButtonRelease-1>", get_record_from_tv)
    show_records()
    root2.mainloop()


def Sales():
    root2 = Toplevel(root)
    root2.geometry("1100x500+100+100")
    root2.focus_force()


#TODO: This is main window
root = Tk()
width = 1000
height = 570
root.geometry("1200x870+30+30")
root.title("Inventory Management System")
All_strings_var = []
conct = sqlite3.connect(database=r'icm.db')
cursr = conct.cursor()

#TODO: This is main meun

menu = Menu(root, )
menu.add_command(label="Employee", command=Customer)
menu.add_command(label="Products", command=Product)
menu.add_command(label="Categories", command=Categories)
menu.add_command(label="Supplier", command=Supplier)
menu.add_command(label="Sales", command=Sales)
menu.add_command(label="Exit", command=root.destroy)
menu.config(bd=2, relief=SUNKEN, bg="#3D3E51", fg="#3D3E51", activebackground="yellow", cursor="hand2", takefocus=YES)
root.config(menu=menu, pady=0)

#TODO: This is main Labels

main_Label = Label(root, text="Inventory Control System", font="timesnewroman 18 bold", bg="#3D3E51", fg="white",
                   anchor="w", padx=10).place(x=0, y=0, relwidth=1, height=60)
logout = Button(root, text="Logout", fg="white", bg="black", relief=GROOVE, width=10,
                font='timesnewroman 12 bold').place(x=880, y=8, height=40)
clock_Label = Label(root, text="Welcome to Inventory Control System\t\t      Date: DD-MM-YYYY\t\tTime: HH:MM:SS",
                    font="timesnewroman 10", bg="#546276", fg="white", )
clock_Label.place(x=0, y=60, relwidth=1, )

N_Employess = Label(root, text="Total Employees\n[ 0 ]", font="timesnewroman 10 bold", bg="#53A2D3", bd=2,
                    relief=GROOVE)
N_Employess.place(x=250, y=100, height=130, width=190)
N_supplier = Label(root, text="Total Supplier\n[ 0 ]", font="timesnewroman 10 bold", bg="#53A2D3", bd=2, relief=GROOVE)
N_supplier.place(x=450, y=100, height=130, width=190)
N_products = Label(root, text="Total Products\n[ 0 ]", font="timesnewroman 10 bold", bg="#53A2D3", bd=2, relief=GROOVE)
N_products.place(x=650, y=100, height=130, width=190)
N_Catogories = Label(root, text="Total Categories\n[ 0 ]", font="timesnewroman 10 bold", bg="#53A2D3", bd=2,
                     relief=GROOVE)
N_Catogories.place(x=250, y=250, height=130, width=190)
N_sales = Label(root, text="Total Sales\n[ 0 ]", font="timesnewroman 10 bold", bg="#53A2D3", bd=2, relief=GROOVE)
N_sales.place(x=450, y=250, height=130, width=190)
Label(root, text="ICM - Inventory Control System | Developed by CodingVenue\n"
                 "Contact us at codingvenue@gmail.com",
      font="timesnewroman 8 italic", bg="#546276", fg="white", ).pack(side=BOTTOM, fill=X)

root.mainloop()
