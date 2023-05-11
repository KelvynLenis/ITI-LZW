import sys
import time

def compress_lzw(file_name, k):
    isVideo = False
    if file_name.endswith(".mp4"):
        isVideo = True

    with open(file_name, 'r', encoding='iso-8859-1') as f:
        data = f.read()

    dictionary = {chr(i): i for i in range(256)}
    dict_size = 256
    current_string = ''
    output = []
    MAX_DICT_SIZE = 2**k

    for char in data:
        if current_string + char in dictionary:
            current_string += char
        else:
            output.append(dictionary[current_string].to_bytes(2, byteorder='big'))
            if dict_size < MAX_DICT_SIZE:
                dictionary[current_string + char] = dict_size
                dict_size += 1
            current_string = char

    if current_string in dictionary:
        output.append(dictionary[current_string].to_bytes(2, byteorder='big'))
    else:
        output.append(dictionary[current_string[:-1]].to_bytes(2, byteorder='big'))
        output.append(dictionary[current_string[-1]].to_bytes(2, byteorder='big'))

    if isVideo:    
        with open(f'./Output/compress/compressedVideo{k}' + '.lzw', 'wb') as f:
            for item in output:
                if len(item) == 2:
                    f.write(item)
                elif len(item) == 3:
                    MAX_INT_SIZE = 65535 # Tamanho máximo permitido para um valor inteiro de 2 bytes
                    if int.from_bytes(item, byteorder='big') <= MAX_INT_SIZE:
                        f.write(item[:2])
                    else:
                        parts = []
                        value = int.from_bytes(item, byteorder='big')
                        while value > 0:
                            part = value % MAX_INT_SIZE
                            parts.append(part.to_bytes(2, byteorder='big'))
                            value = (value - part) // MAX_INT_SIZE
                        f.write(reversed(parts))
    else:
        with open(f'./Output/compress/compressed{k}' + '.lzw', 'wb') as f:
            for item in output:
                if len(item) == 2:
                    f.write(item)
                elif len(item) == 3:
                    MAX_INT_SIZE = 65535 # Tamanho máximo permitido para um valor inteiro de 2 bytes
                    if int.from_bytes(item, byteorder='big') <= MAX_INT_SIZE:
                        f.write(item[:2])
                    else:
                        parts = []
                        value = int.from_bytes(item, byteorder='big')
                        while value > 0:
                            part = value % MAX_INT_SIZE
                            parts.append(part.to_bytes(2, byteorder='big'))
                            value = (value - part) // MAX_INT_SIZE # Atualizando o valor de value para ser a parte inteira da divisão
                        f.write(reversed(parts))

    print(f"Tamanho do dicionario: {dict_size}")

if __name__ == "__main__":
    file_name = sys.argv[1]
    # file_name = './Input/corpus16MB.txt'
    for k in range(9, 17):
        start_time = time.time()  # marca o tempo inicial
        compress_lzw(file_name, k)
        end_time = time.time()  # marca o tempo final
        elapsed_time = end_time - start_time  # calcula o tempo decorrido
        print(f"Iteração {k}: {elapsed_time:.6f} segundos")