PyCollatinus
=========================

PyCollatinus is a port of the famous [Collatinus](https://github.com/biblissima/collatinus) developed in France by
Y. Ouvrad and P. Verkerk. I translated directly the code from C++, mostly manually. 

PyCollatinus aims to provide a Lemmatizer for [CLTK](https://github.com/cltk/cltk) but can also be used
for simple things such as searching for all possible lemmas of each single token of a sentence.

# How to

## Install

At the moment, this library is only usable from this directory. We are planning soon a release and a setup method as package.

You need to download the directory and make sure you have the dependency by typing

```shell
pip install -r requirements.txt
```

## Use

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
 
# To do !

- [ ] Writing tests (a lot !)
- [ ] Ensuring every cases are working
- [ ] Adding a lemmatizer for CLTK-Latin with some kind of probabilistic weighing.
- [ ] pip
- [ ] setup.py

# Licence

[Collatinus](https://github.com/biblissima/collatinus) is developed and maintained by Yves Ouvrard and Philippe Verkerk. It is made available under the GNU GPL v3 licence.

As such, this software bit is also GNU GPL v3.
