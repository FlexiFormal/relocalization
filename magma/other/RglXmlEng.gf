-- Based on https://github.com/10S1/definitionexpansion

concrete RglXmlEng of RglXml = XmlConcr, GrammarEng ** open ResEng, XmlResource in {	    
    lincat
        TagT = _Tag;

    lin
        -- Categories from https://www.grammaticalframework.org/lib/doc/synopsis/index.html
        
        WRAP_A tag x = { 
            s = table { af => wrap tag (x.s ! af) }; 
            isPre = x.isPre; 
            isMost = x.isMost
        };

        WRAP_A2 tag x = { 
            s = table { af => wrap tag (x.s ! af) }; 
            isPre = x.isPre; 
            isMost = x.isMost; 
            c2 = x.c2
        };

        WRAP_ACard tag x = { 
            s = table { c => wrap tag (x.s ! c) }; 
            n = x.n 
        };

        WRAP_AP tag x = { 
            s = table { agr => wrap tag (x.s ! agr) }; 
            isPre = x.isPre 
        };

--        WRAP_AdA tag x = ;

--        WRAP_AdN tag x = ;

--        WRAP_AdV tag x = ;

        WRAP_Adv tag x = {
            s = wrap tag x.s
        };

--        WRAP_Ant tag x = ;

        WRAP_CAdv tag x = { 
            s = table { pol => wrap tag (x.s ! pol) }; 
            p = x.p 
        };

        WRAP_CN tag x = { 
            s = table { 
                num => table { 
                    c => wrap tag (x.s ! num ! c) 
                } 
            }; 
            g = x.g 
        };

        WRAP_Card tag x = { 
            s = table { b => table { c => wrap tag (x.s ! b ! c) } };
            sp = table { b => table { c => wrap tag (x.sp ! b ! c) } };
            n = x.n 
        };

        WRAP_Cl tag x = { 
            s = table { t => table { a => table { cp => table { o => wrap tag (x.s ! t ! a ! cp ! o) } } } } 
        };
                        
        WRAP_ClSlash tag x = { 
            s = table { t => table { a => table { cp => table { o => wrap tag (x.s ! t ! a ! cp ! o) } } } };
            c2 = x.c2 
        };

        WRAP_Comp tag x = { 
            s = table { agr => wrap tag (x.s ! agr) }
        };

        WRAP_Conj tag x = { 
            s1 = wrap tag x.s1;
            s2 = wrap tag x.s2;
            n = x.n 
        };

        WRAP_DAP tag x = { 
            s = wrap tag x.s;
            sp = table { g => table { b => table { c => wrap tag (x.sp ! g ! b ! c) } } };
            n = x.n;
            hasNum = x.hasNum
        };

        WRAP_Det tag x = { 
            s = wrap tag x.s;
            sp = table { g => table { b => table { c => wrap tag (x.sp ! g ! b ! c) } } };
            n = x.n;
            hasNum = x.hasNum
        };
                                
--        WRAP_Dig tag x = ;

        WRAP_Digits tag x = { 
            s = table { co => table { c => wrap tag (x.s ! co ! c) } };
            n = x.n;
            tail = x.tail
        };

--        WRAP_IAdv tag x = ;

        WRAP_IComp tag x = { 
            s = wrap tag x.s 
        };

        WRAP_IDet tag x = { 
            s = wrap tag x.s;
            n = x.n 
        };
                             
        WRAP_IP tag x = { 
            s = table { c => wrap tag (x.s ! c) };
            n = x.n 
        };

        WRAP_IQuant tag x = { 
            s = table { n => wrap tag (x.s ! n) }
        };

        WRAP_Imp tag x = { 
            s = table { cp => table { f => wrap tag (x.s ! cp ! f) } }
        };

--        -- WRAP_ImpForm tag x = ;
--        WRAP_Interj tag x = ;

--        WRAP_ListAP tag x = ;

--        WRAP_ListAdv tag x = ;

--        WRAP_ListNP tag x = ;

--        WRAP_ListRS tag x = ;

--        WRAP_ListS tag x = ;

        WRAP_N tag x = { 
            s = table { num => table { c => wrap tag (x.s ! num ! c) } }; 
            g = x.g 
        };

        WRAP_N2 tag x = { 
            s = table { n => table { c => wrap tag (x.s ! n ! c) } };
            g = x.g;
            c2 = x.c2
        };

        WRAP_N3 tag x = { 
            s = table { n => table { c => wrap tag (x.s ! n ! c) } };
            g = x.g;
            c2 = x.c2;
            c3 = x.c3
        };

        WRAP_NP tag x = { 
            s = table { c => wrap tag (x.s ! c) };
            a = x.a 
        };

--        WRAP_Num tag x = { 
--            s = table { b => table { c => wrap tag (x.s ! b ! c) } };
--            sp = table { b => table { c => wrap tag (x.sp ! b ! c) } };
--            n = x.n;
--            hasCard = x.hasCard
--        };

        WRAP_Numeral tag x = { 
            s = table { b => table { co => table { c => wrap tag (x.s ! b ! co ! c) } } };
            n = x.n 
        };

        WRAP_Ord tag x = { 
            s = table { c => wrap tag (x.s ! c) }
        };

--        WRAP_PConj tag x = ;

        WRAP_PN tag x = { 
            s = table { c => wrap tag (x.s ! c) };
            g = x.g 
        };

--        WRAP_Phr tag x = ;

        WRAP_Pol tag x = { 
            s = wrap tag x.s;
            p = x.p 
        };

        WRAP_Predet tag x = { 
            s = wrap tag x.s 
        };

        WRAP_Prep tag x = { 
            s = wrap tag x.s;
            isPre = x.isPre 
        };

        WRAP_Pron tag x = { 
            s = table { c => wrap tag (x.s ! c) };
            sp = table { c => wrap tag (x.sp ! c) };
            a = x.a 
        };

--        -- WRAP_Punct tag x = ;

        WRAP_QCl tag x = { 
            s = table { t => table { a => table { cp => table { qf => wrap tag (x.s ! t ! a ! cp ! qf) } } } }
        };

        WRAP_QS tag x = { 
            s = table { qf => wrap tag (x.s ! qf) }
        };

        WRAP_RCl tag x = { 
            s = table { t => table { a => table { cp => table { agr => wrap tag (x.s ! t ! a ! cp ! agr) } } } };
            c = x.c 
        };

        WRAP_RP tag x = { 
            s = table { rc => wrap tag (x.s ! rc) };
            a = x.a 
        };


        WRAP_RS tag x = { 
            s = table { agr => wrap tag (x.s ! agr) };
            c = x.c 
        };

        WRAP_S tag x = { 
            s = wrap tag x.s 
        };

--        WRAP_SC tag x = ;

        WRAP_SSlash tag x = { 
            s = wrap tag x.s;
            c2 = wrap tag x.c2
        };

--        WRAP_Sub100 tag x = ;

--        WRAP_Sub1000 tag x = ;

        WRAP_Subj tag x = { 
            s = wrap tag x.s 
        };

--        WRAP_Temp tag x = ;

--        WRAP_Tense tag x = ;

--        WRAP_Text tag x = ;

--        -- WRAP_Unit tag x = ;

        WRAP_Utt tag x = {
            s = wrap tag x.s
        };

        WRAP_V tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        WRAP_V2 tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        WRAP_V2A tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3 
        };

        WRAP_V2Q tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        WRAP_V2S tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2 
        };

        WRAP_V2V tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3; 
            typ = x.typ
        };

        WRAP_V3 tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl; 
            c2 = x.c2; 
            c3 = x.c3 
        };

        WRAP_VA tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

--        WRAP_VP tag x = lin VP { 
--            p = wrap tag x.p;
--            ad = table { agr => wrap tag (x.ad ! agr) };
--            s2 = table { agr => wrap tag (x.s2 ! agr) };
--            ext = wrap tag x.ext;
--            prp = wrap tag x.prp;
--            ptp = wrap tag x.ptp;
--            inf = wrap tag x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => wrap tag (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => wrap tag (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => wrap tag (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => wrap tag (x.nonAuxForms.pres ! agr) };
--                past = wrap tag x.nonAuxForms.past
--            }
--        };

--        WRAP_VPSlash tag x = lin VPSlash { 
--            p = wrap tag x.p;
--            ad = table { agr => wrap tag (x.ad ! agr) };
--            s2 = table { agr => wrap tag (x.s2 ! agr) };
--            ext = wrap tag x.ext;
--            prp = wrap tag x.prp;
--            ptp = wrap tag x.ptp;
--            inf = wrap tag x.inf;
--            isSimple = x.isSimple;
--            isAux = x.isAux;
--            auxForms = {
--                past = table { pol => table { agr => wrap tag (x.auxForms.past ! pol ! agr) } };
--                contr = table { pol => table { agr => wrap tag (x.auxForms.contr ! pol ! agr) } };
--                pres = table { pol => table { agr => wrap tag (x.auxForms.pres ! pol ! agr) } }
--            };
--            nonAuxForms = {
--                pres = table { agr => wrap tag (x.nonAuxForms.pres ! agr) };
--                past = wrap tag x.nonAuxForms.past
--            };
--            c2 = wrap tag x.c2;
--            gapInMiddle = x.gapInMiddle;
--            missingAdv = x.missingAdv
--        };

        WRAP_VQ tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        WRAP_VS tag x = { 
            s = table { vf => wrap tag (x.s ! vf) }; 
            p = x.p; 
            isRefl = x.isRefl 
        };

        WRAP_VV tag x = { 
            s = table { vf => wrap tag (x.s ! vf) };
            p = wrap tag x.p;
            typ = x.typ 
        };

--        WRAP_Voc tag x = ;
}
