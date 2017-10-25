import re
from unidecode import unidecode

voyelles = "āăēĕīĭōŏūŭȳўĀĂĒĔĪĬŌŎŪŬȲЎ"
consonnes = "bcdfgjklmnpqrstvxz"
abrev = [
    "Agr", "Ap", "A", "K", "D", "F", "C",
    "Cn", "Kal", "L", "Mam", "M\"", "M", "N", "Oct",
    "Opet", "Post", "Pro", "P", "Q", "Sert",
    "Ser", "Sex", "S", "St", "Ti", "T", "V",
    "Vol", "Vop", "Pl"
]


_SIMPLIFIED_RE = re.compile("\s+")


def simplified(string):
    """ Remove multiple spaces and strip a string

    :param string: Chaîne à transformer
    :type string: str
    :return: Chaîne nettoyée
    :rtype: str
    """
    return _SIMPLIFIED_RE.sub(" ", string).strip()


def atone(string, caps=True):
    """ Supprimer les diacritiques de la forme donnée

    :param string: Chaîne à transformer
    :type string: str
    :param caps: Transforme les majuscules
    :type caps: bool
    :return: Chaîne nettoyée
    :rtype: str
    """
    a = ""
    for chr in string:
        if caps:
            if chr.isupper():
                a += unidecode(chr)
            else:
                a += chr
        else:
            a += unidecode(chr)
    return a


def communes(g):
    """ Note comme communes toutes les voyelles qui ne portent pas de quantité.

    :param string: Chaîne à transformer
    :type string: str
    :return: Chaîne nettoyée
    :rtype: str
    """
    if len(g) == 0:
        return g
    maj = g[0].isupper()
    g = g.lower()
    if g.contains("a") or g.contains("e") or g.contains("i") or g.contains("o") or g.contains("u") or g.contains("y"):
        g = g.replace("a","ā̆") \
             .replace(QRegExp("([^āăō])e"),"\\1ē̆") \
             .replace(QRegExp("^e"),"ē̆") \
             .replace("i","ī̆") \
             .replace("o","ō̆") \
             .replace(QRegExp("([^āēq])u"),"\\1ū̆") \
             .replace(QRegExp("^u"),"ū̆") \
             .replace(QRegExp("^y"),"ȳ̆") \
             .replace(QRegExp("([^ā])y"),"\\1ȳ̆")

    if maj:
        g[0] = g[0].upper() + g[1:]

    return g


_ROMAIN_REGEXP = re.compile("[^IVXLCDM]")


def estRomain(f):
    """ F est-elle une forme de nombre romain ?

    :param f: Forme
    :type f: str
    :return: Statut de nombre romain
    :type: bool
    """
    return not (_ROMAIN_REGEXP.match(f) or "IL" in f or "IVI" in f)


def deramise(r):
    """ Déramise une chaîne
    
    :param string: Chaîne à transformer
    :type string: str
    :return: Chaîne nettoyée
    :rtype: str
    """
    return r.replace('J', 'I') \
            .replace('j', 'i') \
            .replace('v', 'u') \
            .replace("æ", "ae") \
            .replace("Æ", "Ae") \
            .replace("œ", "oe") \
            .replace("Œ", "Oe") \
            .replace("ụ", 'u') \
            .replace('V', 'U')


def allonge(f):
    """ Modifie f pour que sa dernière voyelle devienne longue.
    
    :param string: Chaîne à transformer
    :type string: str
    :return: Chaîne modifiée
    :rtype: str
    """
    if not f:
        return ""

    return f

    ## TODO : Implementer correctement la suite

    taille = len(f)
    # Je sais que le morceau à attacher commence par une consonne.
    if f[taille-2] in consonnes and not f[-2:].lower() in ["āe", "āu", "ēu",  "ōe"]:
        f = re.sub("[a\u0103]([" + consonnes + "])$", "\u0101\\1", f)
        f = re.sub("[e\u0115]([" + consonnes + "])$", "\u0113\\1", f)
        f = re.sub("[i\u012d]([" + consonnes + "])$", "\u012b\\1", f)
        f = re.sub("[o\u014F]([" + consonnes + "])$", "\u014d\\1", f)
        f = re.sub("[u\u016d]([" + consonnes + "])$", "\u016b\\1", f)
        f = re.sub("[y\u0233]([" + consonnes + "])$", "\u045e\\1", f)
        f = re.sub("[A\u0102]([" + consonnes + "])$", "\u0100\\1", f)
        f = re.sub("[E\u0114]([" + consonnes + "])$", "\u0112\\1", f)
        f = re.sub("[I\u012c]([" + consonnes + "])$", "\u012a\\1", f)
        f = re.sub("[O\u014e]([" + consonnes + "])$", "\u014c\\1", f)
        f = re.sub("[U\u016c]([" + consonnes + "])$", "\u016a\\1", f)
        f = re.sub("[Y\u0232]([" + consonnes + "])$", "\u040e\\1", f)
        return f