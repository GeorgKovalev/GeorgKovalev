a = input()
s = a.split(";")
numbers2 = []
numbers3 = []
words4 = []

for cur_el in s:
    if cur_el.isdigit():
        if int(cur_el) % 2 ==0:
            numbers2.append(cur_el)
        if int(cur_el) % 3 ==0:
            numbers3.append(cur_el)
    elif len(cur_el) > 4:
        words4.append(cur_el)
print(','.join(numbers2 + numbers3 + words4), end='')