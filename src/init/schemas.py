

def create_book(curr):
    curr.execute("""
    CREATE TABLE book(
        ISBN varchar(20),
        title varchar(50),
        writer varchar(50),
        publisher varchar(50)
    )
    """)


def create_on_shelf_book(curr):
    curr.execute("""
        CREATE TABLE on_shelf_book(
            ISBN varchar(20) REFERENCES book,
            price NUMERIC(8,2),
            number INTEGER
        )
        """)
