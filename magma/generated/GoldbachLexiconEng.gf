--# -path=../magma:../lexica:../other:../formulae

concrete GoldbachLexiconEng of GoldbachLexicon = SigFtmlEng ** open SigConstructorsEng, ParadigmsEng, ConstructorsEng in {
  oper
    'even:A' = mkA "even";
    'integer:N' = mkN "integer";
    'greater:A' = mkA "greater";
    'sum:N' = mkN "sum";
    'prime:N' = mkN "prime";
    'prime:A' = mkA "prime";
    'number:N' = mkN "number";
    'divisible:A' = mkA "divisible";
    'matrix:N' = mkN "matrix" "matrices";

  lin
    'verb_even:A_Property' = mkProperty (mkAP 'even:A') ;
    'verb_integer:N_Kind' = mkKind (makeCN 'integer:N') ;
    'verb_greater:A-than-#2_Property2' = mkProperty2 (mkAP 'greater:A') than_Prep;
    'verb_sum:N-of-#1_FKind2' = mkFKind2 (makeCN 'sum:N') of_Prep;
    'verb_prime:N_Kind' = mkKind (makeCN 'prime:N') ;
    'verb_prime:A-number:N_Kind' = mkKind (makeCN 'prime:A' 'number:N') ;
    'verb_divisible:A-by-#2_Property2' = mkProperty2 (mkAP 'divisible:A') by_Prep;
}
