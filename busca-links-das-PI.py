import requests
from bs4 import BeautifulSoup
import time

tipo_protecao = 'programas'
base_url = f'https://agir.ufrn.br/vitrine/{tipo_protecao}?page='
page = 1
links_coletados = []

while True:
    url = f'{base_url}{page}'
    print(f'Acessando {url}')
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f'Erro ao acessar página {page}, código {response.status_code}')
        break

    soup = BeautifulSoup(response.text, 'html.parser')

    # Verifica se a página contém a mensagem de fim
    if 'Nenhum resultado foi encontrado.' in soup.text:
        print('Nenhum resultado encontrado. Encerrando.')
        break

    # Encontra todos os links que contêm "patentes/" no href
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if f'{tipo_protecao}/' in href and href not in links_coletados:
            links_coletados.append(href)
            print(f'https://agir.ufrn.br/vitrine/{href}')

    page += 1
    time.sleep(1)  # Boa prática para evitar sobrecarregar o servidor

# Resultado final
print(f'\nTotal de links encontrados: {len(links_coletados)}')