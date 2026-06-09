import asyncio
from unittest import result
from crawl4ai import AsyncWebCrawler
from bs4 import BeautifulSoup
import re
import pandas as pd
import re
import time

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

#Extrair todos os ingredientes de cada receita individualmente
def extrair_detalhes_receita(html):

    soup = BeautifulSoup(html, "html.parser")

    # INGREDIENTES
    ingredientes = []

    for li in soup.find_all(
        "li",
        class_=re.compile(
            r"(ingredient|ingrediente|p-ingredient|ingredient-item)",
            re.I
        )
    ):
        span = li.find("span")

        if span:
            ingredientes.append(span.get_text(strip=True))
        else:
            ingredientes.append(li.get_text(" ", strip=True))

    # PREPARO
    preparo = []

    lista_passos = soup.find("ol")

    if lista_passos:
        for item in lista_passos.find_all(
            "li",
            class_="recipe-steps-item"
        ):
            p = item.find("p")

            if p:
                preparo.append(p.get_text(strip=True))

    # CATEGORIA
    categoria = None

    categoria_tag = soup.find(
        "a",
        class_="u-some-link",
        href=lambda href: href and "/categorias/" in href
    )

    if categoria_tag:
        categoria = categoria_tag.get_text(strip=True)
        categoria = categoria.replace("Receitas ", "")

    # RENDIMENTO
    rendimento = None

    head = soup.find(
        "h2",
        string=lambda t: t and "Ingredientes" in t
    )

    if head:

        texto = head.get_text(" ", strip=True)

        match = re.search(
            r"\((\d+)\s*por",
            texto.lower()
        )

        if match:
            rendimento = int(match.group(1))

    return {
        "ingredientes": ingredientes,
        "preparo": preparo,
        "categoria": categoria,
        "rendimento": rendimento
    }
async def main():
    inicio = time.time()

    dados = []
    receitas_puladas = 0
    proximo_backup = 1000

    # percorre todas as páginas
    for bloco_inicio in range(3935, 13229, 100): #13228 é o total
        #começando de 3935 que e onde ocorreu o erro

     
        bloco_fim = min(bloco_inicio + 100, 13229)

        print(f"\nProcessando páginas {bloco_inicio} até {bloco_fim - 1}")

        # cria um crawler novo para cada bloco de 100 páginas
        async with AsyncWebCrawler() as crawler:

            for i in range(bloco_inicio, bloco_fim):

                url_base = f"https://www.tudogostoso.com.br/receitas?page={i}"

                await asyncio.sleep(0.5)

                try:
                    result = await crawler.arun(url=url_base)

                    if not result or not result.html:
                        receitas_puladas += 1
                        continue

                except Exception as e:
                    receitas_puladas += 1
                    print(f"Erro na página {url_base}: {e}")
                    continue

                links = extrair_links_receitas(result.html)

                for titulo, link_receita, rating in links:

                    print(link_receita)

                    try:
                        result_receita = await crawler.arun(
                            url=link_receita
                        )

                        if not result_receita or not result_receita.html:
                            receitas_puladas += 1
                            continue

                    except Exception as e:
                        receitas_puladas += 1
                        print(f"Erro na receita {link_receita}: {e}")
                        continue

                    try:
                        detalhes = extrair_detalhes_receita(result_receita.html)

                    except Exception as e:
                        receitas_puladas += 1
                        print(f"Erro ao processar {link_receita}: {e}")
                        continue

                    dados.append({
                        "titulo": titulo,
                        "ingredientes": "\n".join(
                            detalhes["ingredientes"]
                        ),
                        "preparo": "\n".join(
                            detalhes["preparo"]
                        ),
                        "url": link_receita,
                        "rating": rating,
                        "categoria": detalhes["categoria"],
                        "rendimento(porcoes)": detalhes["rendimento"]
                    })

                    # backup periódico
                    if len(dados) >= proximo_backup:

                        pd.DataFrame(dados).to_excel("backup_2.xlsx",index=False)


                        proximo_backup += 1000

    fim = time.time()

    print(f"Tempo de execução: {fim - inicio:.2f} segundos")

    print(f"Receitas coletadas: {len(dados)}")

    print(f"Receitas puladas: {receitas_puladas}")

    df = pd.DataFrame(dados)

    df.to_excel("receitas.xlsx",index=False)

asyncio.run(main())