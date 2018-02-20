0.5::similar(ale,stout).
0.25::similar(ale,gin).
0.2::similar(ale,soda) :- similar(ale,stout), similar(ale,gin).
query(similar(ale,stout)).
query(similar(ale,gin)).
query(similar(ale,soda)).
