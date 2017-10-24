from . import Lemmatiseur
from .ch import atone, deramise
import warnings

class Lemme(object):
    def __init__(self, linea, origin, *parent):
        """ Constructeur de la classe Lemme à partire de la ligne linea.
            *parent est le lemmatiseur (classe Lemmat).

        :param linea: Ligne à parser
        :type linea: str
        :param origin: NO FUCKING IDEA
        :type origin: ?
        :param parent: Lemmatiseur
        :type parent: Lemmatiseur
        """
        # cădo|lego|cĕcĭd|cās|is, ere, cecidi, casum|687
        #   0 | 1  | 2   | 3 |     4                | 5

        self._lemmatiseur = parent

        eclats = linea.split('|')
        lg = eclats[0].split('=')

        self._cle = atone(deramise(lg[0]))
        self._grd = self.oteNh(lg[0], _nh)  # TODO: Cette ligne pose un problè : d'ou vient le _nh

        if lg.count() == 1:
            self._grq = _grd
        else:
            self._grq = lg.at(1)

        # pour l'affichage des dictionnaires, élimine les doubles de la forme canonique
        self._gr = atone(_grq.section(',',0,0))
        self._grModele = eclats[1]
        self._modele = _lemmatiseur.modele(_grModele)
        self._hyphen = ""
        self._origin = origin

        # Tous les lemmes doivent avoir été rencontrés une fois
        self._nbOcc = 1

        # contrôle de format. la liste doit avoir 6 items
        if len(eclats) < 6:
            warnings.warn("Ligne mal formée : " + self._gr + "\n ---Dernier champ " + eclats[-1] + "\n ---" +linea

        # lecture des radicaux, 2 et 3
        for i in range(2, 4):
            if eclats[i]:
                lrad = eclats[i].split(',')
                for rad in lrad:
                    _radicaux[i-1].append(new Radical(rad, i-1, self))

        _lemmatiseur.ajRadicaux(self)

        _indMorph = eclats.at(4)
        QRegExp c("cf\\.\\s(\\w+)$")
        pos = c.indexIn(_indMorph)
        if pos > -1:
            _renvoi = c.cap(1)

        else:
            _renvoi = ""

        _pos.clear()
        if _indMorph.contains("adj."):
            _pos.append('a')
        if _indMorph.contains("conj"):
            _pos.append('c')
        if _indMorph.contains("excl."):
            _pos.append('e')
        if _indMorph.contains("interj"):
            _pos.append('i')
        if _indMorph.contains("num."):
            _pos.append('m')
        if _indMorph.contains("pron."):
            _pos.append('p')
        if _indMorph.contains("prép"):
            _pos.append('r')
        if _indMorph.contains("adv"):
            _pos.append('d')
        if _indMorph.contains(" nom ") or _indMorph.contains("npr."):
            _pos.append('n')
        if _pos.isEmpty():
            _pos.append(_modele.pos())
            # Je prends le POS du modèle
            if _pos == "d" and not _renvoi.isEmpty():
                _pos = ""
            # S'il y a un renvoi (cf.) et que le modèle a donné le POS "d" (adverbe),
            # je prendrai le pos du renvoi (les indéclinables ont le POS par défaut "d").
            # Je ne peux pas le faire maintenant !

        # nombre d'occurrences
        _nbOcc = eclats.at(5).toInt()


    ''' Avec l'internationalisation des morphos, genre dépend de la langue choisie.
     * Il faut donc le définir à la demande.
        _genre.clear()
        if _indMorph.contains(" m."):
            _genre.append(" " + _lemmatiseur.genre(0))
    #        _genre.append(" masculin"); # Peut-être mieux d'utiliser Flexion.genres[0] ?
        if _indMorph.contains(" f."):
            _genre.append(" " + _lemmatiseur.genre(1))
    #        _genre.append(" féminin")
        if _indMorph.contains(" n."):
            _genre.append(" " + _lemmatiseur.genre(2))
    #        _genre.append(" neutre")
        _genre = _genre.trimmed()
    '''


    '''*
     * \fn void Lemme.ajIrreg (Irreg *irr)
     * \brief Ajoute au lemme l'obet irr, représente
     *        une forme irrégulière. Lorsque les formes irrégulières
     *        sont trop nombreuses, lorsque plusieurs lemmes
     *        ont des formes analogues, vaut ajouter un modèle
     *        dans data/modeles.la.
     '''
    def ajIrreg(self, *irr):
        _irregs.append(irr)
        # ajouter les numéros de morpho à la liste
        # des morphos irrégulières du lemme :
        if irr.exclusif()) _morphosIrrExcl.append(irr.morphos():


    '''*
     * \fn void Lemme.ajNombre(int n)
     * \brief Ajoute l'entier n au nombre d'occurrences du lemme.
     *
     *      Un lemme de Collatinus peut être associé à plusieurs lemmes du LASLA.
     *      D'où la somme.
     '''
    def ajNombre(self, n):
        _nbOcc += n
        # Un lemme de Collatinus peut être associé à plusieurs lemmes du LASLA.
        # D'où la somme.


    '''*
     * \fn void Lemme.ajRadical (int i, r)
     * \brief Ajoute le radical r de numéro i à la map des
     *        radicaux du lemme.
     '''
    def ajRadical(self, i, *r):
        _radicaux[i].append(r)


    '''*
     * \fn void Lemme.ajTrad (QString t, l)
     * \brief ajoute la traduction t de langue l à
     *        la map des traductions du lemme.
     '''
    def ajTrad(self, t, l):
    #    if _traduction.contains(l) and _traduction[l] != "":
    #        qDebug() << _grq << t << l << _traduction[l]
        _traduction[l] = t


    '''*
     * \fn QString Lemme.ambrogio()
     * \brief Renvoie dans une chaîne un résumé
     *        de la traduction du lemme dans toutes les
     *        langues cibles disponibles.
     '''
    def ambrogio(self):
        QString retour
        QTextStream ss(&retour)
        ss << "<hr/>" << humain() << "<br/>"
        ss << "<table>"
        for lang in _traduction.keys():
            trad = _traduction[lang]
            langue = _lemmatiseur.cibles()[lang]
            if not trad.isEmpty():
                ss << "<tr><td>- " << langue << "</td><td>&nbsp;" << trad
                   << "</td></tr>\n"

        ss << "</table>"
        return retour


    '''*
     * \fn QString Lemme.cle ()
     * \brief Renvoie la clé sous laquel le
     *        lemme est enregistré dans le lemmatiseur parent.
     '''
    def cle(self):
        return _cle


    '''*
     * \fn QList<int> Lemme.clesR ()
     * \brief Retourne toutes les clés (formes non-ramistes
     *        sans diacritiques) de la map des radicaux du lemme.
     '''
    def clesR(self):
        return _radicaux.keys()


    '''*
     * \fn bool Lemme.estIrregExcl (int nm)
     * \param nm : numéro de morpho
     * \brief Renvoie vrai si la forme irrégulière
     *        avec le n° nm remplace celle construite
     *        sur le radical , si la
     *        forme régulière existe aussi.
     '''
    def estIrregExcl(self, nm):
        return _morphosIrrExcl.contains(nm)


    '''*
     * @brief Lemme.genre
     * @return : le (ou les) genre(s) du mot.
     *
     * Cette routine convertit les indications morphologiques,
     * données dans le fichier lemmes.la,
     * pour exprimer le genre du mot dans la langue courante.
     *
     * Introduite pour assurer l'accord entre un nom et son adjectif.
     *
     '''
    def genre(self):
        QString _genre
        if _indMorph.contains(" m."):
            _genre.append(" " + _lemmatiseur.genre(0))
    # J'ai ainsi le genre dans la langue choisie.
        if _indMorph.contains(" f."):
            _genre.append(" " + _lemmatiseur.genre(1))
    #        _genre.append(" féminin")
        if _indMorph.contains(" n."):
            _genre.append(" " + _lemmatiseur.genre(2))
    #        _genre.append(" neutre")
        _genre = _genre.trimmed()
        if not _renvoi.isEmpty() and _genre.isEmpty():
            Lemme *lr = _lemmatiseur.lemme(_renvoi)
            if lr != NULL) return lr.genre(:

        return _genre


    '''*
     * \fn return _gr
     * \brief Retourne la graphie ramiste du lemme sans diacritiques.
     '''
    def gr(self):
        return _gr


    '''*
     * \fn QString Lemme.grq ()
     * \brief Retourne la graphie ramiste du lemme sans diacritiques.
     '''
    def grq(self):
        return _grq


    '''*
     * \fn QString Lemme.grModele ()
     * \brief Retourne la graphie du modèle du lemme.
     '''
    def grModele(self):
        return _grModele


    '''*
     * \fn QString Lemme.humain (bool html, l)
     * \brief Retourne une chaîne donnant le lemme ramiste avec diacritiques,
     *        ses indications morphologiques et sa traduction dans la langue l.
     *        Si html est True, retour est au format html.
     '''
    def humain(self, html, l, nbr):
        QString res
        QString tr
        if not _renvoi.isEmpty():
            Lemme *lr = _lemmatiseur.lemme(_renvoi)
            if lr != 0:
                tr = lr.traduction(l)
            else:
                tr = "renvoi non trouvé"

        else:
            tr = traduction(l)
        QTextStream flux(&res)
        grq = _grq
        if grq.contains(","):
            grq.replace(",",", ")
            grq.replace("  "," ")

        if html:
            flux << "<strong>" << grq << "</strong>, "
                              << "<em>" << _indMorph << "</em>"
        else:
            flux << grq << ", " << _indMorph
        if (_nbOcc != 1) and nbr:
            if html:
                flux << " <small>(" << _nbOcc << ")</small>"
            else flux << " (" << _nbOcc << ")"

        flux << " : " << tr
        return res


    def indMorph(self):
        return _indMorph


    '''*
     * \fn QString Lemme.irreg (int i, *excl)
     * \brief Renvoie la forme irrégulière de morpho i. excl devient
     *        True si elle est exclusive, sinon.
     '''
    def irreg(self, i, *excl):
        foreach (Irreg *ir, _irregs)
            if ir.morphos().contains(i):
                *excl = ir.exclusif :
                return ir.grq()


        return ""


    '''*
     * \fn Modele* Lemme.modele ()
     * \brief Renvoie l'objet modèle du lemme.
     '''
    Modele *Lemme.modele()
        return _modele


    '''*
     * \fn int Lemme.nbOcc()
     * \brief Renvoie le nombre d'occurrences du lemme dans les textes du LASLA.
     '''
    def nbOcc(self):
        return _nbOcc


    '''*
     * @brief Lemme.clearOcc
     * Initialise le nombre d'occurrences.
     '''
    def clearOcc(self):
        _nbOcc = 1


    '''*
     * \fn int Lemme.nh()
     * \brief Renvoie le numéro d'homonymie du lemme.
     '''
    def nh(self):
        return _nh


    '''*
     * \fn int Lemme.origin()
     * \brief Renvoie l'origine du lemme : 0 pour le lexique de base, pour l'extension.
     '''
    def origin(self):
        return _origin


    '''*
     * \fn QString Lemme.oteNh (QString g, &nh)
     * \brief Supprime le dernier caractère de g si c'est
     *        un nombre et revoie le résultat après avoir
     *        donné la valeur de ce nombre à nh.
     '''
    def oteNh(self, g, &nh):
        c = g.right(1).toInt()
        if c > 0:
            nh = c
            g.chop(1)

        else:
            c = 1
        return g


    '''*
     * \fn QString Lemme.pos ()
     * \brief Renvoie un caractère représentant la
     *        catégorie (part of speech, orationis)
     *        du lemme.
     '''
    def pos(self):
        if _pos.isEmpty() and not _renvoi.isEmpty():
            Lemme *lr = _lemmatiseur.lemme(_renvoi)
            if lr != NULL) return lr.pos(:

        return _pos


    '''*
     * \fn QList<Radical*> Lemme.radical (int r)
     * \brief Renvoie le radical numéro r du lemme.
     '''
    QList<Radical *> Lemme.radical(int r)
        return _radicaux.value(r)


    '''*
     * \fn bool Lemme.renvoi()
     * \brief Renvoie True si le lemme est une forme
     *        alternative renvoyant à une autre entrée
     *        du lexique.
     '''
    bool Lemme.renvoi() { return _indMorph.contains("cf. ");
    '''*
     * \fn QString Lemme.traduction(QString l)
     * \brief Renvoie la traduction du lemme dans la langue
     *        cible l (2 caractères, plus
     *        pour donner l'ordre des langues de secours).
     *        J'ai opté pour un format "l1.l2.l3" où
     *        les trois langues sont en 2 caractères.
     '''
    def traduction(self, l):
        if l.size() == 2:
        if _traduction.keys().contains(l):
            return _traduction[l]
        elif _traduction.keys().contains("fr"):
            return _traduction["fr"]
        else return _traduction["en"]

        elif _traduction.keys().contains(l.mid(0,2)):
            return _traduction[l.mid(0,2)]
        elif _traduction.keys().contains(l.mid(3,2)):
            return _traduction[l.mid(3,2)]
        elif (l.size() == 8) and _traduction.keys().contains(l.mid(6,2)):
            return _traduction[l.mid(6,2)]
        return "non traduit / Translation not available."


    '''*
     * \fn bool Lemme.operator<(Lemme &l)
     * \brief vrai si la fréquence du lemme de gauche est
     *        inférieure à celle de celui de droite.
     *        commenté : vrai si la graphie du lemme de gauche
     *        précède celle de celui de droite dans
     *        l'ordre alphabétique.
     '''
    bool Lemme.operator<( Lemme &l)
        #qDebug()<<"operator<"<<_gr
        return _nbOcc < l.nbOcc()
        #return _gr < l.gr()


    '''*
     * @brief Lemme.setHyphen
     * @param h : indique où se fait la césure.
     * \brief stocke l'information sur la césure étymologique du lemme
     '''
    def setHyphen(self, h):
        _hyphen = h


    '''*
     * @brief Lemme.getHyphen
     * @return la césure étymologique du lemme
     '''
    def getHyphen(self):
        return _hyphen
