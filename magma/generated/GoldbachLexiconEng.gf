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

  lin
    'verb_#1-even:A_Property' = mkProperty (mkAP 'even:A') ;
    'verb_#1-integer:N_Kind' = mkKind (makeCN 'integer:N') ;
    'verb_#1-greater:A-than-#2_Property2' = mkProperty2 (mkAP 'greater:A') than_Prep;
    'verb_sum:N-of-#1_FKind2' = mkFKind2 (makeCN 'sum:N') of_Prep;
    'verb_#1-prime:N_Kind' = mkKind (makeCN 'prime:N') ;
    'verb_#1-prime:A-number:N_Kind' = mkKind (makeCN 'prime:A' 'number:N') ;
}
