import requests
import pathlib
import sys
import os

BASE_URL = "https://transparencia.mpmg.mp.br/db_form/contracheque/"

# Generate endpoints able to download
def links_remuneration(month, year):
    links_type = {}
    link = ""
    if (int(year) < 2020) or (int(month) <= 4 and year == "2020"):
        link = (
            BASE_URL
            + "remuneracao_auxilios_membros_ativos?year="
            + year
            + "&month="
            + month
            + "&format=html&position=membro&status=ativo"
        )
    else:
        link = (
            BASE_URL
            + "res2002019/remuneracao_auxilios_membros_ativos?year="
            + year
            + "&month="
            + month
            + "&format=html&position=membro&status=ativo"
        )

    links_type["Membros ativos"] = link
    return links_type


def links_other_funds(month, year):
    links_type = {}
    link = ""
    if year == "2018" or (month == "02" and year == "2019"):
        link = (
            BASE_URL
            + "auxilios?year="
            + year
            + "&month="
            + month
            + "&format=html&status=ativo&name=undefined&numInitial=undefined&interval="
        )
    elif month != "02" and year == "2019" or (int(month) <= 4 and year == "2020"):
        link = (
            BASE_URL
            + "auxilios?year="
            + year
            + "&month="
            + month
            + "&format=html&status=ativo"
        )
    else:
        link = (
            BASE_URL
            + "res2002019/auxilios?year="
            + year
            + "&month="
            + month
            + "&format=html&status=ativo"
        )

    links_type["Membros ativos"] = link
    return links_type


def download(url, file_path):
    try:
        response = requests.get(url, allow_redirects=True)
        with open(file_path, "wb") as file:
            file.write(response.content)
        file.close()
    except Exception as excep:
        sys.stderr.write(
            f"Não foi possível fazer o download do arquivo: {file_path}. O seguinte erro foi gerado: {excep}"
        )
        sys.exit(1)


# Crawl retrieves payment files from MPM.
def crawl(year, month, output_path):
    urls_remuneration = links_remuneration(month, year)
    urls_other_funds = links_other_funds(month, year)
    files = []

    for element in urls_remuneration:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name = f"membros-ativos-contracheque-{month}-{year}.html"
        file_path = output_path + "/" + file_name
        download(urls_remuneration[element], file_path)
        files.append(file_path)

    for element in urls_other_funds:
        pathlib.Path(output_path).mkdir(exist_ok=True)
        file_name_indemnity = (
            f"membros-ativos-verbas-indenizatorias-{month}-{year}.html"
        )

        file_path_indemnity = output_path + "/" + file_name_indemnity
        download(urls_other_funds[element], file_path_indemnity)
        files.append(file_path_indemnity)

    return files
