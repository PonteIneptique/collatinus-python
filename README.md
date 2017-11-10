PyCollatinus
=========================

[![Build Status](https://travis-ci.org/PonteIneptique/collatinus-python.svg?branch=master)](https://travis-ci.org/PonteIneptique/collatinus-python)
[![Coverage Status](https://coveralls.io/repos/github/PonteIneptique/collatinus-python/badge.svg?branch=master)](https://coveralls.io/github/PonteIneptique/collatinus-python?branch=master)
[![DOI](https://zenodo.org/badge/108088404.svg)](https://zenodo.org/badge/latestdoi/108088404)
[![PyPI version](https://badge.fury.io/py/pycollatinus.svg)](https://badge.fury.io/py/pycollatinus)

PyCollatinus is a port of the famous [Collatinus](https://github.com/biblissima/collatinus) developed in France by
Y. Ouvrard and P. Verkerk. I translated directly the code from C++, mostly manually. 

PyCollatinus aims to provide a Lemmatizer for [CLTK](https://github.com/cltk/cltk) but can also be used
for simple things such as searching for all possible lemmas of each single token of a sentence.

# How to

## Install

You can install PyCollatinus using pip : `pip install pycollatinus`

## Use

The analyzer is pretty easy to use : 

```python
from pycollatinus import Lemmatiseur
analyzer = Lemmatiseur()
analyzer.lemmatise_multiple("Cogito ergo sum")
```

will result in
 
```python
[
    [{'lemma': 'cogo', 'morph': '2ème singulier impératif futur actif', 'form': 'cogito'}, {'lemma': 'cogo', 'morph': '3ème singulier impératif futur actif', 'form': 'cogito'}, {'lemma': 'cogito', 'morph': '1ère singulier indicatif présent actif', 'form': 'cogito'}, {'lemma': 'cogito', 'morph': '1ère singulier indicatif présent actif', 'form': 'cogito'}],
    [{'lemma': 'ergo', 'morph': '1ère singulier indicatif présent actif', 'form': 'ergo'}, {'lemma': 'ergo', 'morph': 'positif', 'form': 'ergo'}],
    [{'lemma': 'sum', 'morph': '1ère singulier indicatif présent actif', 'form': 'sum'}]
]
```

## How to make it faster

There is a lot of data to process for PyCollatinus and we decided not to convert this data to keep as close as possible 
to the original C and this way be able to load any new data coming our way or helping them correct some more.

To avoid a huge loading time, you can compile the Lemmatizer and load it : 

```python
from pycollatinus import Lemmatiseur
analyzer = Lemmatiseur()
analyzer.compile()  # Persists the data
```

Next time, just do : 

```python
from pycollatinus import Lemmatiseur
analyzer = Lemmatiseur.load()
```

## Performance

On a *Intel(R) Core(TM) i3-3120M CPU @ 2.50GHz*, LinuxMint 17 3.8.4 (Ubuntu 2015-12-02), Python 3.4.3

| Method | Average Time on 10 calls |
| ------ | ---- |
| From Collatinus data | 11.62 s |
| From compiled data | 5.92 s |

[Script run for these evaluations](eval.py)

# Licence

[Collatinus](https://github.com/biblissima/collatinus) is developed and maintained by Yves Ouvrard and Philippe Verkerk. It is made available under the GNU GPL v3 licence.

As such, this software bit is also GNU GPL v3.
