import math
import random as rnd
import time

# LÊ OS DADOS DE UM ARQUIVO INSTANCIA
def le_dados_instancia(arq_instancia):
    with open(arq_instancia, "r", encoding="utf8") as f:
        # Lê todas as linhas do arquivo
        linhas = f.readlines()
        # Lê qtd_jobs e qtd_maqs nas linhas 0 e 1
        qtd_jobs = int(linhas[0].strip().split(";")[1])
        qtd_maqs = int(linhas[1].strip().split(";")[1])
        del linhas[:3]
        # Lê as distancias
        mat_principal = list()
        for i in range(qtd_jobs):
            v_linha0 = linhas[i].strip().split(";")
            v_linha = v_linha0
            for j in range(len(v_linha0)):
                if j==1:
                    v_linha[j] = float(v_linha0[j])
                else:
                    v_linha[j] = int(v_linha0[j])
            mat_principal.append(v_linha)
    # Retorno das variaveis
    return qtd_jobs, qtd_maqs, mat_principal

# CALCULA A PROBABILIDADE ACUMULADA CONSIDERANDO OS PESOS
def prob_acumulada(mat_jobs):
    # Define o expoente para aumentar a probabilidade dos maiores e diminuir a dos pesos menores
    exp = 50
    # Define a soma dos pesos elevados ao expoente definido acima
    soma_pesos_exp = sum(math.pow(mat_jobs[i][1], exp) for i in range(len(mat_jobs)))
    # Gera valores de probabilidade de acordo com o peso
    # dividindo o peso elevado ao expoente pela soma dos pesos elevados
    prob_total = [math.pow(mat_jobs[i][1], exp) / soma_pesos_exp for i in range(len(mat_jobs))]
    # print("--prob total--")
    # print(prob_total)
    # Gera a lista de probabilidade acumulada
    prob_acumulada = list(range(len(prob_total)))
    for i in range(len(prob_total)):
        if i == 0:
            prob_acumulada[i] = prob_total[i]
        else:
            prob_acumulada[i] = prob_acumulada[i-1] + prob_total[i]
    # Adiciona referencia ao numero do job correspondente na lista de probabilidade acumulada
    for i in range(len(prob_total)):
        prob_acumulada[i] = [prob_acumulada[i], mat_jobs[i][0]]

    return prob_acumulada

# GERA SOLUÇÃO ALEATÓRIA
def solucao_aleatoria(mat_principal, qtd_jobs):
    mat_jobs = mat_principal.copy()
    sol = list(range(qtd_jobs))
    # Itera para cada Job do problema
    for i in range(qtd_jobs):
        # Gera para cada iteração um numero aleatorio
        prob = prob_acumulada(mat_jobs)
        # print(prob)
        r = rnd.random()
        # print(r)
        # Verifica qual o job sorteado
        for j in range(len(mat_jobs)):
            if r < prob[j][0]:
                sol[i] = prob[j][1]
                idx = j
                # Ao encontrar o sorteado, sai do loop
                break
        # Remove o job sorteado da lista de jobs disponíveis para sorteio
        del(mat_jobs[idx])
    return sol

# GERA UMA QTD DEFINIDA DE SOL ALEAT. E RETORNA A MELHOR ENTRE AS GERADAS
def melhor_solucao_aleatoria(qtd_vezes_gera_solucao, mat_principal, qtd_jobs):
    melhor_sol = list()
    melhor_ttp = 0
    for i in range(qtd_vezes_gera_solucao):
        # Retorna a solução aleatória gerada
        sol = solucao_aleatoria(mat_principal, qtd_jobs)
        # Retorna o tempo total ponderado da solução dada
        ttp = calcula_valor_solucao(sol, mat_principal)
        # Caso seja a primeira solucao gerada, define ela como parâmetro de comparação
        if i == 0:
            melhor_sol = sol
            melhor_ttp = ttp
        else: # Para as outras iterações, verifica se tem ttp menor que a melhor atual
            if ttp < melhor_ttp: # se for, define a solucao atual como a melhor para comparação
                melhor_ttp = ttp
                melhor_sol = sol
    return melhor_sol, melhor_ttp

# CALCULA O TEMPO TOTAL PONDERADO DE DETERMINADA SOLUÇÃO
def calcula_valor_solucao(solucao, mat_principal):
    mat_solucao = list()
    # print(solucao)
    qtd_maqs = len(mat_principal[0])-2
    # Itera para cada maquina, para preencher a matriz de tempos de terminos
    for maq in range(qtd_maqs):
        if maq == 0: # Se for a máquina 0, preenche com os valores da mat_principal, somando o anterior
            for job in range(len(mat_principal)):
                if job == 0:
                    mat_solucao.append(mat_principal[solucao[job]][2])
                else:
                    mat_solucao.append(mat_principal[solucao[job]][2]+mat_solucao[job-1])
        else: # para maquinas de 1 a n
            for job in range(len(mat_principal)): # para cada job
                if job==0: # se for o job 0, preenche a primeira linha das maqs1..maqn, copiando e somando os valores
                    if type(mat_solucao[job]) is int:
                        mat_solucao[job] = [mat_solucao[job], (mat_principal[solucao[job]][maq + 2] + mat_solucao[job])]
                    else:
                        mat_solucao[0].append((mat_principal[solucao[job]][maq + 2]+mat_solucao[job][-1]))
                else: # se não for o job 0
                    # comparar
                    if maq==1: # se for a maq 1
                        acima = mat_solucao[job-1][maq]
                        lado = mat_solucao[job]
                        if lado >= acima: #45 x 39
                            mat_solucao[job] = [mat_solucao[job], mat_solucao[job] + mat_principal[solucao[job]][maq+2]]
                        else:
                            mat_solucao[job] = [mat_solucao[job], mat_solucao[job-1][maq] + mat_principal[solucao[job]][maq + 2]]
                    else: # quanto não é a maq1
                        acima = mat_solucao[job-1][maq]
                        lado = mat_solucao[job][maq-1]
                        if lado >= acima:
                            mat_solucao[job].append(mat_solucao[job][-1] + mat_principal[solucao[job]][maq+2])
                        else:
                            mat_solucao[job].append(mat_solucao[job-1][maq] + mat_principal[solucao[job]][maq+2])

    # Realiza o produto dos pesos dos jobs com o tempo de finalização na ultima maquina de cada um deles
    total = 0
    # print(mat_solucao)
    # print()
    # print(mat_principal)
    for i in range(len(mat_principal)):
        total += (mat_principal[solucao[i]][1] * mat_solucao[i][-1])
        # print(f"",mat_principal[i][1],";", mat_solucao[i][-1])
        # print(mat_solucao[i])

    tempo_total_ponderado = total

    return(tempo_total_ponderado)

#GERA VIZINHOS E RETORNA O MELHOR
def gera_vizinhos(sol, mat_principal):
    melhor_vizinho = []
    melhor_vizinho_valor = float("inf")
    # Gera todas as soluções candidatas e verifica se são melhores que a atual
    qtd_jobs = len(mat_principal)
    for i in range(qtd_jobs - 1):
        for j in range(i, qtd_jobs):
            # print(i, j)
            # Faz uma cópia da solução original e realiza a troca
            # print(i,j)
            sol_candidata = sol[:]
            sol_candidata[i] = sol[j]
            sol_candidata[j] = sol[i]
            # Calcula o custo da solução candidata
            sol_candidata_valor = calcula_valor_solucao(sol_candidata, mat_principal)

            print(sol_candidata)

            # Verifica se é maior que o melhor vizinho atual
            if sol_candidata_valor < melhor_vizinho_valor:
                melhor_vizinho = sol_candidata
                melhor_vizinho_valor = sol_candidata_valor

    return melhor_vizinho, melhor_vizinho_valor

#GERA VIZINHOS E RETORNA O PRIMEIRO QUE SEJA AO MENOS 0.5% MELHOR
def gera_vizinhos_first(sol, mat_principal):
    # Gera todas as soluções candidatas e retorna a primeira que for melhor que a original
    qtd_jobs = len(mat_principal)
    # Indicador se a solução encontrada é melhor que a atual
    melhor = False
    for i in range(qtd_jobs - 1):
        if melhor == False:
            for j in range(i, qtd_jobs):
                # Faz uma cópia da solução original e realiza a troca
                sol_candidata = sol[:]

                sol_candidata[i] = sol[j]
                sol_candidata[j] = sol[i]
                # Calcula o custo da solução candidata
                sol_candidata_valor = calcula_valor_solucao(sol_candidata, mat_principal)
                # Na primeira iteração, atribui a ela o título de melhor para que seja possível a comparação
                if i==0 and j==0:
                    melhor_vizinho_valor = sol_candidata_valor
                    melhor_vizinho = sol_candidata
                # Verifica se é ao menos 0.5% melhor que o melhor atual
                # Caso seja melhor, já sairemos do loop para diminuir o tempo de processamento
                if (sol_candidata_valor/melhor_vizinho_valor) <= 0.995:
                    melhor_vizinho = sol_candidata
                    melhor_vizinho_valor = sol_candidata_valor
                    melhor = True
                    break

    return melhor_vizinho, melhor_vizinho_valor


if __name__ == "__main__":

    arq_instancia = "Instancias_testes/teste_artigo.csv"
    qtd_jobs, qtd_maqs, mat_principal = le_dados_instancia(arq_instancia)
    sol, ttp = melhor_solucao_aleatoria(100, mat_principal, qtd_jobs)
    # print(sol, round(ttp, 2))
    sol = [1,0,2,4,3]

    # melhor_sol, melhor_ttp = gera_vizinhos(sol, mat_principal)
    # print("----------")
    # print(melhor_sol, melhor_ttp)

    melhor_sol, melhor_ttp = gera_vizinhos_first(sol, mat_principal)
    print(melhor_sol, melhor_ttp)