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
    if caps is True:
        return unidecode(string)
    a = ""
    for char in string:
        if char.isupper():
            a += char
        else:
            a += unidecode(char)
    return a


_VOY_COMMUNES = re.compile("\w*[aeiouy]\w*")


_VOY_REPLACE = [
    (re.compile("([^āăō])e"), "\1ē̆"),
    (re.compile("^e"),"ē"),
    (re.compile("([^āēq])u"), "\1ū̆"),
    (re.compile("^u"), "ū̆"),
    (re.compile("^y"),"ȳ̆"),
    (re.compile("([^ā])y"), "\1ȳ̆")
]

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
    if _VOY_COMMUNES.match(g):
        g = g.replace("a", "ā̆") \
             .replace("i", "ī̆") \
             .replace("o", "ō̆")
        for regex, replace in _VOY_REPLACE:
            g = regex.sub(replace, g)

    if maj:
        g = g[0].upper() + g[1:]

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