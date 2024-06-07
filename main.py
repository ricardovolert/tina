## --------------------------------------------------- ##
## Tina v.2.0.0 - Personal assistant                   ## 
## This is ricardovolert's (i.e. me) version of        ##
## fabrimatt's original project.                       ##
## Miniaturized design of an Alexa clone. It will help ##
## with temperature via Google, time and playing music ##
## on YouTube and searches using Google and Wikipedia. ##
## --------------------------------------------------- ##

'''
speech_recognition é usada para reconhecimento de voz.
pyttsx4 é usada para conversão de texto em fala.
datetime é usada para trabalhar com datas e horas.
wikipedia é usada para buscar resumos na Wikipedia.
pywhatkit é usada para tocar músicas no YouTube.
requests é usada para fazer requisições HTTP.
BeautifulSoup é usada para fazer parsing de HTML.
'''

import speech_recognition as sr
import pyttsx4
import datetime
import wikipedia
import pywhatkit
import requests
from bs4 import BeautifulSoup

# Função para converter número para texto
# numero_para_texto : converte um número em seu equivalente textual em português, 
# retornando uma string correspondente ao número fornecido.
def numero_para_texto(numero):
    numeros_texto = {
        0: 'zero', 1: 'um', 2: 'dois', 3: 'três', 4: 'quatro',
        5: 'cinco', 6: 'seis', 7: 'sete', 8: 'oito', 9: 'nove',
        10: 'dez', 11: 'onze', 12: 'doze', 13: 'treze', 14: 'catorze',
        15: 'quinze', 16: 'dezesseis', 17: 'dezessete', 18: 'dezoito',
        19: 'dezenove', 20: 'vinte', 21: 'vinte e um', 22: 'vinte e dois',
        23: 'vinte e três', 24: 'vinte e quatro', 25: 'vinte e cinco',
        26: 'vinte e seis', 27: 'vinte e sete', 28: 'vinte e oito',
        29: 'vinte e nove', 30: 'trinta', 31: 'trinta e um',
        32: 'trinta e dois', 33: 'trinta e três', 34: 'trinta e quatro',
        35: 'trinta e cinco', 36: 'trinta e seis', 37: 'trinta e sete',
        38: 'trinta e oito', 39: 'trinta e nove', 40: 'quarenta',
        41: 'quarenta e um', 42: 'quarenta e dois', 43: 'quarenta e três',
        44: 'quarenta e quatro', 45: 'quarenta e cinco', 46: 'quarenta e seis',
        47: 'quarenta e sete', 48: 'quarenta e oito', 49: 'quarenta e nove',
        50: 'cinquenta', 51: 'cinquenta e um', 52: 'cinquenta e dois',
        53: 'cinquenta e três', 54: 'cinquenta e quatro', 55: 'cinquenta e cinco',
        56: 'cinquenta e seis', 57: 'cinquenta e sete', 58: 'cinquenta e oito',
        59: 'cinquenta e nove'
    }
    return numeros_texto.get(numero, '')

# Define uma função obter_previsao_tempo_google que faz uma requisição ao Google 
# para obter a previsão do tempo de uma cidade específica, parseando o HTML da 
# resposta e retornando o objeto BeautifulSoup se a requisição for bem-sucedida.
def obter_previsao_tempo_google(cidade):
    url = f"https://www.google.com/search?q=previsão+do+tempo+{cidade.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    resposta = requests.get(url, headers=headers)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.content, "html.parser")
        return soup
    else:
        return None

# Define uma função analisar_previsao que extrai e retorna informações 
# detalhadas sobre a previsão do tempo a partir do HTML parseado.
def analisar_previsao(soup):
    cidade = soup.find("div", attrs={"id": "wob_loc"}).text
    tempo = soup.find("span", attrs={"id": "wob_dc"}).text
    temperatura = soup.find("span", attrs={"id": "wob_tm"}).text
    precipitação = soup.find("span", attrs={"id": "wob_pp"}).text
    umidade = soup.find("span", attrs={"id": "wob_hm"}).text
    vento = soup.find("span", attrs={"id": "wob_ws"}).text

    previsao_detalhada = {
        'cidade': cidade,
        'tempo': tempo,
        'temperatura': f"{temperatura}°C",
        'precipitação': precipitação,
        'umidade': umidade,
        'vento': vento
    }

    return previsao_detalhada

# Define uma função previsao_por_extenso que formata a previsão do tempo 
# detalhada em uma string descritiva.
def previsao_por_extenso(cidade, previsao_detalhada):
    descricao = f"Agora em {cidade} faz {previsao_detalhada['temperatura']}, {previsao_detalhada['tempo']} com umidade em {previsao_detalhada['umidade']} e ventos com velocidade de {previsao_detalhada['vento']}\n"
    return descricao

# Define uma função google_search que faz uma busca no Google por uma 
# query específica, remove elementos HTML desnecessários, extrai os 
# resultados relevantes e os retorna como uma lista de strings.
def google_search(query):
    url = f"https://www.google.com/search?q=texto+sobre+{query.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    resposta = requests.get(url, headers=headers)
    if resposta.status_code == 200:
        soup = BeautifulSoup(resposta.content, "html.parser")
        
        # Remove conteúdo da classe "I6Kpxd XNfAUb z1Mm0e"
        for element in soup.find_all(class_="I6Kpxd XNfAUb z1Mm0e"):
            element.decompose()

        # Extrai conteúdo das classes "hgKElc" e "f5cPye"
        results = []
        for element in soup.find_all(class_="hgKElc"):
            results.append(element.get_text(strip=True))
        for element in soup.find_all(class_="f5cPye"):
            results.append(element.get_text(strip=True))
        
        return results
    else:
        return []

# Inicializa o reconhecedor de áudio (audio) e o conversor de texto para fala (maquina).
audio = sr.Recognizer()
maquina = pyttsx4.init()

# Listar e configurar a voz desejada: Comentado, mas pode ser usado para listar e 
# configurar a voz desejada para a conversão de texto para fala.
# voices = maquina.getProperty('voices')
# for voice in voices:
#    print(f"ID: {voice.id}\nName: {voice.name}\nLanguage: {voice.languages}")
# Escolher a voz (substitua pelo ID da voz desejada)
# maquina.setProperty('voice', voices[0].id)  # Exemplo: setar para a primeira voz disponível

# Define a função executa_comando que ouve um comando de voz, 
# reconhece o texto usando a API do Google e, se o comando 
# contiver "tina", remove essa palavra e repete o comando.
def executa_comando():
    comando = ""  # Inicializa a variável comando
    try:
        with sr.Microphone() as source:
            print('Ouvindo...')
            voz = audio.listen(source)
            comando = audio.recognize_google(voz, language='pt-BR')
            comando = comando.lower()
            if 'tina' in comando:
                comando = comando.replace('tina', '')
                maquina.say(comando)
                maquina.runAndWait()
    except:
        print('Microfone não está ok')
    return comando

# Define a função comando_voz_usuario que executa diferentes 
# ações com base no comando de voz recebido, incluindo:
# - Dizer a hora atual.
# - Fazer uma pesquisa na Wikipedia.
# - Fazer uma pesquisa no Google.
# - Obter a previsão do tempo.
# - Tocar uma música no YouTube.
# - Encerrar o programa.
def comando_voz_usuario():
    comando = executa_comando()
    if 'horas' in comando:
        hora_atual  = datetime.datetime.now().strftime('%H:%M')
        # Convertendo a hora e minuto para texto
        hora, minuto = map(int, hora_atual.split(':'))
        hora_texto = numero_para_texto(hora)
        minuto_texto = numero_para_texto(minuto)
        # Montando o resultado final
        hora_por_extenso = f"{hora_texto} horas e {minuto_texto} minutos"
        maquina.say('Agora são ' + hora_por_extenso)
        maquina.runAndWait()
    elif 'pesquise' in comando:
        procurar = comando.replace('pesquise', '')
        wikipedia.set_lang('pt')
        resultado = wikipedia.summary(procurar, 2)
        print(resultado)
        maquina.say(resultado)
        maquina.runAndWait()
    #elif 'roteiro' in comando:
        query = comando.replace('pesquise', '').strip()
        resultados = google_search(query)
        resultado_final = ' '.join(resultados)
        print(resultado_final)
        maquina.say(resultado_final)
        maquina.runAndWait()
    elif 'temperatura' in comando:
        # Exemplo de uso
        cidade = 'Curitiba'
        soup = obter_previsao_tempo_google(cidade)
        if soup:
            previsao_detalhada = analisar_previsao(soup)
            resultado = previsao_por_extenso(cidade, previsao_detalhada)
            maquina.say(resultado)
            maquina.runAndWait()
        else:
            maquina.say("Desculpe, não foi possível obter a previsão do tempo.")
            maquina.runAndWait()
    elif 'tocar' in comando:
        musica = comando.replace('tocar','')
        resultado = pywhatkit.playonyt(musica)
        maquina.say('Procurando música')
        maquina.runAndWait()
    elif 'sair' in comando or 'parar' in comando:
        maquina.say('Encerrando o programa.')
        maquina.runAndWait()
        exit()

# Inicia o programa com uma mensagem de saudação usando conversão de texto para fala.
maquina.say("Olá, meu nome é Tina. No que posso lhe ajudar hoje?")
maquina.runAndWait()

# Inicia um loop infinito que imprime as instruções de uso e 
# chama a função comando_voz_usuario para continuar ouvindo e 
# executando comandos de voz do usuário.
while True:
    print("use: [horas] [pesquise ...] [temperatura] [tocar ...] [sair]")
    comando_voz_usuario()
