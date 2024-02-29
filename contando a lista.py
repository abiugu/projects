import os

def read_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def process_data(lines):
    acertos = 0
    acertos_martingale = 0
    erros = 0
    erros_martingale = 0
    acertos_patterns = []
    erros_patterns = []

    in_detailed_results = False
    
    for line in lines:
        if "Acerto" in line:
            if "Martingale" in line:
                acertos_martingale += 1
            else:
                acertos += 1
        elif "Erro" in line:
            if "Martingale" in line:
                erros_martingale += 1
            else:
                erros += 1
        elif "Resultados detalhados" in line:
            in_detailed_results = True
        elif in_detailed_results and line.strip().startswith('('):
            number = int(line.split(')')[0][1:])
            if "Acerto" in line:
                acertos_patterns.append(number)
            elif "Erro" in line:
                erros_patterns.append(number)
        elif in_detailed_results and not line.strip():
            break
    
    return acertos, acertos_martingale, erros, erros_martingale, acertos_patterns, erros_patterns

def main():
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_name = 'historico_do_dia.txt'
    file_path = os.path.join(desktop_path, file_name)
    
    if os.path.exists(file_path):
        lines = read_file(file_path)
        acertos, acertos_martingale, erros, erros_martingale, acertos_patterns, erros_patterns = process_data(lines)

        print("acertos:", acertos)
        print("acertos martingale:", acertos_martingale)
        print("erros:", erros)
        print("erros martingale:", erros_martingale)
    else:
        print(f"O arquivo {file_name} não foi encontrado no desktop.")

if __name__ == "__main__":
    main()
