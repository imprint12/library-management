def create_tables(curr):
    curr.execute("""
        CREATE TABLE employee(
            username TEXT PRIMARY KEY,
            true_name TEXT,
            id INTEGER,
            age INTEGER,
            gender CHAR
        );

        CREATE TABLE admin(
            username TEXT PRIMARY KEY,
            true_name TEXT,
            id INTEGER,
            age INTEGER,
            gender CHAR
        )
    """)

    curr.execute("""
        CREATE TABLE book_info(
            ISBN VARCHAR(20) PRIMARY KEY ,
            title TEXT,
            writer TEXT[],
            publisher TEXT
        )
    """)

#    curr.execute("""
#        CREATE TABLE writes(
#            ISBN VARCHAR REFERENCES book_info ,
#            writer VARCHAR(50),
#            PRIMARY KEY(ISBN, writer)
#        )
#    """)

    curr.execute("""
        CREATE TABLE storage(
            ISBN VARCHAR(20) PRIMARY KEY REFERENCES book_info,
            price NUMERIC(8, 2),
            num INTEGER
    )
    """)

    curr.execute("""
        CREATE TABLE restock_order(
            order_no INTEGER PRIMARY KEY,
            ISBN VARCHAR(20) REFERENCES book_info,
            num INTEGER,
            total_price NUMERIC(12, 2),
            state VARCHAR(10),
            username TEXT REFERENCES employee
    )
    """)

    curr.execute("""
        CREATE TABLE payment_bill(
            bill_no INTEGER PRIMARY KEY,
            dt TIMESTAMP,
            total_price NUMERIC(12, 2),
            username TEXT REFERENCES employee
    )
    """)

    curr.execute("""
        CREATE TABLE revenue_bill(
            bill_no INTEGER PRIMARY KEY,
            dt TIMESTAMP,
            total_price NUMERIC(12, 2),
            username TEXT REFERENCES employee
    )
    """)

    curr.execute("""
        CREATE TABLE revenue_storage(
            bill_no INTEGER PRIMARY KEY REFERENCES revenue_storage,
            ISBN VARCHAR(20) REFERENCES book_info,
            num INTEGER
        )
    """)

    curr.execute("""
        CREATE TABLE restock_pay(
            order_no INTEGER PRIMARY KEY REFERENCES restock_order,
            bill_no INTEGER REFERENCES payment_bill
        )
    """)


def create_auth(curr):
    curr.execute("""
        CREATE ROLE employee;
        CREATE ROLE admin;
    """)

    curr.execute("GRANT ALL PRIVILEGES ON DATABASE library TO admin;")
    curr.execute("GRANT ALL ON ALL TABLES IN SCHEMA public TO admin;")

    curr.execute("""
        CREATE POLICY lib_update_policy ON employee FOR UPDATE TO employee
        USING (current_user = username);
        CREATE POLICY lib_select_policy ON employee FOR SELECT TO employee
        USING (current_user = username);
    """)

#    curr.execute("""
#        CREATE POLICY library_policy ON librarian FOR SELECT TO employee
#        USING (current_user = username)
#    """)

    curr.execute("""
        GRANT SELECT, UPDATE ON employee TO employee;
        GRANT ALL ON book_info TO employee;
        GRANT ALL ON storage TO employee;
        GRANT ALL ON restock_order TO employee;
        GRANT ALL ON revenue_bill TO employee;

        GRANT INSERT, SELECT ON restock_pay TO employee;
        GRANT INSERT, SELECT ON revenue_storage TO employee;
    """)
