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
    _dict_path_N = mkN "path";
    _dict_finite_A = mkA "finite";
    _dict_sequence_N = mkN "sequence";
    _dict_edge_N = mkN "edge";
    _dict_transition_N = mkN "transition";
    _dict_element_N = mkN "element";

  lin
    'http://mathhub.info?a=smglom/automata&p=mod&m=auto-reachable/EXTSTRUCT_1&s=steprelation__verb0' = mkFKind (makeCN _dict_step_N _dict_relation_N) ;
    'http://mathhub.info?a=smglom/sets&p=mod&m=relation&s=relationon__verb0' = mkKind2 (makeCN _dict_relation_N) on_Prep;
    'http://mathhub.info?a=smglom/sets&p=mod&m=transitive-closure&s=reflexivetransitiveclosure__verb0' = mkFKind2 (makeCN _dict_reflexive_A _dict_transitive_A _dict_closure_N) of_Prep;
    'http://mathhub.info?a=smglom/automata&p=mod&m=auto-reachable/EXTSTRUCT_1&s=reachabilityrelation__verb0' = mkFKind (makeCN _dict_reachability_N _dict_relation_N) ;
    smallest__verb0 = mkProperty (mkAP ( superlative _dict_small_A )) ;
    binary__verb0 = mkProperty (mkAP _dict_binary_A) ;
    'http://mathhub.info?a=Papers/25-CICM-AST&p=mod&m=quiver-path/EXTSTRUCT_1&s=path__verb0' = mkKind (makeCN _dict_path_N) ;
    'http://mathhub.info?a=smglom/sets&p=mod&m=finite-cardinality&s=finite__verb0' = mkProperty (mkAP _dict_finite_A) ;
    'http://mathhub.info?a=smglom/mv&p=mod&m=sequence&s=sequence__verb0' = mkKind2 (makeCN _dict_sequence_N) of_Prep;
    'http://mathhub.info?a=Papers/25-CICM-AST&p=mod&m=quiver/quiver&s=edge__verb0' = mkKind (makeCN _dict_edge_N) ;
    'http://mathhub.info?a=Papers/25-CICM-AST&p=mod&m=nts/non-deterministictransitionsystem&s=transition__verb0' = mkKind (makeCN _dict_transition_N) ;
    'https://mathhub.info?a=smglom/sets&p=mod&m=set&s=element__verb0' = mkKind2 (makeCN _dict_element_N) of_Prep;
}
