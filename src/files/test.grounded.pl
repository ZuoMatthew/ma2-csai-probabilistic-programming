win_keep :- prize(1).
open_door(2) :- \+prize(2), prize(3).
open_door(3) :- \+prize(3), prize(2).
win_switch :- prize(2), \+open_door(2).
win_switch :- prize(3), \+open_door(3).
query(prize(1)).
query(prize(2)).
query(prize(3)).
select_door(1).
query(select_door(1)).
query(win_keep).
query(win_switch).
