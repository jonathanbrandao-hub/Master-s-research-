import asyncio
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup

async def main():
    async with AsyncWebCrawler() as crawler:
        url = "https://www.tudogostoso.com.br/receitas?page=1"
        result = await crawler.arun(url=url)
        soup = BeautifulSoup(result.html, "html.parser")

        main_content = soup.find("main")

        # Encontra o span "Receitas recentes"
        span_recents = soup.find("span", string="Receitas recentes")

        # Se achar, sobe para o container pai que engloba essa seção
        recentes_container = None
        if span_recents:
            # Sobe 2 níveis, por exemplo, ajuste se precisar
            recentes_container = span_recents.find_parent()
            if recentes_container:
                recentes_container = recentes_container.find_parent()

        titulos = []
        for a_tag in main_content.find_all("a"):
            # Se o link estiver dentro da seção recentes, ignora
            if recentes_container and recentes_container.find_all("a") and a_tag in recentes_container.find_all("a"):
                continue

            texto = a_tag.get_text(strip=True)
            href = a_tag.get("href", "")
            if texto and "/receita/" in href:
                titulos.append(texto)

        print("Títulos filtrados da lista principal (excluindo recentes):")
        for t in titulos:
            print(f" - {t}")

asyncio.run(main())
'''async def main():
    async with AsyncWebCrawler() as crawler:
        url = "https://www.tudogostoso.com.br/receitas?page=2"
        result = await crawler.arun(url=url)
        soup = BeautifulSoup(result.html, "html.parser")
        receitas = soup.select("card card-recipe is-video is-row")
        titulos = []
        for receita in receitas:
            titulo = receita.select_one("h2.card-title a")
            titulo_text = titulo.get_text(strip=True) if titulo else "Sem título"
            titulos.append(titulo_text)
        print("Títulos das receitas na página 2:")
        for t in titulos:
            print(f" - {t}")

asyncio.run(main())'''