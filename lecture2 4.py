import csv
import matplotlib.pyplot as plt
import numpy as np
import math
import matplotlib.ticker as ticker

def average(a):
    sm = 0

    for x in a:
        sm += float(x)

    return sm / len(a)

a = {}
seen = set([])

# "Kostya": 19, ...

with open('New-Zealand-period-life-tables-2017-2019-CSV.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    header = True
    for row in spamreader:
        if header == True:
            header = False
            continue
        
        if row[4] not in seen:
            seen.add(row[4])
            a[row[4].split()[0]] = [ row[6] ]
        else:
            a[row[4].split()[0]].append(row[6])

x = a.keys()
y = []
for key in a.keys():
    y.append(average(a[key]))

fig, ax = plt.subplots()

#  Устанавливаем интервал основных делений:
ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
#  Устанавливаем интервал вспомогательных делений:
ax.xaxis.set_minor_locator(ticker.MultipleLocator(10))

#  Данные в виде линий:
ax.plot(x, y, label='*Some index* dependence on age') # ДОБАВИТЬ НАЗВАНИЕ ИССЛЕДОВАНИЯ
ax.set(title='График') # НАЗВАНИЕ ГРАФИКА

syntet_data = np.linspace(0, 100, 100)
syntet_data_y = -3 * syntet_data**2 + 30000

ax.plot(syntet_data, syntet_data_y, label='Parabola')

plt.xlabel('age', fontsize=16)
plt.ylabel('Some index', fontsize=16) # ДОБАВИТЬ НАЗВАНИЕ ИССЛЕДОВАНИЯ

plt.legend(fontsize=14, loc = 3)
plt.show()
