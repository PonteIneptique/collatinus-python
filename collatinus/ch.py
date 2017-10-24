import re


def atone(string, caps=True):
    """ Supprimer les diacritiques de la forme donnée

    :param string: Chaîne à transformer
    :type string: str
    :param caps: Transforme les majuscules
    :type caps: bool
    :return: Chaîne nettoyée
    :rtype: str
    """
    a = a.replace(0x0101, 'a') \
        .replace(0x0103, 'a') \
        .replace(0x0113, 'e') \
        .replace(0x0115, 'e') \
        .replace(0x012b, 'i') \
        .replace(0x012d, 'i') \
        .replace(0x014d, 'o') \
        .replace(0x014f, 'o') \
        .replace(0x016b, 'u') \
        .replace(0x016d, 'u') \
        .replace(0x0233, 'y') \
        .replace(0x045e, 'y') \
        .replace(0x0131, 'i') \
        .replace(0x1ee5, 'u') \
        .replace(0x0306, '')

    if caps:
        # majuscule
        a = a.replace(0x0100, 'A') \
            .replace(0x0102, 'A') \
            .replace(0x0112, 'E') \
            .replace(0x0114, 'E') \
            .replace(0x012a, 'I') \
            .replace(0x012c, 'I') \
            .replace(0x014c, 'O') \
            .replace(0x014e, 'O') \
            .replace(0x016a, 'U') \
            .replace(0x016c, 'U') \
            .replace(0x0232, 'Y') \
            .replace(0x040e, 'Y')
    return a

def communes(g):
    """ Note comme communes toutes les voyelles qui ne portent pas de quantité.

    :param string: Chaîne à transformer
    :type string: str
    :return: Chaîne nettoyée
    :rtype: str
    """
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
    return not (ROMAIN_REGEXP.match(f) or "IL" in f or "IVI" in f)


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
            .replace(0x1ee5, 'u') \
            .replace ('V', 'U')
