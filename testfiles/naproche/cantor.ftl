Definition (defempty):
  for all v0, ((v0 is equal to the empty set) iff (v0 is a set and it is wrong that for some v1, (v1 is an element of v0)))

Definition (defsub):
  for all v0, (if v0 is a class then for all v1, ((v1 is a subclass of v0) iff (v1 is a class and for all v2, (if v2 is an element of v1 then v2 is an element of v0))))

Theorem (extensionality):
  for all v0, (for all v1, (if v0 is a class and v1 is a class then (if v0 is a subclass of v1 and v1 is a subclass of v0 then v0 is equal to v1)))
Proof:
Qed.

Definition (subset):
  for all v0, (if v0 is a class then for all v1, ((v1 is a subset of v0) iff (v1 is a set and v1 is a subclass of v0)))

Axiom (separation):
  for all v0, (if v0 is a set then for all v1, (if v1 is a subclass of v0 then v1 is a set))

Definition:
  for all v0, (for all v1, (if v0 is a class and v1 is a class then for all v2, ((v2 is equal to the intersection of v0 and v1) iff (v2 is a class and (if v0 is a set then v2 is a set) and for all v3, (v3 is an element of v2 iff (v3 is an element of v0 and v3 is an object and v3 is an element of v1))))))

Definition:
  for all v0, (for all v1, (if v0 is a class and v1 is a class then for all v2, ((v2 is equal to the union of v0 and v1) iff (v2 is a class and for all v3, (v3 is an element of v2 iff (v3 is an object and (v3 is an element of v0 or v3 is an element of v1)))))))

Definition:
  for all v0, (for all v1, (if v0 is a class and v1 is a class then for all v2, ((v2 is equal to the set difference of v0 and v1) iff (v2 is a class and (if v0 is a set then v2 is a set) and for all v3, (v3 is an element of v2 iff (v3 is an element of v0 and v3 is an object and it is wrong that v3 is an element of v1))))))

Definition:
  for all v0, (for all v1, (if v0 is a class and v1 is a class then ((v0 is disjoint from v1) iff it is wrong that for some v2, (v2 is an element of v0 and v2 is an element of v1))))

Definition:
  for all v0, ((v0 is a family) iff (v0 is a set and for all v1, (if v1 is an element of v0 then v1 is a set)))

Definition:
  for all v0, ((v0 is a disjoint family) iff (v0 is a family and for all v1, (for all v2, (if v1 is an element of v0 and v2 is an element of v0 and it is wrong that v1 is equal to v2 then v1 is disjoint from v2))))

Axiom:
  for all v0, (for all v1, (for all v2, (for all v3, (if v0 is an object and v1 is an object and v2 is an object and v3 is an object then (if the ordered pair of v0 and v1 is equal to the ordered pair of v2 and v3 then (v0 is equal to v2 and v1 is equal to v3))))))

Definition:
  for all v0, (for all v1, (if v0 is a class and v1 is a class then for all v2, ((v2 is equal to v0 \times v1) iff (v2 is a class and for all v3, (v3 is an element of v2 iff (v3 is an object and for some v4, (for some v5, (v4 is an element of v0 and v5 is an element of v1 and v3 is equal to the ordered pair of v4 and v5))))))))

Axiom:
  for all v0, (for all v1, (if v0 is a set and v1 is a set then v0 \times v1 is a set))

Theorem:
  for all v0, (for all v1, (if v0 is an object and v1 is an object then for all v2, (for all v3, (if v2 is a class and v3 is a class then (if the ordered pair of v0 and v1 is an element of v2 \times v3 then (v0 is an element of v2 and v1 is an element of v3))))))
Proof:
Qed.

Axiom:
  for all v0, (if v0 is a map then (if the domain of v0 is a set and for all v1, (if v1 is an element of the domain of v0 then the value of v0 under v1 is an object) then v0 is a function))

Definition:
  for all v0, (if v0 is a map then for all v1, (if v1 is a subclass of the domain of v0 then for all v2, ((v2 is equal to v0 [ v1 ]) iff (v2 is a class and for all v3, (v3 is an element of v2 iff (v3 is an object and for some v4, (v4 is an element of v1 and v3 is equal to the value of v0 under v4)))))))

Definition:
  for all v0, (for all v1, (for all v2, (if v0 is a class and v1 is a class and v2 is a map then ((v2 maps elements of v0 to elements of v1) iff (the domain of v2 is equal to v0 and v2 [ v0 ] is a subclass of v1)))))

Axiom (replacement):
  for all v0, (if v0 is a map then for all v1, (if v1 is a subset of the domain of v0 then v0 [ v1 ] is a set))

Definition:
  for all v0, (for all v1, (for all v2, (if v0 is a class and v1 is a class and v2 is a map then ((v2 : v0 \leftrightarrow v1) iff (v2 maps elements of v0 to elements of v1 and for some v3, (v3 is a map and v3 maps elements of v1 to elements of v0 and for all v4, (if v4 is an element of the domain of v2 then the value of v3 under the value of v2 under v4 is equal to v4) and for all v4, (if v4 is an element of the domain of v3 then the value of v2 under the value of v3 under v4 is equal to v4)))))))

Definition:
  for all v0, (if v0 is a set then for all v1, ((v1 is a function of v0) iff (v1 is a function and the domain of v1 is equal to v0)))

Definition:
  for all v0, (for all v1, (if v1 is a function and v0 is a set then ((v1 surjects onto v0) iff (v0 is a class and for all v2, (v2 is an element of v0 iff (v2 is an object and for some v3, (v3 is an element of the domain of v1 and v2 is equal to the value of v1 under v3)))))))

Definition:
  for all v0, (for all v1, (if v0 is a set and v1 is a set then for all v2, ((v2 is a function from v0 onto v1) iff (v2 is a function of v0 and v2 surjects onto v1))))

Definition:
  for all v0, (if v0 is a set then for all v1, ((v1 is equal to the powerset of v0) iff (v1 is a class and for all v2, (v2 is an element of v1 iff (v2 is a subset of v0 and v2 is an object)))))

Axiom:
  for all v0, (if v0 is a set then the powerset of v0 is a set)

Theorem (cantor):
  for all v0, (if v0 is a set then for all v1, (if v1 is a function of v0 then it is wrong that v1 surjects onto the powerset of v0))
Proof:
  it is wrong that the thesis holds
  f is a function from M onto the powerset of M
  for all v0, (if v0 is an element of M then the value of f under v0 is a set)
  N is a class and (if M is a set then N is a set) and for all v0, (v0 is an element of N iff (v0 is an element of M and v0 is an object and it is wrong that v0 is an element of the value of f under v0))
  N is a subset of M
  z is an element of M and the value of f under z is equal to N
  z is an element of N iff (it is wrong that z is an element of the value of f under z and the value of f under z is equal to N)
  falsity holds
Qed.

