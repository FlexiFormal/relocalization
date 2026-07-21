--# -path=../magma:../lexica:../other:../formulae

abstract MonoidLexicon = SigFtml ** {
  fun
    'verb_monoid:N_Kind' : Kind;
    'verb_commutative:A-monoid:N_Kind' : Kind;
    'verb_invertible:A_Property' : Property;
}
