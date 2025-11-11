abstract RglXml = Grammar, Xml ** {
    oper
        TagT : Type = {s: Str};
    fun
        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html

        WRAP_A : TagT -> A -> A;
        WRAP_A2 : TagT -> A2 -> A2;
        WRAP_ACard : TagT -> ACard -> ACard;

        WRAP_AP : TagT -> AP -> AP;
        WRAP_AdA : TagT -> AdA -> AdA;
        WRAP_AdN : TagT -> AdN -> AdN;
        WRAP_AdV : TagT -> AdV -> AdV;
        WRAP_Adv : TagT -> Adv -> Adv;

        WRAP_Ant : TagT -> Ant -> Ant;
        WRAP_CAdv : TagT -> CAdv -> CAdv;
        WRAP_CN : TagT -> CN -> CN;
        WRAP_Card : TagT -> Card -> Card;
        WRAP_Cl : TagT -> Cl -> Cl;
                
        WRAP_ClSlash : TagT -> ClSlash -> ClSlash;
        WRAP_Comp : TagT -> Comp -> Comp;
        WRAP_Conj : TagT -> Conj -> Conj;
        WRAP_DAP : TagT -> DAP -> DAP;
        WRAP_Det : TagT -> Det -> Det;
                        
        WRAP_Dig : TagT -> Dig -> Dig;
        WRAP_Digits : TagT -> Digits -> Digits;
        WRAP_IAdv : TagT -> IAdv -> IAdv;
        WRAP_IComp : TagT -> IComp -> IComp;
        WRAP_IDet : TagT -> IDet -> IDet;
                        
        WRAP_IP : TagT -> IP -> IP;
        WRAP_IQuant : TagT -> IQuant -> IQuant;
        WRAP_Imp : TagT -> Imp -> Imp;
        -- WRAP_ImpForm : TagT -> ImpForm -> ImpForm;
        WRAP_Interj : TagT -> Interj -> Interj;

        WRAP_ListAP : TagT -> ListAP -> ListAP;
        WRAP_ListAdv : TagT -> ListAdv -> ListAdv;
        WRAP_ListNP : TagT -> ListNP -> ListNP;
        WRAP_ListRS : TagT -> ListRS -> ListRS;
        WRAP_ListS : TagT -> ListS -> ListS;

        WRAP_N : TagT -> N -> N;
        WRAP_N2 : TagT -> N2 -> N2;
        WRAP_N3 : TagT -> N3 -> N3;
        WRAP_NP : TagT -> NP -> NP;
        -- WRAP_Num : TagT -> Num -> Num;

        WRAP_Numeral : TagT -> Numeral -> Numeral;
        WRAP_Ord : TagT -> Ord -> Ord;
        WRAP_PConj : TagT -> PConj -> PConj;
        WRAP_PN : TagT -> PN -> PN;
        WRAP_Phr : TagT -> Phr -> Phr;

        WRAP_Pol : TagT -> Pol -> Pol;
        WRAP_Predet : TagT -> Predet -> Predet;
        WRAP_Prep : TagT -> Prep -> Prep;
        WRAP_Pron : TagT -> Pron -> Pron;
        -- WRAP_Punct : TagT -> Punct -> Punct;

        WRAP_QCl : TagT -> QCl -> QCl;
        WRAP_QS : TagT -> QS -> QS;
        WRAP_RCl : TagT -> RCl -> RCl;
        WRAP_RP : TagT -> RP -> RP;
        WRAP_RS : TagT -> RS -> RS;

        WRAP_S : TagT -> S -> S;
        WRAP_SC : TagT -> SC -> SC;
        WRAP_SSlash : TagT -> SSlash -> SSlash;
        WRAP_Sub100 : TagT -> Sub100 -> Sub100;
        WRAP_Sub1000 : TagT -> Sub1000 -> Sub1000;

        WRAP_Subj : TagT -> Subj -> Subj;
        WRAP_Temp : TagT -> Temp -> Temp;
        WRAP_Tense : TagT -> Tense -> Tense;
        WRAP_Text : TagT -> Text -> Text;
        -- WRAP_Unit : TagT -> Unit -> Unit;

        WRAP_Utt : TagT -> Utt -> Utt;
        WRAP_V : TagT -> V -> V;
        WRAP_V2 : TagT -> V2 -> V2;
        WRAP_V2A : TagT -> V2A -> V2A;
        WRAP_V2Q : TagT -> V2Q -> V2Q;

        WRAP_V2S : TagT -> V2S -> V2S;
        WRAP_V2V : TagT -> V2V -> V2V;
        WRAP_V3 : TagT -> V3 -> V3;
        WRAP_VA : TagT -> VA -> VA;
        WRAP_VP : TagT -> VP -> VP;

        WRAP_VPSlash : TagT -> VPSlash -> VPSlash;
        WRAP_VQ : TagT -> VQ -> VQ;
        WRAP_VS : TagT -> VS -> VS;
        WRAP_VV : TagT -> VV -> VV;
        WRAP_Voc : TagT -> Voc -> Voc;
}
