def isbn(conn, isbn):
    print(isbn)
    curr = conn.cursor()
    curr.execute("""
        SELECT *
        FROM book_info LEFT OUTER JOIN storage USING (ISBN)
        WHERE ISBN = %s;
    """, (isbn,))
    books = curr.fetchall()
    print(books)
    for book in books:
        print(book)
    curr.close()

def title(conn, title):
    pass
