Entities:

librarian(username, age, gender)

book_info(ISBN, title, writer, publisher)

storage(ISBN, number)

restock_order(order_no, ISBN, number, arrived)

bill:
  payment_bill(bill_no, date, total_price, paid)
  revenue_bill(bill_no, date, total_price)


relationship:
pay_restock(order_no, bill_no, ISBN, number)
revenue_book(bill_no, ISBN, number)
