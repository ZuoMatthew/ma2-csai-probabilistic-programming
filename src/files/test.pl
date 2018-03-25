0.2::msw(locus1,'A'); 0.8::msw(locus1,a).
0.3::msw(locus2,b).
genotype(locus1,'A',a) :- msw(locus1,'A'), msw(locus1,a).
genotype(locus1,'A','A') :- msw(locus1,'A').
genotype(locus2,b,b) :- msw(locus2,b).
genotype(locus1,a,'A') :- msw(locus1,a), msw(locus1,'A').
bloodtype(a) :- genotype(locus1,'A','A'), genotype(locus2,b,b).
bloodtype(a) :- genotype(locus1,'A',a), genotype(locus2,b,b).
bloodtype(a) :- genotype(locus1,a,'A'), genotype(locus2,b,b).
query(bloodtype(a)).