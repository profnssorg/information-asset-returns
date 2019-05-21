# Importacao de bibliotecas

# separa as noticias que interessam
def separar_noticias(arq, palavras):
    arquivo = open(arq)
    lista = []
    for linha in arquivo.readlines():
        achou = False
        for palavra in palavras:
            if achou == False:
                if (palavra.lower() in linha.lower()[:linha.find('link')]) == True:
                    lista.append(linha[1:-3])
                    achou == True
    return(lista)
    arquivo.close()

# pegar as letras com acento das noticias e trasnformar o grupo de caracteres
# que as representam nas letras com acento
def transformar(lista):
    final = []
    asci = ['$', ';', '%', '\\u00f4', '\\u00f5', '\\u00e1', '\\u00e0', '\\u00e3', '\\u00e2', '\\u00e9', '\\u00ea', '\\u00ed', '\\u00f3', '\\u00fa', '\\u00e7']
    utf = ['\\$', ',', ' por cento', 'ô', 'õ', 'á', 'à', 'ã', 'â', 'é', 'ê', 'í', 'ó', 'ú', 'ç']
    for noticia in lista:
        a = noticia
        ja = False
        for i in range(len(asci)):
            if ja == False:
                a = noticia.replace(asci[i], utf[i])
                ja = True
            else:
                a = a.replace(asci[i], utf[i])
                ja = True
        final.append(a)
    return(final)