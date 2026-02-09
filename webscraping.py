import asyncio
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url='https://www.tudogostoso.com.br/receitas?page=2')
        print(result.html)
        '''from bs4 import BeautifulSoup
        soup = BeautifulSoup(result.html, "html.parser")
        receitas = soup.select("article.recipe-card")
        for receita in receitas:
            titulo = receita.select_one("h2.recipe-card__title")
            avaliacoes = receita.select_one(".rating__count")
            
            titulo_text = titulo.get_text(strip=True) if titulo else "Sem título"
            avaliacoes_text = avaliacoes.get_text(strip=True) if avaliacoes else "Sem avaliações"
            
            print(f"{titulo_text} — {avaliacoes_text}")'''

asyncio.run(main())