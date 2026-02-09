import asyncio
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import json
import re

async def extrair_ingredientes_de_receita(receita_url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url=receita_url)
        soup = BeautifulSoup(result.html, "html.parser")
        ingredientes = []

# Como na inspeção do site eu constatei que a classe que contem o texto com os ingredientes é spans, vamos procurar por elementos <li class="..."> contendo spans
        for li in soup.find_all("li", class_=re.compile(r"(ingredient|ingrediente|p-ingredient|ingredient-item)", re.I)):
            span = li.find("span")
            if span and span.get_text(strip=True):
                ingredientes.append(span.get_text(strip=True))
            else:
                txt = li.get_text(" ", strip=True)
                if txt:
                    ingredientes.append(txt)

        if ingredientes:
            return ingredientes
# Debug: não encontrou nada — imprime trecho do HTML para inspeção
        snippet = (result.html[:4000] + "...") if len(result.html) > 4000 else result.html
        print(" Não foi possível localizar ingredientes com os seletores usados.")
        print("Trecho inicial do HTML para debug (até 4000 chars):\n")
        print(snippet)
        return ingredientes  # vazio
    
# definir função que extrai todos os métodos de preparo da receita e vamos armazenálo em uma lista
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
async def main():
    receita_url = "https://www.tudogostoso.com.br/receita/10254-fricasse-de-frango.html"  # substitua aqui
    ingredientes = await extrair_ingredientes_de_receita(receita_url)
    passos = await  extrair_modo_preparo(receita_url)
    print("\n=== Ingredientes encontrados ===")
    if not ingredientes:
        print("Nenhum ingrediente encontrado.")
    else:
        for ing in ingredientes:
            print("-", ing)
    print("\n=== Modo de Preparo ===")
    if not passos:
        print("Nenhum ingrediente encontrado.")
    else:
        for ing in passos:
            print("-", ing)
asyncio.run(main())