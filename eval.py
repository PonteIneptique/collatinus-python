from pycollatinus.lemmatiseur import Lemmatiseur
import timeit


# l.compile()
# del l
# l = Lemmatiseur.load()

number_of_tests = 10
start_time = timeit.default_timer()
for x in range(number_of_tests):
    l = Lemmatiseur()
    if x != number_of_tests - 1:
        del l
    print(x)
elapsed = timeit.default_timer() - start_time

print("{} s par test en moyenne pour {} chargements bruts".format(elapsed / number_of_tests, number_of_tests))
l.compile()
del l

start_time = timeit.default_timer()
for x in range(number_of_tests):
    l = Lemmatiseur.load()
    del l
    print(x)
elapsed = timeit.default_timer() - start_time
print("{} s par test en moyenne pour {} chargements par pickle".format(elapsed / number_of_tests, number_of_tests))

print(l.lemmatise("est"))
print(l.lemmatise("lascivi"))
print(l.lemmatise("lascivissimi"))
print(l.lemmatise("aliud"))
