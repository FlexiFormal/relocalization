--# -path=../magma:../lexica:../other:../formulae

concrete MonoidLexiconEng of MonoidLexicon = SigFtmlEng ** open SigConstructorsEng, ParadigmsEng, ConstructorsEng in {
  oper
    'monoid:N' = mkN "monoid";
    'commutative:A' = mkA "commutative";
    'invertible:A' = mkA "invertible";
    'matrix:N' = mkN "matrix" "matrices";

  lin
    'verb_monoid:N_Kind' = mkKind (makeCN 'monoid:N') ;
    'verb_commutative:A-monoid:N_Kind' = mkKind (makeCN 'commutative:A' 'monoid:N') ;
    'verb_invertible:A_Property' = mkProperty (mkAP 'invertible:A') ;
}
