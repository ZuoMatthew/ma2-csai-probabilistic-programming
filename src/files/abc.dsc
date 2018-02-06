belief network "unknown"
node A {
  type : discrete [ 2 ] = { "a1", "a2" };
}
node B {
  type : discrete [ 2 ] = { "b1", "b2" };
}
node C {
  type : discrete [ 3 ] = { "c1", "c2", "c3" };
}

probability ( A ) {
   0.1, 0.9;
}

probability ( B | A ) {
  (0) : 0.1, 0.9;
  (1) : 0.2, 0.8;
}
probability ( C | A ) {
  (0) : 0.1, 0.2, 0.7;
  (1) : 0.01, 0.09, 0.9;
}