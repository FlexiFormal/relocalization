--# -path=../magma:../lexica:../other:../formulae

abstract GoldbachLexicon = SigFtml ** {
  fun
    'verb_#1-even:A_Property' : Property;
    'verb_#1-integer:N_Kind' : Kind;
    'verb_#1-greater:A-than-#2_Property2' : Property2;
    'verb_sum:N-of-#1_FKind2' : FKind2;
    'verb_#1-prime:N_Kind' : Kind;
    'verb_#1-prime:A-number:N_Kind' : Kind;
}
