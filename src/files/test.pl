0.3::a; 0.54::b.
0.4::c; 0.4::d :- a, b.

evidence(b, false).

query(a).
query(c).
query(d).
