# getfinance_test


Use _sqliteman_ to inspect the test db.

A more complex model would involve the creation of a costs table (if the cost
depends on the destination bank)

Add transfer costs as db triggers

Storing transfers implies storing foreign accounts and movements in every bank,
so we will only store movements themselves.