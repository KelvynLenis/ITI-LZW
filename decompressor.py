import time
import sys

def decompress_lzw(input_file, k):
    isVideo = False
    if  "Video" in input_file:
        isVideo = True

    # Inicializa o dicionário com os caracteres ASCII
    dictionary = {i: chr(i) for i in range(256)}
    dict_size = 256

    current_string = ''
    output = []
    MAX_DIC_SIZE = 2**k

    # Lê o arquivo de entrada como uma sequência de bytes
    with open(input_file, "rb") as f:
        compressed_data = f.read()

    # Converte a sequência de bytes em uma sequência de números inteiros
    compressed_numbers = []
    for i in range(0, len(compressed_data), 2):
        compressed_numbers.append(int.from_bytes(compressed_data[i:i+2], byteorder='big'))

    # Inicializa o processo de descompressão
    current_string = chr(compressed_numbers.pop(0))
    output = [current_string]

    # Descomprime os dados usando o algoritmo LZW
    for num in compressed_numbers:
        if num in dictionary:
            entry = dictionary[num]
        elif num == dict_size:
            entry = current_string + current_string[0]
        else:
            raise ValueError("Compressed data is invalid")

        output.append(entry)

        # Adiciona uma nova entrada ao dicionário, se ainda houver espaço
        if dict_size < MAX_DIC_SIZE:
            dictionary[dict_size] = current_string + entry[0]
            dict_size += 1

        current_string = entry

    # Escreve a sequência de caracteres descomprimidos em um arquivo de saída
    output_file = input_file.split(".")[0] + "_decompressed.txt"
    if isVideo:        
        with open(f'./Output/decompress/decompressVideo{k}.mp4', "w", encoding='utf-8') as f:
            f.write("".join(output))
    else:
        with open(f'./Output/decompress/decompress{k}.txt', "w", encoding='utf-8') as f:
            f.write("".join(output))

if __name__ == "__main__":
    file_name = sys.argv[1]
    k = sys.argv[2]
    start_time = time.time()  # marca o tempo inicial
    decompress_lzw(file_name, int(k))
    end_time = time.time()  # marca o tempo final
    elapsed_time = end_time - start_time  # calcula o tempo decorrido
    print(f"Iteração {k}: {elapsed_time:.6f} segundos")