--# -path=../magma:../lexica:../other:../formulae

concrete AutomataGrammarEng of AutomataGrammar = SigFtmlEng ** open SigConstructorsEng, ParadigmsEng, ConstructorsEng in {
  oper
    _dict_step_N = mkN "step";
    _dict_relation_N = mkN "relation";
    _dict_reflexive_A = mkA "reflexive";
    _dict_transitive_A = mkA "transitive";
    _dict_closure_N = mkN "closure";
    _dict_reachability_N = mkN "reachability";
    _dict_small_A = mkA "small";
    _dict_binary_A = mkA "binary";

  lin
    'http://mathhub.info?a=smglom/automata&p=mod&m=auto-reachable/EXTSTRUCT_1&s=steprelation__verb0' = mkFKind (makeCN _dict_step_N _dict_relation_N) ;
    'http://mathhub.info?a=smglom/sets&p=mod&m=relation&s=relationon__verb0' = mkKind2 (makeCN _dict_relation_N) on_Prep;
    'http://mathhub.info?a=smglom/sets&p=mod&m=transitive-closure&s=reflexivetransitiveclosure__verb0' = mkFKind2 (makeCN _dict_reflexive_A _dict_transitive_A _dict_closure_N) of_Prep;
    'http://mathhub.info?a=smglom/automata&p=mod&m=auto-reachable/EXTSTRUCT_1&s=reachabilityrelation__verb0' = mkFKind (makeCN _dict_reachability_N _dict_relation_N) ;
    smallest__verb0 = mkProperty (mkAP ( superlative _dict_small_A )) ;
    binary__verb0 = mkProperty (mkAP _dict_binary_A) ;
}
