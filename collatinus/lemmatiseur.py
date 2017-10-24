from .ch import estRomain

class Lemmatiseur(object):
	def __init__(self):
		pass

    def lemmatise(self, f):
        result = []
        if f.isEmpty():
            return result
        V_maj = f[0] == 'V'

        f_lower = f.lower()
        cnt_v = f_lower.count("v")
        cnt_ae = f_lower.count("æ")
        cnt_oe = f_lower.count("œ")
        if f_lower.endsWith("æ"):
            cnt_ae -= 1
        f = Lemmatiseur.deramise(f)
        # formes irrégulières
        QList<Irreg *> lirr = _irregs.values(f)
        foreach (Irreg *irr, lirr)
            for m in irr.morphos():
                sl = {irr.grq(), morpho(m), ""
                # result[irr.lemme()].prepend (morpho (m))
                result[irr.lemme()].prepend(sl)


        # radical + désinence
        for i in range(len(f)):
            r = f[:i]
            d = f[i:]
            ldes, lrad = [], []
            
            ldes = _desinences.values(d)
            if ldes.empty():
                continue
            # Je regarde d'abord si d est une désinence possible,
            # car il y a moins de désinences que de radicaux.
            # Je fais la recherche sur les radicaux seulement si la désinence existe.
            lrad = _radicaux.values(r)
            # ii noté ī
            # 1. Patauium, gén. Pataui : Patau.i . Patau+i.i
            # 2. conubium, conubis : conubi.s . conubi.i+s
            if d.startsWith('i') and not d.startsWith("ii") and not r.endsWith('i'):
                lrad.append(_radicaux.values(r + "i"))

            if lrad.empty(): # Il n'y a rien à faire si le radical n'existe pas.
                continue

            
            for rad in lrad:
                l = rad.lemme()
                for des in ldes:
                    if des.modele() == l.modele() and des.numRad() == rad.numRad() and not l.estIrregExcl(des.morphoNum()):
                        
                        c = cnt_v == 0 or (cnt_v == rad.grq().lower().count("v")+des.grq().count("v"))

                        if not c:
                            c = V_maj and rad.gr()[0] == 'U' and cnt_v - 1 == rad.grq().lower().count("v")

                        c = c and cnt_oe == 0 or cnt_oe == rad.grq().toLower().count("ōe")
                        c = c and cnt_ae == 0 or cnt_ae == (rad.grq().toLower().count("āe") + rad.grq().toLower().count("prăe"))

                        if c:
                            fq = rad.grq() + des.grq()
                            if not r.endsWith("i") and rad.gr().endsWith("i"):
                                fq = rad.grq().left(rad.grq().size()-1) + "ī" + des.grq().right(des.grq().size()-1)
                                
                            sl = {fq, morpho(des.morphoNum()), ""}
                            result[l].prepend(sl)

        if _extLoaded and not _extension and not result.isEmpty():
            # L'extension est chargée mais je ne veux voir les solutions qui en viennent que si toutes en viennent.
            MapLem res
            foreach (Lemme *l, result.keys())
                if l.origin() == 0:
                    res[l] = result[l]


            if (not res.isEmpty()) result = res

        # romains
        if estRomain(f) and not _lemmes.contains(f):
            lin = QString("%1|invor|adj. num.|1").arg(f)
            Lemme *romain = Lemme(lin, 0, self)
            nr = aRomano(f)
            romain.ajTrad(QString("%1").arg(nr), "fr")
            _lemmes.insert(f, romain)
            sl = {f,"inv",""
            QList<SLem> lsl
            lsl.append(sl)
            result.insert(romain, lsl)

        return result