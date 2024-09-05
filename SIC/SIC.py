import math

#定義十六進制的字典
HexDict = {i: str(i) if i < 10 else chr(i + 55) for i in range(16)}

#十進制轉十六進制
def dec_to_hex(dec):
    hex_value = ''
    while dec >= 16:
        hex_value = HexDict[dec % 16] + hex_value
        dec //= 16
    hex_value = HexDict[dec] + hex_value
    return hex_value

#十六進制轉十進制的字典
DecDict = {v: k for k, v in HexDict.items()}

#十六進制轉十進制
def hex_to_dec(hex_value):
    dec = 0
    times = 0
    while hex_value:
        dec += int(DecDict[hex_value[-1]] * math.pow(16, times))
        hex_value = hex_value[:-1]
        times += 1
    return dec

#定義byte指令
def byte(value):
    mode, data = value[0], value[2:-1]
    obj_code = ''
    if mode == 'C':
        obj_code = ''.join([dec_to_hex(ord(char)).zfill(2) for char in data])
    elif mode == 'X':
        obj_code = data
    else:
        print('BYTE Error')
    index_add = len(obj_code) // 2
    return index_add, obj_code

#定義word指令
def word(value):
    value = int(value)
    obj_code = dec_to_hex(value).zfill(6) if value >= 0 else dec_to_hex(hex_to_dec('1000000') + value).zfill(6)
    index_add = len(obj_code) // 2
    return index_add, obj_code

#定義resb指令
def resb(value):
    return int(value), ''

#定義resw指令
def resw(value):
    return int(value) * 3, ''

#指令助手字典，將Mnemonic映射為對應的機器碼
instruction_convert = {
    "ADD": "18", "ADDF": "58", "ADDR": "90", "AND": "40", "CLEAR": "B4", "COMP": "28", "COMPF": "88", "COMPR": "A0",
    "DIV": "24", "DIVF": "64", "DIVR": "9C", "FIX": "C4", "FLOAT": "C0", "HIO": "F4",
    "J": "3C", "JEQ": "30", "JGT": "34", "JLT": "38", "JSUB": "48",
    "LDA": "00", "LDB": "68", "LDCH": "50", "LDF": "70", "LDL": "08", "LDS": "6C", "LDT": "74", "LDX": "04", "LPS": "E0",
    "MUL": "20", "MULF": "60", "MULR": "98", "NORM": "C8", "OR": "44", "RD": "D8", "RMO": "AC", "RSUB": "4C",
    "SHIFTL": "A4", "SHIFTR": "A8", "SIO": "F0", "SSK": "EC", "STA": "0C", "STB": "78", "STCH": "54", "STF": "80", "STI": "D4",
    "STL": "14", "STS": "7C", "STSW": "E8", "STT": "84", "STX": "10", "SUB": "1C", "SUBF": "5C", "SUBR": "94", "SVC": "B0",
    "TD": "E0", "TIO": "F8", "TIX": "2C", "TIXR": "B8", "WD": "DC"}

#偽指令
pseudo_instruction = ['START', 'BYTE', 'WORD', 'RESB', 'RESW', 'END']

original_input = {} #原始輸入指令
function_index = {} #函數起始位置索引
object_code = {} #物件碼

#讀取輸入檔案
with open('Input.txt', 'r', encoding='utf-8') as inp:
    input_lines = inp.readlines()

    start = input_lines[0].replace('\n', '').split(' ')
    if start[-2] != 'START': #倒數第二個元素是否為'START'
        print('Error START')
    else:
        index = [dec_to_hex(hex_to_dec(start[-1]))]

        for i, line in enumerate(input_lines):
            if line.startswith('.'):  # 註解
                continue

            now_input = []
            now = line.replace('\n', '').split(' ')

            for j, item in enumerate(now):
                if item in instruction_convert or item in pseudo_instruction:
                    if item != 'START':
                        if item == 'BYTE':
                            index_add, obj_code = byte(now[j + 1])
                        elif item == 'WORD':
                            index_add, obj_code = word(now[j + 1])
                        elif item == 'RESB':
                            index_add, obj_code = resb(now[j + 1])
                        elif item == 'RESW':
                            index_add, obj_code = resw(now[j + 1])
                        elif item == 'END':
                            index_add, obj_code = 0, ''
                        else:
                            index_add = 3
                            try:
                                if ',X' in now[j + 1]:
                                    obj_code = f'nx,{instruction_convert[item]}{now[j + 1]}'
                                else:
                                    obj_code = f'n,{instruction_convert[item]}{now[j + 1]}'
                            except:
                                obj_code = f'{instruction_convert[item]}0000'

                        next_index = dec_to_hex(hex_to_dec(index[-1]) + index_add)
                    else:
                        index_add, obj_code = 0, ''
                        next_index = index[0]
                        original_input['START'] = now

                    if j == 1:
                        if now[0] not in function_index:
                            function_index[now[0]] = index[-1]
                        else:
                            print('Function Error, line:', index[-1])

                        now_input = [now[0]] + now[1:]
                    else:
                        now_input = [''] + now

                    if len(now_input) == 2:
                        now_input.append('')

                    object_code[index[-1]] = obj_code
                    original_input[index[-1]] = now_input

                    index.append(next_index)

        for i in object_code.keys():
            if 'n' in object_code[i]:
                obj_code = object_code[i].split(',')[1]
                address = function_index[obj_code[2:]]
                if len(address) < 4:
                    address = ("0" * (4 - len(address)) + address)
                if 'nx' in object_code[i]:
                    address = dec_to_hex(hex_to_dec(address[0]) + 8) + address[1:]

                object_code[i] = obj_code[:2] + address
print('\n\nLine'.ljust(15) + 'Location'.ljust(15) +
      'Original input'.ljust(45) + 'Object code'.rjust(15))
print('------------------------------------------------------------------------------------------')

print(str(5).ljust(15) + index[0].ljust(15) +
      original_input['START'][0].ljust(15) +
      original_input['START'][1].ljust(15) +
      original_input['START'][2].ljust(15) +
      ''.rjust(15))

for i, location in enumerate(index[1:-1]):
    line = (i + 2) * 5
    print(str(line).ljust(15) +
          location.ljust(15) +
          original_input[location][0].ljust(15) +
          original_input[location][1].ljust(15) +
          original_input[location][2].ljust(15) +
          object_code[location].rjust(15))