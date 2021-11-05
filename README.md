# Gráfico de Ações


Financeiro_GUI é um código em Python com interface gráfica onde o usuário pode gerar gráficos de ações conforme necessidade. É necessária a utilização de uma API-KEY que pode ser
requisitada gratuitamente [neste link](https://www.alphavantage.co/support/#api-key). Após a obtenção da chave, favor copiá-la para a variável API-KEY, em formato de string, na 
linha 236 do código.

Utiliza a API [AlphaVantage](https://www.alphavantage.co/documentation/). 

Bibliotecas:
- [tkinter](https://docs.python.org/3/library/tkinter.html): para interface gráfica;
- [pandas](https://pandas.pydata.org/): para a manipulação dos dados;
- [plotly](https://plotly.com/python/candlestick-charts/): para criação e manipulação dos gráficos.

O usuário pode escolher entre ver os dados no período Intraday, Diário, Semanal e Mensal. Para maiores informações, ver documentação do AlphaVantage.

