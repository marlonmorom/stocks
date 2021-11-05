from tkinter import *
import requests
import pandas as pd
import json
import plotly.graph_objects as go


# -----Declaração de funções-----
def calculaVariacao(alta, baixa):  # retorna o
    return (alta/baixa-1)*100


def calculaDados(df):
    global open, high, low, close, dmin, dmax, maxima_global, minima_global, media
    open = '1. open'
    high = '2. high'
    low = '3. low'
    close = '4. close'

    # conversão das entradas para números
    df[high] = pd.to_numeric(df[high])
    df[low] = pd.to_numeric(df[low])
    df[close] = pd.to_numeric(df[close])

    # verificando a maior variação entre cada dia
    df['Delta'] = df.apply(lambda df: calculaVariacao(df[high], df[low]), axis=1)

    # retornando as máximas e mínimas globais, e o dia
    dmax = df[high].idxmax()
    maxima_global = df[high].max()

    dmin = df[low].idxmin()
    minima_global = df[low].min()

    media = df[close].mean()

    plotaGrafico(df)


def plotaGrafico(df):
    global botaoNovaConsulta
    fig = go.Figure(data=[go.Candlestick(x=df.index,
                    open=df[open],
                    high=df[high],
                    low=df[low],
                    close=df[close])])

    # Formatação do gráfico
    fig.update_layout(
        title={
            'text': 'Variação {} do Ticker {}<br>Última cotação: ${:.2f} '.format(intervalo, ticker.upper(), float(df[close].iloc[0])),
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font=dict(
            family="Courier New, monospace",
            size=18,
        ),
        yaxis_title='$',

    )

    # Inserção de indicadores

    fig.add_annotation(x=df['Delta'].idxmax(), y=df[high].loc[df['Delta'].idxmax()],
                       text="Maior variação: {:.2f}%".format(
                           df['Delta'].max()),
                       showarrow=True,
                       arrowhead=3)

    fig.add_annotation(x=dmax, y=maxima_global,
                       text="Máxima: $ {:.2f}".format((float(maxima_global))),
                       showarrow=True,
                       arrowhead=1)

    fig.add_annotation(x=dmin, y=minima_global,
                       text="Mínima: $ {:.2f}".format(float(minima_global)),
                       showarrow=True,
                       arrowhead=1)
    fig.show()

    texto_principal.set('Máxima: $ {:.2f}\nMínima: $ {:.2f}\nMédia de fechamento: $ {:.2f}\nMaior variação máxima/mínima por divisão de tempo: {:.2f}%'.format(
        float(maxima_global), float(minima_global), float(media), df['Delta'].max()))
    posicionaLabel()
    inputUsuario.grid_remove()
    botaoNovaConsulta = Button(root, text='Nova Consulta', command=reinicia,
                               width=15, background='#15215C', fg='white', font=('verdana', 10, 'bold'))
    botaoNovaConsulta.grid(pady=5, row=2)


def requisitaDados():
    global ticker, botaoNovaConsulta
    botaoAjuda.grid_forget()
    botaoGrafico.grid_forget()
    ticker = inputUsuario.get()
    inputUsuario.delete(0, END)

    # Requisitando API, retornando no formato JSON
    url = 'https://www.alphavantage.co/query?function={}&symbol={}&interval=5min&apikey={}'.format(
        periodo, ticker,API_KEY)
    r = requests.get(url)

    # Armazenando os dados
    data = r.json()

    if(len(data)) != 1:  # verifica se o site não retornou apenas uma mensagem contendo erro
        # Pulando a coluna Meta Data
        for i, key in enumerate(data):
            if i == 1:
                seg_coluna = key

        # Transformando em DataFrame. Não é necessária a coluna MetaData
        df = pd.DataFrame(data[seg_coluna])
        df = df.T

        calculaDados(df)

    else:
        texto_principal.set(
            'Houve algum erro! Tente novamente. \nTente mudar o ticker ou a periodicidade!\nDigite a periodicidade desejada:\n\nI - Intraday\nD - Diária\nS - Semanal\nM - Mensal\n')
        posicionaLabel()
        posicionaEntrada()


def reinicia():
    botaoNovaConsulta.grid_remove()
    texto_principal.set(
        'Digite a periodicidade desejada:\n\nI - Intraday\nD - Diária\nS - Semanal\nM - Mensal\n')
    posicionaLabel()
    posicionaEntrada()


def posicionaLabel():
    global posx
    # recebe a largura necessária para o Label
    larguraLabel = entrada.winfo_reqwidth()
    # posiciona horizontalmente no meio da tela
    posx = (larguraTelaUsuario/2-larguraLabel/2)
    entrada.grid(padx=posx, pady=(posy, posyInferior), sticky="NESW")


def posicionaEntrada():
    inputUsuario.grid(padx=posx, pady=5, row=1)
    botaoOK.grid(pady=5, row=2)
    inputUsuario.focus()


def clickAjuda():
    global botaoBusca

    # limpando entradas
    inputUsuario.delete(0, END)
    inputUsuario.focus()
    botaoOK.grid_forget()
    botaoAjuda.grid_forget()
    botaoGrafico.grid_forget()

    # setando textos
    texto_principal.set('Digite o nome da empresa ou um ticker: ')
    # criando botão

    botaoBusca = Button(root, text='Buscar', command=verificaTicker, width=10,
                        background='#15215C', fg='white', font=('verdana', 10, 'bold'))
    botaoBusca.grid(pady=5, row=2)
    posicionaLabel()


def verificaTicker():
    keyword = inputUsuario.get()

    empresas = []
    url = 'https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={}&apikey={}'.format(
        keyword,API_KEY)
    r = requests.get(url)
    data = r.json()

    if len(data["bestMatches"]) == 0:
        texto_principal.set(
            "Empresa não encontrada! Tente mudar o \nnome ou retirar acentos: ")
        inputUsuario.delete(0, END)
        inputUsuario.focus()
        posicionaLabel()

    else:
        for i, ent in enumerate(data["bestMatches"]):
            empresas.append(('Empresa: {}. Ticker: {}'.format(
                ent['2. name'], ent['1. symbol'])))

        inputUsuario.delete(0, END)
        inputUsuario.focus()
        botaoBusca.grid_forget()
        texto_principal.set(
            'Digite o ticker desejado exatamente como escrito abaixo:\n\n'+'\n'.join(empresas))
        botaoGrafico.grid(pady=5, row=2)
        posicionaLabel()


def clickOK():
    global botaoAjuda, intervalo, periodo, botaoGrafico
    intervaloUsuario = inputUsuario.get()

    # verifica se a inicial está correta
    if not any(x in intervaloUsuario[0].lower() for x in iniciais):
        inputUsuario.delete(0, END)
        texto_principal.set(
            'Digite apenas a letra inicial do período.\n\nI - Intraday\nD - Diária\nS - Semanal\nM - Mensal\n')
        posicionaLabel()
        inputUsuario.grid_forget()
        botaoOK.grid_forget()
        posicionaEntrada()

    else:
        # ordem de todas as listas está correspondente para poder se utilizar o mesmo índice
        intervalo = lista_intervalo[iniciais.index(
            intervaloUsuario[0].lower())]
        periodo = lista_periodos[iniciais.index(intervaloUsuario[0].lower())]

        texto_principal.set(
            'Digite o ticker desejado ou clique em \n"ajuda" para procurar pelo nome da empresa \nou caso não tenha certeza da grafia do ticker')
        posicionaLabel()

        inputUsuario.delete(0, END)
        inputUsuario.focus()
        botaoOK.grid_remove()

        botaoGrafico = Button(root, text='Gera Grafico', command=requisitaDados, width=10,
                              background='#15215C', fg='white', font=('verdana', 10, 'bold'))
        botaoGrafico.grid(pady=5, row=2)
        botaoAjuda = Button(root, text='Ajuda', command=clickAjuda, width=10,
                            background='#15215C', fg='white', font=('verdana', 10, 'bold'))
        botaoAjuda.grid(pady=5, row=3)


#-----declaração entradas API-----
API_KEY = ''
iniciais = ['i', 'd', 's', 'm']
lista_intervalo = ['Intraday', 'Diária', 'Semanal', 'Mensal']
lista_periodos = ['TIME_SERIES_INTRADAY', 'TIME_SERIES_DAILY',
                  'TIME_SERIES_WEEKLY', 'TIME_SERIES_MONTHLY']

# -----criação e configuração de tela-----
root = Tk()
root.configure(background='#A8A8A8')
larguraTelaUsuario = root.winfo_screenwidth()
alturaTelaUsuario = root.winfo_screenheight()
root.geometry("%dx%d" % (larguraTelaUsuario, alturaTelaUsuario))

# utiliza string variável para mudar o texto da label durante o decorrer do programa
texto_principal = StringVar()
texto_principal.set(
    'Digite a periodicidade desejada:\n\nI - Intraday\nD - Diária\nS - Semanal\nM - Mensal\n')

entrada = Label(
    root,
    justify='left',
    font="Verdana 30",
    textvariable=texto_principal,
    borderwidth=5,
    background='#15215C',
    fg='white',
    relief='groove',
)

posyInferior = 10  # afastamento no eixo Y a partir do final da label
alturaLabel = entrada.winfo_reqheight()  # recebe a altura necessária pelo Label
fatorPosy = 0.3  # fator para deslocamento da posição vertical. Valores acima de 1 abaixam a posição, fatores abaixo de 1 sobem a posição
posy = (alturaTelaUsuario/2-alturaLabel/2)*fatorPosy

# -----declaração entrada e botão OK-----
inputUsuario = Entry(root, width=30, background='#DCDCDC', font='Verdana 15')
botaoOK = Button(root, text='OK', command=clickOK, width=10,
                 background='#15215C', fg='white', font=('verdana', 10, 'bold'))


root.title("Gráficos de Ações")
posicionaLabel()
posicionaEntrada()

root.mainloop()
