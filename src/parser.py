# coding: utf8
import sys
import os

from coleta import coleta_pb2 as Coleta

from headers_keys import (CONTRACHEQUE_MAY_20_FORWARD,
                          CONTRACHEQUE_APRIL_20_BACKWARD,
                          INDENIZACOES_MAY_20_FORWARD,
                          INDENIZACOES_APRIL_20_BACKWARD, HEADERS)
import number


def parse_employees(fn, chave_coleta, categoria, base):
    employees = {}
    counter = 1
    for row in fn:
        matricula = row[1]
        name = row[2]
        function = row[base[0]]
        location = row[base[1]]

        if name == "TOTAL":
            break
        if not number.is_nan(name) and not number.is_nan(matricula) and name != "0" and name != "Nome" and "Unnamed" not in name :
            membro = Coleta.ContraCheque()
            membro.id_contra_cheque = chave_coleta + "/" + str(counter)
            membro.chave_coleta = chave_coleta
            membro.nome = name
            membro.matricula = matricula
            membro.funcao = function
            membro.local_trabalho = location
            membro.tipo = Coleta.ContraCheque.Tipo.Value("MEMBRO")
            membro.ativo = True
            
            membro.remuneracoes.CopyFrom(
                cria_remuneracao(row, categoria)
            )
          
            employees[matricula] = membro
            counter += 1
            
    return employees


def cria_remuneracao(row, categoria):
    remu_array = Coleta.Remuneracoes()
    items = list(HEADERS[categoria].items())
    for i in range(len(items)):
        key, value = items[i][0], items[i][1]
        remuneracao = Coleta.Remuneracao()
        remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("R")
        remuneracao.categoria = categoria
        remuneracao.item = key
        # Caso o valor seja negativo, ele vai transformar em positivo:
        remuneracao.valor = float(abs(number.format_value(row[value])))

        if categoria == CONTRACHEQUE_MAY_20_FORWARD and value in [14, 15, 16, 17]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")
        elif categoria == CONTRACHEQUE_APRIL_20_BACKWARD and value in [13, 14, 15]:
            remuneracao.valor = remuneracao.valor * (-1)
            remuneracao.natureza = Coleta.Remuneracao.Natureza.Value("D")
        else: 
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("O")

        if categoria == CONTRACHEQUE_MAY_20_FORWARD and value in [5]:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")
        elif categoria == CONTRACHEQUE_APRIL_20_BACKWARD and value in [6]:
            remuneracao.tipo_receita = Coleta.Remuneracao.TipoReceita.Value("B")

        remu_array.remuneracao.append(remuneracao)

    return remu_array


def update_employees(fn, employees, categoria):
    for row in fn:
        matricula = row[1]
        if matricula in employees.keys():
            emp = employees[matricula]
            remu = cria_remuneracao(row, categoria)
            emp.remuneracoes.MergeFrom(remu)
            employees[matricula] = emp
    return employees


def parse(data, chave_coleta, month, year):
    employees = {}
    folha = Coleta.FolhaDePagamento()

    # Puts all parsed employees in the big map
    if (int(year) < 2020) or (int(month) <= 4 and year == "2020"):
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_APRIL_20_BACKWARD, [3, 5]))
        update_employees(data.indenizatorias, employees, INDENIZACOES_APRIL_20_BACKWARD)

    else:
        employees.update(parse_employees(data.contracheque, chave_coleta, CONTRACHEQUE_MAY_20_FORWARD, [3, 4]))
        update_employees(data.indenizatorias, employees, INDENIZACOES_MAY_20_FORWARD)

    for i in employees.values():
        folha.contra_cheque.append(i)
    return folha
