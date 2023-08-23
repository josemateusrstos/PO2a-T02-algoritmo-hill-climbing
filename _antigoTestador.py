from TRAB_2_HC import resolve_instancia
import os

# GERA SOLUÇÕES PARA TODAS AS INSTANCIAS DA PASTA
def gera_todas_solucoes():
    # GERA TODAS AS INSTANCIAS
    lista_arquivos = os.listdir("Instancias")
    lista_arquivos.sort()
    # Processa todos os arquivos
    for instancia in lista_arquivos:
        # Cria o caminho completo para os arquivos de instância e solução
        arq_instancia = os.path.join("Instancias", instancia)
        arq_solucao = os.path.join("Solucoes", instancia)
        # Efetivamente resolve a instância e salva a solução
        resolve_instancia(arq_instancia, arq_solucao, 0, 0)

# REALIZA O BENCHMARKING
def benchmark():
    lista_arquivos = os.listdir("Instancias")
    lista_arquivos.sort()
    # Processa todos os arquivos
    gera_todas_solucoes()
    solucoes = list()
    bench = list()
    pior = list()
    for instancia in lista_arquivos:
        # Cria o caminho completo para os arquivos de solucao geradas e do parametro para o benchmark
        arq_solucao = os.path.join("Solucoes", instancia)
        arq_solucao_benchmark = os.path.join("Solucoes_Benchmark", instancia)
        arq_solucao_pior = os.path.join("Solucoes_Aleatorias", instancia)

        with open(arq_solucao, "r", encoding="utf8") as f:
            arq = f.readlines()
            solucoes.append(float(arq[0].strip().split(";")[1]))

        with open(arq_solucao_benchmark, "r", encoding="utf8") as f:
            arq = f.readlines()
            bench.append(float(arq[0].strip().split(";")[1]))

        with open(arq_solucao_pior, "r", encoding="utf8") as f:
            arq = f.readlines()
            pior.append(float(arq[0].strip().split(";")[1]))

    for i in range(len(solucoes)):
        print(solucoes[i])

    # print(bench)
    # print(pior)
    qpior = 0
    qmelhor = 0
    qac = 0

    for i in range(len(solucoes)):
        # print(f"Instancia", i, " - PIOR:",pior[i]," - SOL:", solucoes[i],"BENCH:",bench[i])
        if pior[i] <= solucoes[i]:
            # print("TA PIOR")
            qpior = qpior + 1
        else:
            if bench[i] >= solucoes[i]:
                # print("MELHOR QUE O BENCH")
                qmelhor = qmelhor + 1
            else:
                # print("OK")
                qac = qac + 1

    print("----------------------------")
    print(f"Piores que o aleatório: ", qpior,"\nMelhores ou iguais às ótimas:", qmelhor,"\nEntre a ótima e a pior:", qac)


    porc_bench = list()
    porc_pior = list()

    for i in range(len(bench)):
        porc_bench.append(solucoes[i]/bench[i])
        porc_pior.append(solucoes[i]/pior[i])

    porcentagem_otimas = ((sum(porc_bench))/(len(porc_bench))-1)*100
    porcentagem_piores = ((sum(porc_pior)/(len(porc_pior)))-1)*100

    print(f"Relação com as ótimas:",porcentagem_otimas,"(menor é melhor)\nRelação com as aleatórias:",porcentagem_piores,"(mais negativo é melhor)")

if __name__ == "__main__":

    benchmark()