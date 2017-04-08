## Entities:

librarian(**username**, true_name, id, age, gender)

book_info(**ISBN**, title, writer, publisher)

storage(**ISBN**, number, price)


restock_order(**order_no**, ISBN, number, state, username)

### bill:
  payment_bill(**bill_no**, date, total_price, username)
  revenue_bill(**bill_no**, date, total_price, username)


## Relationship:

restock_pay(**order_no**, bill_no)
revenue_storage(**bill_no**, ISBN, number)
