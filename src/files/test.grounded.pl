0.3::msw(locus2,b); 7/10::msw(locus2,'B').
0.8::msw(locus1,a); 0.2::msw(locus1,'A').
genotype(locus1,a,a) :- msw(locus1,a).
genotype(locus2,b,b) :- msw(locus2,b).
bloodtype(o) :- genotype(locus1,a,a), genotype(locus2,b,b).
genotype(locus1,'A',a) :- msw(locus1,'A'), msw(locus1,a).
genotype(locus1,'A','A') :- msw(locus1,'A').
genotype(locus1,a,'A') :- msw(locus1,a), msw(locus1,'A').
genotype(locus2,'B',b) :- msw(locus2,'B'), msw(locus2,b).
genotype(locus2,'B','B') :- msw(locus2,'B').
genotype(locus2,b,'B') :- msw(locus2,b), msw(locus2,'B').
bloodtype(a) :- genotype(locus1,'A','A'), genotype(locus2,b,b).
bloodtype(a) :- genotype(locus1,'A',a), genotype(locus2,b,b).
bloodtype(a) :- genotype(locus1,a,'A'), genotype(locus2,b,b).
bloodtype(b) :- genotype(locus1,a,a), genotype(locus2,'B','B').
bloodtype(b) :- genotype(locus1,a,a), genotype(locus2,'B',b).
bloodtype(b) :- genotype(locus1,a,a), genotype(locus2,b,'B').
bloodtype(ab) :- \+bloodtype(o), \+bloodtype(a), \+bloodtype(b).
query(bloodtype(o)).
query(bloodtype(a)).
query(bloodtype(b)).
query(bloodtype(ab)).
