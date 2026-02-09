import pandas as pd
from collections import Counter
import re

def split_word(item):#separar quando vem dois ingredientes juntos
    return re.split(r'\s+(?:e|com)\s+', item)

def normalizar(texto): #normalizar vou tirar as palavras em excesso
    texto = texto.lower()
    padroes = [
    r"\d+\/\d+",   # frações (1/2, 3/4)
    r"\d+",        # números
    r"\(.*?\)",    # parenteses (chá), (sopa)
]
    medidas = ["separados","xícaras", "xícara", "colheres", "colher","chá","sopa","caixinha","pitadas","pitada","copos","copo", "sem pele e sem sementes",
               "caixas", "caixa", "a gosto","litros", "litro", "garrafa","pequena","pequeno","cubos", "cobertura","calda", "pacote",
               "bem cheia","medida da lata","lata ","kg", "g ","cortados em", "cortado em", "cortadasem","cortada em", "picadas ou raladas", "picada ou ralada", "picadas", "picada", "picados","picada", "picado",
               "picadinhas", "picadinhos","picadinho", "picadinha","raladas","ralada","ralado", "inteiros", "médias", "média", "sem caroços", "sem caroço","fatiados","fatiadas", "fatiada","fatiado", "peitos", "peito", "desfiados",
               "desfiado", "vaca", "com soro","moídas","moída", "ml", "amassados", "amassado", "sem sal", "sem pele", "peles", "pele", "integral",
               "sementes", "sem semente", "em pau","padaria","grossa", "mornas","morna", "mornos","morno","quente", "morna","natural", "gelada", "dentes","dente", "puro " ,"tabeltes", "grandes","grande", "por minutos em panela de pressão",
               "para pão", "derretida", "derretido", "inteiro", "cortadas","na vertical" ,"na horizontal", "horizontal","vertical","para ","untar", "a forma", "polvilhar", "integral",
               "levemente", "batidos", "batido", "batida", "cozido", "tabletes","tablete", "cozida e amassada", "pincelar sobre massa", "medida", "fritar", 
               "recheio", "desossado", "rasas", "rasa", "tempero", "biológico", "químico", " por minutos em ",  "panela de pressão", "suco de", "por", "minutos em", 
               "em pó","branco","achocolatado ou", "em rodela", "em rodelas", "rodelas", "fatias","fatiados","fatiadas", "fatiado", "fatiada",  "oliva",
               "o quanto o bastante", "suficiente", ",sabor chocolate", "desnatado", "tira", "em pedaços","em pedaço"," esmagado", "sal dormido duro",
               "cristal", "vegetal", "cortados no meio", "torrado", "em fatia","temperatura ambiente", "filé de", "fresco", "bem","em quadradinhos","em quadradinho","quadradinho"
               "pote", "quanto bastante", "escorrida", "à vontade", "pincelar", "granulado colorido", "fervente", "crua", "cheia", "ao leite", "pedaços médios", "maço",
               "tira", "rodela", "espremido","enfeitar","refrigerante de laranja", "boa qualidade"," , o quanto baste, para molhar a bolacha", ", sabor chocolate", " decorar", " em ", "ou ", "de ", " e "
    ]
    # compostos que devem ser preservados
    compostos = ["creme de leite", "doce de leite", "óleo de coco", "leite de coco", "farinha de trigo", "extrato de tomate",
                 "molho de tomate", "amido de milho", "bis de limão", "caldo de galinha", "gema de ovo", "fermento de pão", "cheiro verde", "farinha de rosca", "óleo de soja", 
                 "massa de lasanha", "cheiro-verde", "bis de limão", "queijo ralado", "milho para pipoca", "achocolatado em pó ou chocolate", "chocolate em pó ou achocolatado"
                 "caldo de legumes","fermento químico em pó", "alho e sal", "essência de baunilha", "massa de lasanha", "caldo de bacon ou costela",
                 "suco em pó", "gelatina", "flocão de milho", "margarina ou manteiga", "pimentão verde", "folha de louro", "latas molho pronto de tomate",
                 "raspas de limão", "claras de ovo", "leite de moça", "leite moça", "raspas de limão", "lingüiça calabresa defumada", "pão de forma", "margarina ou manteiga",
                 "pão de sal dormidos duros", "milho verde", "pote de requeijão", 'cogumelos em conserva cortados ao meio', "caldo de carne"
    ]

    for i in compostos:
        if i in texto:
            return i   # já retorna normalizado

    for p in padroes:
        texto = re.sub(p, "", texto)
    for m in medidas:
        texto = texto.replace(m, "")
    
    texto = texto.strip()
    return texto

def lematizar (texto): #vou arrumar as palavras que estou no plural ou possuem mesmo significado
    plural_singular = {
    "ovos": "ovo","cenouras": "cenoura","tomates": "tomate","limões": "limão",
    "pães": "pão","cebolas": "cebola", "carnes": "carne","massas": "massa",
    "muçarela":"queijo","ervilhas":"ervilha","tomate": "tomate","fermento em pó":"fermento",
    "suco limão": "suco de limão", "gema ovo batido para a massa": "ovo", "fermento químico em pó": "fermento",
    "gema de ovo": "ovo", "banadas":"banana", "fermento de pão": "fermento químico", "queijo parmesão ralado": "queijo ralado","queijo parmesão": "queijo",
    "mussarela":"queijo", "margarina ou manteiga": "margarina", "chocolate bis":"chocolate", "milho verde":"milho", "requeijão cremoso": "queijo",
    "óleo de soja": "óleo", "cheiro-verde":"cheiro verde", "bis de limão": "chocolate", "chocolate granulado":"chocolate", 
    "achocolatado em pó": "chocolate", "fermento químico em pó": "fermento", "pimenta-do-reino":"pimenta", 
    "caldo de bacon ou costela": "caldo de carne", "coco ralado sem açúcar": "coco ralado", "achocolatado":"chocolate", "pimenta-do-reino":"pimenta", 
    "pimenta-de-cheiro":"pimenta", "trigo":"farinha de trigo", "clado carne":"caldo de carne", "claras de ovo": "ovo", "leite moça":"leite condensado", 
    "leite de moça":"leite condensado", "nescau":"chocolate", "açucar": "açúcar", "queijo mussarela":"queijo", "linguiça calabresa defumada":"porco", 
    "pão de forma":"pão", "chocolate em pó ou achocolatado":"chocolate", "pão de sal dormidos duros": "pão", "milho verde":"milho", "champignon": "cogumelo",
    "pote de requeijão":"queijo", "gema": "ovo", 'cogumelos em conserva cortados ao meio': "cogumelo","pimentão vermelho":"pimentão", "pimentão verde":"pimentão",
    "pimentão amarelo":"pimentão", "pimentões verdes": "pimentão", "latas leite condensado":"leite condensado", "latas molho pronto de tomate":"molho de tomate","carne  ":"carne",
    "massa de lasanha": "macarrão", "parafuso": "macarrão", "espaguete":"macarrão", "chocolate meio amargo":"chocolate", "mussarela  quadradinho": "queijo"

}
    #assumi todos os queijos como queijo
    #assumi qualquer suco como a fruta
    #assumi qualquer tipo de chocolate como chocolate
    #assumi que margarina ou manteiga a pessoa vai escolher margarina
    # Se estiver no dicionário, retorna o singular
    if texto in plural_singular:
        return plural_singular[texto]
    # fallback de regras
    if texto.endswith("s "):
        return texto[:-2]
    if texto.endswith("ões"):
        return texto[:-3] + "ão"
    if texto.endswith("ães"):
        return texto[:-3] + "ão"
    if texto.endswith("es") and len(texto) > 3:
        if texto == "verdes":
            return texto
        return texto[:-1]
    if texto.endswith("s") and len(texto) > 3:
        if texto == "brócolis":
            return texto
        return texto[:-1]

    return texto
# Carrega a planilha (#teste com apenas 10 itens)
df = pd.read_excel("ingredientes.xlsx")

todos_ingredientes = []

for receita in df['ingredientes']:
    if pd.isna(receita):
        continue
    linhas = receita.split("\n")  # separa por quebra de linha
    for item in linhas:
        item = item.strip().lower()
        if item:
            todos_ingredientes.append(item)

# 1. Quantos ingredientes no total
total_ingredientes = len(todos_ingredientes)
print("Total de ingredientes:", total_ingredientes)

#identificar item que se perdeu no caminho (primeira análise foi só a 'corbertura' ent tudo bem)
sumidos = []
for i in todos_ingredientes:
    n = normalizar(i)
    if not n:
        sumidos.append(i)

print("Itens perdidos no normalizar:", sumidos)
print("Total perdidos:", len(sumidos))
# 2. Contagem de tipos (ainda bruto)
#normalizados = [normalizar(i) for i in todos_ingredientes if normalizar(i)]
normalizados = []
for i in todos_ingredientes:
    n = normalizar(i)
    if not n:
        continue
    # aqui entra o split_coord
    partes = split_word(n)
    for p in partes:
        p = p.strip()
        if p:
            normalizados.append(p)
lematizados = [lematizar(i) for i in normalizados]
contagem_normalizada = Counter(lematizados)
print("Total bruto:", len(todos_ingredientes))
print("Depois normalizar:", len(normalizados))
print("Depois lematizar:", len(lematizados))
print("Total no Counter:", sum(contagem_normalizada.values()))
print(contagem_normalizada)
print("Total de ingredientes únicos:", len(contagem_normalizada))

#tranformar em tabela
tabela = pd.DataFrame(contagem_normalizada.items(), columns=["ingrediente", "quantidade"])

#criar a planilha exceel
tabela.to_excel("Ingredientes_top100.xlsx")