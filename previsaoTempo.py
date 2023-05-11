import requests
from datetime import datetime, timedelta


api_key = 'e9e3c00d165577f4a9ec34c51379d1f6'
cidade = input('Digite uma cidade: ')

# Obter a previsão atual
link_atual = f'https://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={api_key}&lang=pt_br'
requisicao_atual = requests.get(link_atual)
requisicao_atual_dict = requisicao_atual.json()
descricao_atual = requisicao_atual_dict['weather'][0]['description']
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
print(f'A temperatura atual é {temperatura_atual}Cº')
print(f"As condições do tempo em {cidade} são: {descricao_atual}.")
print(f"A temperatura mínima é de {temperatura_min}°C e a temperatura máxima é de {temperatura_max}°C.")

if previsao_24h:
    print("Previsão das próximas 24 horas:")
    for previsao in previsao_24h:
        data_previsao, descricao_previsao, temperatura_previsao = previsao
        print(f"{data_previsao.strftime('%d/%m/%Y %H:%M')}: {descricao_previsao}, temperatura de {temperatura_previsao}°C")
else:
    print("Não foi possível obter a previsão das próximas 24 horas.")