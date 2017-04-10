def create_tables(curr):
    curr.execute("""
        CREATE TABLE librarian(
            username VARCHAR(30) PRIMARY KEY,
            true_name VARCHAR(50),
            id INTEGER,
            age INTEGER,
            gender CHAR
    )
    """)

    curr.execute("""
    CREATE TABLE book_info(
        ISBN VARCHAR(20) PRIMARY KEY ,
        title VARCHAR(50),
        writer VARCHAR(50),
        publisher VARCHAR(50)
    )
    """)

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
            username VARCHAR(30) REFERENCES librarian
    )
    """)

    curr.execute("""
        CREATE TABLE payment_bill(
            bill_no INTEGER PRIMARY KEY,
            dt TIMESTAMP,
            total_price NUMERIC(12, 2),
            username VARCHAR(30) REFERENCES librarian
    )
    """)

    curr.execute("""
        CREATE TABLE collection_bill(
            bill_no INTEGER PRIMARY KEY,
            dt TIMESTAMP,
            total_price NUMERIC(12, 2),
            username VARCHAR(30) REFERENCES librarian
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
