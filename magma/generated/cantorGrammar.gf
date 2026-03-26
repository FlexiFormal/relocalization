--# -path=../magma:../lexica:../other

abstract cantorGrammar = Forthel ** {
  fun
    set__verb0 : Kind;
    eset__verb0 : Kind;
    intersection__verb0 : Kind2;
    union__verb0 : Kind2;
    setdiff__verb0 : Kind2;
    member__verb0 : Kind2;
    family__verb0 : Kind;
    disjfamily__verb0 : Kind;
    orderedpair__verb0 : Kind2;
    class__verb0 : Kind;
    object__verb0 : Kind;
    map__verb0 : Kind;
    function__verb0 : Kind;
    functionof__verb0 : Kind2;
    functionfromonto__verb0 : Kind3;
    valueofunder__verb0 : Kind3;
    domain__verb0 : Kind2;
    subclass__verb0 : Kind2;
    subset__verb0 : Kind2;
    powerset__verb0 : Kind2;
    equal__verb0 : Property2;
    disj__verb0 : Property2;
    mapto__verb0 : Predicate3;
    surjectonto__verb0 : Predicate2;
    cartprod__notation0 : ForthelTerm -> ForthelTerm -> ForthelTerm;
    imgnotation__notation0 : ForthelTerm -> ForthelTerm -> ForthelTerm;
    bijection__notation0 : ForthelTerm -> ForthelTerm -> ForthelTerm -> ForthelStmt;
    v0 : ForthelIdentifier;
    v1 : ForthelIdentifier;
    v2 : ForthelIdentifier;
    v3 : ForthelIdentifier;
    v4 : ForthelIdentifier;
    v5 : ForthelIdentifier;
    f : ForthelIdentifier;
    M : ForthelIdentifier;
    n : ForthelIdentifier;
    N : ForthelIdentifier;
    z : ForthelIdentifier;
}
