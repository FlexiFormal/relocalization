--# -path=../magma:../lexica:../other:../formulae

abstract AutomataGrammar = SigFtml ** {
  fun
    'http://mathhub.info?a=smglom/automata&p=mod&m=auto-reachable/EXTSTRUCT_1&s=steprelation__verb0' : FKind;
    'http://mathhub.info?a=smglom/sets&p=mod&m=relation&s=relationon__verb0' : Kind2;
    'http://mathhub.info?a=smglom/sets&p=mod&m=transitive-closure&s=reflexivetransitiveclosure__verb0' : FKind2;
    'http://mathhub.info?a=smglom/automata&p=mod&m=auto-reachable/EXTSTRUCT_1&s=reachabilityrelation__verb0' : FKind;
    smallest__verb0 : Property;
    binary__verb0 : Property;
}
