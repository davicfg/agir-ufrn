import requests
from bs4 import BeautifulSoup
import csv

tipo_protecao='patentes'
# Arquivo com os links
with open(f'links-{tipo_protecao}.txt', 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

# Nome do arquivo de saída
output_file = f'{tipo_protecao}.csv'

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    for url in urls:
        print(f'Processando {url}')
        response = requests.get(url)

        if response.status_code != 200:
            print(f'Erro ao acessar {url}')
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        container = soup.find(class_='ctn-conteudo-interno')

        if not container or 'O item não foi encontrado na área Patentes...' in soup.text:
            print(f'Conteúdo não encontrado em {url}')
            continue

        # Pega o texto de cada tag filha direta do container
        colunas = [tag.get_text(strip=True) for tag in container.find_all(recursive=False)]
        colunas.append(url)
        print(colunas)
        writer.writerow(colunas)
