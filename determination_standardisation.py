from main import *
from main import *
def est_standard(auto:Automate):
    print("je suis dans standar")
    print(auto.etatsInitiaux)
    if (est_deterministe(auto) ):
        return True



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
print(est_deterministe(t))

t.affichage()
determinisation(t)
for etat in t.etats:
    print(etat)
n=t.etats[1]+t.etats[3]
print("eeee",*t.etats[3].transiSortante)
print('experience',n,'s',*n.transiSortante,"e",*n.transiEntrante)

