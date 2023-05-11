import requests
from datetime import datetime, timedelta
import tkinter as tk

def obter_previsoes():
    cidade = entrada_cidade.get()
    api_key = 'e9e3c00d165577f4a9ec34c51379d1f6'

    # Obter a previsão atual
    link_atual = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br'
    requisicao_atual = requests.get(link_atual)
    requisicao_atual_dict = requisicao_atual.json()

    if requisicao_atual.status_code != 200:
        texto_resultado.delete('1.0', tk.END)
        texto_resultado.insert('1.0', 'Não foi possível obter a previsão do tempo. Verifique se a cidade foi digitada corretamente e tente novamente.')
        return

    if 'weather' in requisicao_atual_dict:
        descricao_atual = requisicao_atual_dict['weather'][0]['description']
    else:
        descricao_atual = 'Não foi possível obter a descrição do tempo atual.'

    temperatura_atual = round(requisicao_atual_dict['main']['temp'] - 273.15)
    temperatura_min = round(requisicao_atual_dict['main']['temp_min'] - 273.15)
    temperatura_max = round(requisicao_atual_dict['main']['temp_max'] - 273.15)

    # Obter a previsão das próximas 24 horas
    link_previsao = f'https://api.openweathermap.org/data/2.5/forecast?q={cidade}&appid={api_key}&lang=pt_br'
    requisicao_previsao = requests.get(link_previsao)
    requisicao_previsao_dict = requisicao_previsao.json()

    # Obter a previsão para as próximas 24 horas
    previsao_24h = []
    for previsao in requisicao_previsao_dict['list']:
        data_previsao = datetime.fromtimestamp(previsao['dt'])
        if data_previsao <= datetime.now() + timedelta(hours=24):
            descricao_previsao = previsao['weather'][0]['description']
            temperatura_previsao = round(previsao['main']['temp'] - 273.15)
            previsao_24h.append((data_previsao, descricao_previsao, temperatura_previsao))

    # Exibir a previsão atual e das próximas 24 horas
    texto_resultado.delete('1.0', tk.END)
    texto_resultado.insert('1.0', f'A temperatura atual é {temperatura_atual}Cº\n')
    texto_resultado.insert('2.0', f'Mínima: {temperatura_min}Cº - Máxima: {temperatura_max}Cº\n\n')
    texto_resultado.insert('3.0', f'Previsão para as próximas 24 horas:\n\n')
    for previsao in previsao_24h:
        data = previsao[0].strftime('%d/%m/%Y %H:%M')
        descricao = previsao[1]
        temperatura = previsao[2]
        texto_resultado.insert(tk.END, f'{data} - {descricao} - {temperatura}Cº\n')

# Configuração da janela principal
janela = tk.Tk()
janela.title('Previsão do Tempo')

# Entrada de texto para a cidade
frame_entrada = tk.Frame(janela)
frame_entrada.pack(side=tk.TOP, pady=10)
label_cidade = tk.Label(frame_entrada, text='Cidade:', font=('bold', 14))
label_cidade.pack(side=tk.LEFT)
entrada_cidade = tk.Entry(frame_entrada, font=('bold', 14))
entrada_cidade.pack(side=tk.LEFT, padx=10)
botao_previsao = tk.Button(janela, text='Obter previsão do tempo', font=('bold', 14), command=obter_previsoes)
botao_previsao.pack(pady=10)
frame_resultado = tk.Frame(janela)
frame_resultado.pack(side=tk.TOP, pady=10)
texto_resultado = tk.Text(frame_resultado, font=('bold', 14), height=10, width=50)
texto_resultado.pack(side=tk.LEFT)
scrollbar_resultado = tk.Scrollbar(frame_resultado)
scrollbar_resultado.pack(side=tk.RIGHT, fill=tk.Y)
texto_resultado.config(yscrollcommand=scrollbar_resultado.set)
scrollbar_resultado.config(command=texto_resultado.yview)

janela.mainloop()

# Exibir a previsão atual e das próximas 24 horas
texto_resultado.delete('1.0', tk.END)
texto_resultado.insert('1.0', f'A temperatura atual é {temperatura_atual}Cº\n')

texto_resultado.insert(tk.END, f'\nPrevisão das próximas 24 horas para {cidade}:\n\n')
for previsao in previsao_24h:
    texto_resultado.insert(tk.END, f'{previsao[0].strftime("%d/%m/%Y %H:%M:%S")} - {previsao[1]} - {previsao[2]}Cº\n')

# Interface gráfica
janela = tk.Tk()
janela.title('Previsão do Tempo')

# Entrada de texto para a cidade
frame_entrada = tk.Frame(janela)
frame_entrada.pack(side=tk.TOP, padx=10, pady=10)

label_cidade = tk.Label(frame_entrada, text='Cidade:')
label_cidade.pack(side=tk.LEFT)

entrada_cidade = tk.Entry(frame_entrada, width=30)
entrada_cidade.pack(side=tk.LEFT)

botao_buscar = tk.Button(frame_entrada, text='Buscar', command=obter_previsoes)
botao_buscar.pack(side=tk.LEFT)

# Área de exibição do resultado
frame_resultado = tk.Frame(janela)
frame_resultado.pack(side=tk.BOTTOM, padx=10, pady=10)

texto_resultado = tk.Text(frame_resultado, height=10, width=50)
texto_resultado.pack(side=tk.LEFT)

scrollbar_resultado = tk.Scrollbar(frame_resultado)
scrollbar_resultado.pack(side=tk.RIGHT, fill=tk.Y)

texto_resultado.config(yscrollcommand=scrollbar_resultado.set)
scrollbar_resultado.config(command=texto_resultado.yview)

janela.mainloop()

