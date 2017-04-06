def create_book(curr):
    curr.execute("""
    CREATE TABLE book(
        ISBN VARCHAR(20) PRIMARY KEY ,
        title VARCHAR(50),
        writer VARCHAR(50),
        publisher VARCHAR(50)
    )
    """)


def create_on_shelf_book(curr):
    curr.execute("""
        CREATE TABLE on_shelf_book(
            ISBN VARCHAR(20) PRIMARY KEY REFERENCES book,
            price NUMERIC(8, 2),
            number INTEGER
        )
        """)


def create_restore(curr):
    curr.execute("""
        CREATE TABLE restore(
            ISBN VARCHAR(20) PRIMARY KEY REFERENCES book,
            number INTEGER,
            total_price NUMERIC(12, 2)
    )    
    """)


def create_payment_bill(curr):
    curr.execute("""
            CREATE TABLE payment_bill(
                no INTEGER PRIMARY KEY ,
                date TIMESTAMP,
                total_price NUMERIC(12, 2),
                paid BOOLEAN
        )    
        """)


def create_collection_bill(curr):
    curr.execute("""
            CREATE TABLE collection_bill(
                no INTEGER PRIMARY KEY ,
                date TIMESTAMP,
                total_price NUMERIC(12, 2)
        )    
        """)


def create_storage(curr):
    curr.execute("""
        CREATE TABLE storage(
            ISBN VARCHAR(20) PRIMARY KEY REFERENCES book,
            number INTEGER
        )
    """)
