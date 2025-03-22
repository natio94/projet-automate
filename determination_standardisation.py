from main import *
def est_standard(auto:Automate):
    if (est_deterministe(auto) and auto.etatsInitiaux[0].transiEntrante == []):
        return True
    return False


def standardisation(auto:Automate):
    if (est_standard(auto) == True):
        return auto.affichage()
    else :
        c = Etat(1000)
        etatInit=deepcopy(auto.etatsInitiaux)
        for i in etatInit:
            for e in i.transiSortante:
                auto.transitions.append(Transition(c , e.symbole, e.arrivee))
            auto.etatsInitiaux.remove(i)
        c.final=any(etat.final for etat in etatInit)
        auto.etatsInitiaux.append(c)
        auto.etats.append(c)
    return auto.affichage()


def est_deterministe(auto:Automate):
    if auto.nbEtatsInitiaux!=1:
        return False
    etatSymb=[]
    for transi in auto.transitions:
        etatSymb.append(str(transi.depart)+str(transi.symbole))
    return len(etatSymb)==len(set(etatSymb))


def determinisation(auto:Automate):
    if est_deterministe(auto):
        print("L'automate est déjà déterministe")
        return auto
    if auto.nbEtatsInitiaux>1:
        etatsInit=auto.etatsInitiaux




t=Automate("automates/5")
print(est_standard(t))
print(standardisation(t))
print(est_deterministe(t))



