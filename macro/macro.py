with open('./Input.txt', 'r') as f:
    Input = f.readlines()

main, macro, in_macro, line = [], {}, [False, ''], 5

#處理分割後的程式碼的各個部分
def process_line(parts):
    if len(parts) == 1:
        return [line, '', parts[0], '']
    elif len(parts) == 2: 
        return [line, '', parts[0], parts[1]]
    else:
        return [line, parts[0], parts[1], parts[2]]

for i in Input:
    line += 5

    #巨集處理
    if i[0] == '.':
        continue

    i = i.replace('\n', '').split(' ')
    now = process_line(i)

    if now[2] == 'MACRO':
        in_macro = [True, now[1]]
        macro[now[1]] = [now[3].split(','), []]
        continue
    elif now[2] == 'MEND':
        in_macro = [False, '']
        continue

    #主程式碼轉換
    if in_macro[0]:
        macro[in_macro[1]][1].append(now)
    else:
        if now[2] in macro:
            function_ = now[1]

            if now[1] != '':
                now[1] = f'.{now[1]}'

            main.append(now.copy())

            parms = {macro[now[2]][0][n]: now[3].split(',')[n] for n in range(len(macro[now[2]][0]))}

            macro[now[2]][1][0][1] = function_
            for n, j in enumerate(macro[now[2]][1]):
                j = j.copy()
                j[0] = str(line) + chr(ord('a') + n)

                for k in parms.keys():
                    if k in j[3]:
                        j[3] = j[3].replace(k, parms[k])

                main.append(j.copy())

        else:
            main.append(now)

print(" %-10s %-10s %-10s %-10s" % ('Line', '', 'Original', ''))
for i in main:
    if i[1] == '.':
        print(" %-10s %-10s %-10s %-39s" % (i[0], i[1], i[2], i[3]))
    else:
        print(" %-10s %-10s %-10s %-10s" % (i[0], i[1], i[2], i[3]))