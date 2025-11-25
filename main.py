from tkinter import * # Importa todos os componentes básicos do Tkinter (botões, labels, janelas etc.)
import tkinter as tk
import pytz # Biblioteca para trabalhar com fusos horários
from geopy.geocoders import Nominatim # Usado para transformar o nome de uma cidade em coordenadas,latitude longitude.
from datetime import datetime, timedelta # pegar a hora atual, somar, subtrair tempo etc.
import requests # fazer requisições HTTP e buscar os dados do clima na API.
from PIL import Image,ImageTk # carregar e exibir imagens.
from tkinter import messagebox, ttk # messagebox: exibe janelas de aviso/erro, ttk: widgets mais modernos.
from timezonefinder import TimezoneFinder
import os # Permite acessar variáveis do sistema, como as do arquivo .env
from dotenv import load_dotenv #carregar as variáveis salvas no arquivo .env
load_dotenv() # carrega as variáveis do .env

root = Tk() # cria a janela principal do aplicativo.
root.title("weather App ") #titulo
root.geometry("750x470+300+200") # define o tamanho da janela e a posição inicial na tela.
root.resizable(False,False) #nao permite que usuário redimensione a janela, primeiro False é para largura, o segundo para altura.
root.config(bg="#202731") # define a cor de fundo da janela, "#202731" cor em hexadecimal (tom escuro).

#funcao para obter clima e fuso horario

def getWeather():
    city = textfield.get()#pega o texto digitado no campo
    geolocator = Nominatim(user_agent="new") #objeto para buscar a localizacao
    location = geolocator.geocode(city) #busca lat e long da cidade
    obj=TimezoneFinder()#objeto para encontrar o fuso horario
    result = obj.timezone_at(lat=location.latitude, lng=location.longitude)#descobre o fuso horario pela lat/long
    timezone.config(text=result)#mostra o fuso horario no label timezone

    #lat/long formatada com 4 casas decimais(round)
    long_lat.config(text=f"{round(location.latitude,4)} °N {round(location.longitude,4)} °E")

    home = pytz.timezone(result)#define o fuso horario da cidade
    local_time = datetime.now(home)#pega a hora local da cidade
    current_time = local_time.strftime("%I:%M %p") #formata no estilo 12hr AM/PM
    clock.config(text=current_time)#mostra a hora no label "clock"

    api_key = os.getenv("OPENWEATHER_API_KEY") #chave api
    api = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric" # Monta o link da API com a cidade, a chave e a unidade de medida
    json_data = requests.get(api).json() #Faz a requisição para a API e converte o resultado (JSON) em um dicionário Python
    #print(json_data)

    #current weather from first forecast

    current = json_data['list'][0] #Acessa o primeiro item da lista 'list' no JSON , dados atuais do clima
    temp = current['main']['temp'] # Pega a temperatura atual
    humidity = current['main']['humidity'] # Pega a umidade do ar
    pressure = current['main']['pressure'] # Pega a pressão atmosférica
    wind_speed = current['wind']['speed'] # Pega a velocidade do vento
    description = current['weather'][0]['description'] # Pega a descrição textual do clima, ex 'céu limpo'

    t.config(text=f"{temp}°C") # Mostra a temperatura no rótulo 't'
    h.config(text=f"{humidity}%") # Mostra a umidade no rótulo 'h'
    p.config(text=f"{pressure} hPa") # Mostra a pressão no rótulo 'p'
    w.config(text=f"{wind_speed} m/s") # Mostra a velocidade do vento no rótulo 'w'
    d.config(text=f"{description}") # Mostra a descrição do clima no rótulo 'd'

    
    #daily forecast pick 12:00 pm entries
    
    daily_data = [] # Cria uma lista para armazenar as previsões diárias (às 12:00)
    for entry in json_data['list']:
        if "12:00:00" in entry['dt_txt']: # Se o horário for meio-dia
            daily_data.append(entry) # Adiciona o item à lista de previsões diárias

    icons = [] # Lista para armazenar os ícones de clima de cada dia
    temps = [] # Lista para armazenar as temperaturas máxima e sensação de cada dia

    for i in range(5): # Para os próximos 5 dias
        if i >= len(daily_data): # Se não houver dados suficientes
            break # interrompe o loop
        icon_code = daily_data[i]['weather'][0]['icon'] # Pega o código do ícone de clima
        img = Image.open(f"icon/{icon_code}@2x.png").resize((50,50)) # Abre e redimensiona o ícone
        icons.append(ImageTk.PhotoImage(img)) # Converte para Tkinter e adiciona à lista de ícones
        temps.append((daily_data[i]['main']['temp_max'], daily_data[i]['main']['feels_like'])) # Salva temperaturas máxima e sensação

    day_widget = [ # Cria uma lista de tuplas, cada uma com label do ícone, label do dia, label da temperatura
        (firstimage, day1, day1temp),
        (secondimage, day2, day2temp),
        (thirdimage, day3, day3temp),
        (fourthimage, day4, day4temp),
        (fifthimage, day5, day5temp)
    ]

    for i, (img_label, day_label, temp_label) in enumerate(day_widget): # Itera pelos widgets de cada dia
        if i >= len(icons): # Se faltar ícone, interrompe
            break
        img_label.config(image=icons[i]) # Atualiza o label do ícone para o dia correspondente
        img_label.image = icons[i] # Mantém referência do ícone para evitar que o Python apague da memória
        temp_label.config(text=f"Day: {temps[i][0]}\nNight: {temps[i][1]}") # Atualiza o label da temperatura do dia/noite
        future_date = datetime.now() + timedelta(days=i) # Calcula a data futura para o dia
        day_label.config(text=future_date.strftime("%A")) # Atualiza o label do nome do dia (segunda, terça, etc)


##icon
image_icon=PhotoImage(file="Images/logo.png") # carrega uma imagem para usar como ícone da janela
root.iconphoto(False,image_icon)

Round_box=PhotoImage(file="Images/Rounded rectangle 1.png")
Label(root, image=Round_box,bg="#202731").place(x=30, y=60) # cria um Label no Tkinter e coloca a imagem carregada dentro dele.

# Label

label1 = Label(root, text="Temperature", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")  # Label para exibir o texto "Temperature" ao lado do valor exibido
label1.place(x=50, y=120)

label2 = Label(root, text="Humidity", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")     # Label para exibir o texto "Humidity" ao lado do valor exibido
label2.place(x=50, y=140)

label3 = Label(root, text="Pressure", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")     # Label para exibir o texto "Pressure" ao lado do valor exibido
label3.place(x=50, y=160)

label4 = Label(root, text="Wind Speed", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")   # Label para exibir o texto "Wind Speed" ao lado do valor exibido
label4.place(x=50, y=180)

label5 = Label(root, text="Description", font=("Helvetica", 11), fg="#323661", bg="#aad1c8")  # Label para exibir o texto "Description" ao lado da descrição textual do clima
label5.place(x=50, y=200)


#search box

Search_image=PhotoImage(file="Images/Rounded Rectangle 3.png") #carrega a imagem da barra de busca
myimage=Label(root,image=Search_image,bg="#202731")
myimage.place(x=270,y=122) #posiciona a imagem da barra de busca na tela

weat_image=PhotoImage(file="Images/Layer 7.png")
weatherimage=Label(root,image=weat_image,bg="#333c4c")
weatherimage.place(x=290, y=127)

textfield=tk.Entry(root,justify="center",width=15,font=("poppins",25,"bold"),bg="#202731",border=0,fg="white")
textfield.place(x=370,y=130)

Search_icon=PhotoImage(file="Images/Layer 6.png")
myimage_icon=Button(root,image=Search_icon,borderwidth=0,cursor="hand2",bg="#333c4c", command=getWeather)
myimage_icon.place(x=640,y=135)

#bottom box
frame=Frame(root,width=900,height=180,bg="#7094d4") ## Cria o painel inferior , a faixa azul na janela
frame.pack(side=BOTTOM) # Posiciona o painel na parte de baixo

#boxes
firstbox=PhotoImage(file="Images/Rounded Rectangle 2.png") #carrega as duas artes das caixas do rodapé (são imagens diferentes)
secondbox=PhotoImage(file="Images/Rounded Rectangle 2 copy.png")

Label(frame,image=firstbox,bg="#7094d4").place(x=30,y=20) # desenha a 1ª caixa dentro do frame inferior
Label(frame,image=secondbox,bg="#7094d4").place(x=300,y=30) # 2ª caixa
Label(frame,image=secondbox,bg="#7094d4").place(x=400,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=500,y=30)
Label(frame,image=secondbox,bg="#7094d4").place(x=600,y=30)

#clock
clock = Label(root, font=("Helvetica",20), bg="#202731", fg="white") # Label para mostrar o relógio (hora atual)
clock.place(x=30, y=20) # Posição do relógio no topo esquerdo da janela

#timezone
timezone = Label(root, font=("Helvetica",20), bg="#202731", fg="white") # Label para mostrar o fuso horário
timezone.place(x=500, y=20) # Posição do fuso horário no topo direito da janela

long_lat = Label(root, font=("Helvetica",10), bg="#202731", fg="white") # Label para mostrar latitude/longitude da cidade
long_lat.place(x=500, y=50) # Posição da latitude/longitude abaixo do fuso horário




#twpwd
t = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white", wraplength=90) # Label para mostrar temperatura
t.place(x=150, y=120)

h = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white", wraplength=90) #(humidity)
h.place(x=150, y=140)

p = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white", wraplength=90) #(pressure)
p.place(x=150, y=160)

w = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white", wraplength=90) #(wind)
w.place(x=150, y=180)  # ajustado o y para dar espaçamento

d = Label(root, font=("Helvetica", 9), bg="#333c4c", fg="white", wraplength=90) # descrição do clima
d.place(x=150, y=200)





#first cell
firstframe = Frame(root, width=230, height=132, bg="#323661") # Caixa (frame) para organizar os elementos
firstframe.place(x=35, y=315) # Posição da caixa na janela (x=horizontal, y=vertical)

firstimage = Label(firstframe, bg="#323661") # Espaço (label) para mostrar a imagem do clima
firstimage.place(x=1, y=15) # Posição da imagem

day1 = Label(firstframe, font=("arial 20"), bg="#323661", fg="white") # Texto (label) para o dia da semana
day1.place(x=100, y=5) # Posição do texto do dia dentro da caixa

day1temp = Label(firstframe, font=("arial 15 bold"), bg="#323661", fg="white") # Texto (label) para a temperatura
day1temp.place(x=100, y=50) # Posição da temperatura dentro da caixa



# second cell

secondframe=Frame(root, width=70, height=115, bg="#eeefea") # Caixa (frame) p/ previsão do 2º dia
secondframe.place(x=305, y=325) # Posição da caixa na tela

secondimage=Label(secondframe, bg="#eeefea") # Espaço p/ ícone do clima (2º dia)
secondimage.place(x=7, y=20) # Posição do ícone dentro da caixa

day2=Label(secondframe, bg="#eeefea", fg="#000") # Texto p/ nome do dia (2º dia)
day2.place(x=10, y=5) # Posição do texto dentro da caixa

day2temp=Label(secondframe, bg="#eeefea", fg="#000") # Texto p/ temperatura (2º dia)
day2temp.place(x=2, y=70) # Posição da temperatura dentro da caixa



# third cell

thirdframe=Frame(root, width=70, height=115, bg="#eeefea") # Caixa (frame) p/ previsão do 3º dia
thirdframe.place(x=405, y=325) # Posição da caixa na tela (igual à segunda, pode sobrepor)

thirdimage=Label(thirdframe, bg="#eeefea") # Espaço p/ ícone do clima (3º dia)
thirdimage.place(x=7, y=20) # Posição do ícone dentro da caixa

day3=Label(thirdframe, bg="#eeefea", fg="#000") # Texto p/ nome do dia (3º dia)
day3.place(x=10, y=5) # Posição do texto dentro da caixa

day3temp=Label(thirdframe, bg="#eeefea", fg="#000") # Texto p/ temperatura (3º dia)
day3temp.place(x=2, y=70) # Posição da temperatura dentro da caixa



# fourth cell
fourthframe = Frame(root, width=70, height=115, bg="#eeefea") # Cria a 4ª caixa (previsão do 4º dia)
fourthframe.place(x=505, y=325) # Posiciona a caixa na janela

fourthimage = Label(fourthframe, bg="#eeefea") # Espaço p/ o ícone do clima (4º dia)
fourthimage.place(x=7, y=20) # Posição do ícone dentro da caixa

day4 = Label(fourthframe, bg="#eeefea") # Texto p/ nome do dia (4º dia)
day4.place(x=10, y=5) # Posição do texto

day4temp = Label(fourthframe, bg="#eeefea") # Texto p/ temperatura (4º dia)
day4temp.place(x=2, y=70) # Posição da temperatura



# fifth cell
fifthframe = Frame(root, width=70, height=115, bg="#eeefea") # Cria a 5ª caixa (previsão do 5º dia)
fifthframe.place(x=605, y=325) # Posiciona a caixa na janela

fifthimage = Label(fifthframe, bg="#eeefea") # Espaço p/ o ícone do clima (5º dia)
fifthimage.place(x=7, y=20) # Posição do ícone dentro da caixa

day5 = Label(fifthframe, bg="#eeefea", fg="#000") # Texto p/ nome do dia (5º dia)
day5.place(x=10, y=5) # Posição do texto

day5temp = Label(fifthframe, bg="#eeefea", fg="#000") # Texto p/ temperatura (5º dia)
day5temp.place(x=2, y=70) # Posição da temperatura











root.mainloop() # mantém a janela aberta até que o usuário feche.
