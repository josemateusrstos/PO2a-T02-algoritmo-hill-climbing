import time
import os
from TRAB_2_HC import resolve_instancia
from datetime import datetime

# Roda a meta-heurística para as instancias teste
def roda_testes():
    # GERA TODAS AS INSTANCIAS
    lista_arquivos = os.listdir("Instancias_testes")
    lista_arquivos.sort()
    # Processa todos os arquivos
    qtd_iteracoes = 5
    registro = list()
    for instancia in lista_arquivos:
        # Cria o caminho completo para os arquivos de instância, solução e relatório
        arq_instancia = os.path.join("Instancias_testes", instancia)
        arq_solucao = os.path.join("Solucoes_testes", instancia)
        arq_relatorio = os.path.join("Relatorios_testes", instancia)
        # Lê a quantidade de jobs do arquivo
        with open(arq_instancia, "r", encoding="utf8") as f:
            # Lê todas as linhas do arquivo
            linhas = f.readlines()
            jobs = int(linhas[0].strip().split(";")[1])
        # Define a quantidade de iterações dependendo da quantidade de jobs
        if jobs == 25:
            qtd_iteracoes = 5
        if jobs == 50:
            qtd_iteracoes = 5
        if jobs == 100:
            qtd_iteracoes = 5
        if jobs == 150:
            qtd_iteracoes = 5
        if jobs == 200:
            qtd_iteracoes = 5
        if jobs == 300:
            qtd_iteracoes = 5
        # Roda o resolve_instancia para cada instancia testada
        # print(f"Arquivo:", arq_instancia)
        # print(f"Início:", datetime.now())
        t0 = time.time()
        resolve_instancia(arq_instancia, arq_solucao, arq_relatorio, qtd_iteracoes)
        t1 = time.time()
        # print(f"Tempo total em segundos:", round(t1 - t0, 2))
        print("____________________")
        registro.append([arq_instancia, round(t1 - t0, 2)])

    # print("-------------------------")
    for i in range(len(registro)):
        print(registro[i][1])


def solucoes_csv():
    lista_arquivos = os.listdir("Solucoes_testes")
    lista_arquivos.sort()
    solucoes = list()
    for instancia in lista_arquivos:
        arq_solucao = os.path.join("Solucoes_testes", instancia)
        with open(arq_solucao, "r", encoding="utf8") as f:
            arq = f.readlines()
            solucoes.append(float(arq[0].strip().split(";")[1]))


    for i in range(len(solucoes)):
        print(solucoes[i])



if __name__ == "__main__":

    roda_testes()

    # a = False
    # for i in range(5):
    #     print(a)
    #     if a == False:
    #         print(i)
    #         for j in range(3):
    #             print(j)
    #             if j == 0:
    #                 a = True
    #                 break
    #
    #
    # a = 100
    # b = 95
    #
    # if (b/a) <= 0.95:
    #     print(b/a)
