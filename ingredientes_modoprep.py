import asyncio
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import re
import pandas as pd
import re
import time


async def extrair_ingredientes_de_receita(receita_url):
#Extrair todos os ingredientes de cada receita individualmente

    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=receita_url)
        soup = BeautifulSoup(result.html, "html.parser")

        # lista vazia que vamos inserir os ingredientes depois
        ingredientes = []

        #procurar a classe em que os ingredeintes estão contidos
        for li in soup.find_all("li", class_=re.compile(r"(ingredient|ingrediente|p-ingredient|ingredient-item)", re.I)):
            span = li.find("span")
            if span and span.get_text(strip=True):
                ingredientes.append(span.get_text(strip=True))
            else:
                txt = li.get_text(" ", strip=True)
                if txt:
                    ingredientes.append(txt)
                    
        # se a lista não está vazia, ou seja, é true, retorna a lista de ingredientes
        if ingredientes:
            return ingredientes

    
# definir função que extrai todos os métodos de preparo da receita e vamos armazenar em uma lista
async def extrair_modo_preparo(html):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=html)
        soup = BeautifulSoup(result.html, "html.parser")

    # Localiza a lista ordenada contendo os passos
    lista_passos = soup.find("ol")
    if not lista_passos:
        return []

    # Encontra todos os li com classe recipe-steps-item
    itens = lista_passos.find_all("li", class_="recipe-steps-item")

    passos = []
    for item in itens:
        # cada passo está dentro de <p>
        texto_tag = item.find("p")
        if texto_tag:
            passos.append(texto_tag.get_text(strip=True))

    return passos
#definir função que converte o tipo de texto que a avaliação esta contida
def parse_rating(texto):
    texto = texto.lower().strip()  # normaliza
    # captura números com ou sem decimal + opcional k
    match = re.search(r"(\d+(?:\.\d+)?)(k?)", texto)
    if not match:
        return None
    numero = float(match.group(1))
    sufixo = match.group(2)
    if sufixo == "k":
        numero *= 1000
    return int(numero)
#Se nao tiver rating a funcao retorna "0".

def extrair_links_receitas(html):
    soup = BeautifulSoup(html, "html.parser")
    container = soup.find("div", class_="grid card-listing")
    #tentenado extrair todas as receitas
    links_receitas = []
    ratings_receitas = []
    for a in container.find_all("a", class_="card-link"):
        href = a.get("href", "")
        titulo = a.get_text(strip=True)
    #tentando extrair os ratings junto
        numero_avaliacao = 0
        card = a.find_parent("div", class_="card")
        rating_tag = card.find("span", class_="rating-votes") if card else None
        if rating_tag:
            avaliacao = rating_tag.get_text(strip=True) 
            numero_avaliacao = parse_rating(avaliacao)
    # Garante que é uma receita verdadeira
        if "/receita/" in href:
            links_receitas.append((titulo, href, numero_avaliacao))

    return links_receitas

#definir função que extrai o rendimento da receita
async def extrair_rendimento(html):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=html)
        soup = BeautifulSoup(result.html, "html.parser")
        head = soup.find("h2", string=lambda t: t and "Ingredientes" in t)
        if not head:
            return None
        
        texto = head.get_text(" ", strip=True)
        
        match = re.search(r"\((\d+)\s*por", texto.lower())
        
        if match:
            rendimento = match.group(1)
            return rendimento

        return None

#definir função que extrai a categoria da receita
async def extrair_classe(html):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=html)
        soup = BeautifulSoup(result.html, "html.parser")
        categoria_tag = soup.find("a", class_ = "u-some-link", href = lambda href: href 
                                  and "/categorias/" in href)

        if categoria_tag:
            categoria = categoria_tag.get_text(strip=True)
            categoria = categoria.replace("Receitas ","")
            return categoria
        
        return None


async def main():
    inicio = time.time()
    dados = []
    time.sleep(1)
    for i in range (1,2):#13228 é o total
        url_base =  f"https://www.tudogostoso.com.br/receitas?page={i}"
        await asyncio.sleep(0.5)
        async with AsyncWebCrawler() as crawler:
            try:
                result = await crawler.arun(url=url_base)
            except Exception as e:
                print(f"Erro em {url_base}: {e}")
                continue
        #1 Encontrar os links presentes no site (apenas os desejados)
            links = extrair_links_receitas(result.html)
        #2Extrair título, ingredientes e modo de preparo de cada link
            for i in links:
                link_receita = i[1]
                print(f'O link da vez é {link_receita}')
                titulo = i[0]
                rating = i[2]
                ingredientes = await extrair_ingredientes_de_receita(link_receita)
                preparo = await extrair_modo_preparo(link_receita)
                categoria = await extrair_classe(link_receita)
                rendimento = await extrair_rendimento(link_receita)
        #Adicionar cada um como um dicionário 
                dados.append({
                        "titulo": titulo,
                        "ingredientes": "\n".join(ingredientes),
                        "preparo": "\n".join(preparo),
                        "url": link_receita,
                        "rating": rating,
                        "categoria": categoria,
                        "rendimento(porcoes)": rendimento})
    #Criar planilha
    fim = time.time()
    tempo_total = fim - inicio
    print(f"Tempo de execução: {tempo_total:.4f} segundos")
    
    df = pd.DataFrame(dados)

    
    print(df)
        

    # 3. Cria planilha Excel
    #df.to_excel("receitas_tudogostoso_class.xlsx")

    #print("\n Planilha criada com sucesso")

asyncio.run(main())

'''Sobre o modo de divisão das receitas: 
Talvez eu possa fazer que nem o livro Authentic Brazilian homecooking e dividir os pratos em 
*Categoria Carnes
-Bife
-Frango
-Porco
-Frutos do mar
*Vegetarianos
-No livro ela apresenta tanto como dishes e sides --> O maior problema seria em como Categorizar side dishes
*Rice and beans dishes
-Pratos em que o conteudo principal são o arroz e o feijão e o resto só entra como servings (por exemplo feijoada)
-Acredito que o virado a paulista não deveria estar aqui!!!
*Snacks
*Deserts

Sobre o dataset:
Posso usar a AIST primeiro e vasculhar se ela contem o ingrediente que é usado na receita, 
se sim eu pego dela, se não eu uso o outro dataset.

Para a apresentação joint meeting: Colocar um slide da netflix e amazon mostrando content-based e collaborative filtering
Ja temos 13226 receitas no site. 
Tem que ver como vamos lidar com as receitas que não tem avaliação, ou seja, rating = 0.

Preciso definir uma funcao que extraia o rendimento da receita e uma que extraia a categoria da receita.

 '''
