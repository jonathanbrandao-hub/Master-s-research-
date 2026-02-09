import asyncio
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import pandas as pd
import re
async def main():
    receitas = []
    async with AsyncWebCrawler() as crawler:
        for i in range (1,2):
            url = f"https://www.tudogostoso.com.br/receitas?page={i}"
            result = await crawler.arun(url=url)
            soup = BeautifulSoup(result.html, "html.parser")
            # Find the section of recent recipes
            span_recentes = soup.find("span", string="Receitas recentes")
            recentes_container = None
            if span_recentes:
                recentes_container = span_recentes.find_parent().find_parent()

            avaliacoes = []
            numero_avaliacao = None

            # Extract all cards
            for card in soup.find_all("div", class_="card"):
            # Skip if the card is inside the recent section 
                if recentes_container and recentes_container.find_all("div", class_="card") and card in recentes_container.find_all("div", class_="card"):
                    continue

            # gets title
                titulo_tag = card.find("a", href=True)
                titulo = titulo_tag.get_text(strip=True) if titulo_tag else None
            # gets ratings
                rating_tag = card.find("span", class_="rating-votes")
                if rating_tag:
                    avaliacao = rating_tag.get_text(strip=True) 
                    numero = re.search(r"[\d.]+", avaliacao)  # converting numbers and dots
                    if numero:
                        numero_limpo = numero.group().replace(".", "")  # remove dots
                        numero_avaliacao = int(numero_limpo)
                if titulo and numero_avaliacao:
                    avaliacoes.append(f"{titulo} - {numero_avaliacao}")
                    receitas.append((titulo, numero_avaliacao))
                    

            '''print("Avaliações filtradas da lista principal (excluindo recentes):")
            for item in avaliacoes:
                print(f" - {item}")'''
    # Create the data frame with pandas 
    df = pd.DataFrame(receitas, columns=["Title", "ratings"])
    # transform the data Frame into an excel file
    #df.to_excel("dados.xlsx", index = False)
    print(df)
asyncio.run(main())