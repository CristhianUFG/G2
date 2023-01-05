from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import math
import dash

dash.register_page(__name__)

dash.register_page(
    __name__,
    title = 'Dados de Barra',
    name  = 'Dados de Barra'
)

dataBus = []
id = []
#===========================================================================================
#Function that read the input data_bus file
#===========================================================================================
def readInputBus():
    dataFile = open("data_Bus.txt","r")
    linhas = dataFile.readlines()
    j=0
    for linha in linhas:
        if j != 0:
            idJ=linha.split(",",2)[0] 
            id.append(idJ)
            type=linha.split(",",2)[1]
            dataBus.append([])
            dataBus[j-1].append(id)
            dataBus[j-1].append(type)
        else:
            nBus=int(linha.split(",",2)[0])
        j=j+1
    return nBus

nBus    = readInputBus()
tensao = []
moduloTensao   = []
anguloTensao   = []
results = []

#===========================================================================================
#Function that read the input results file
#===========================================================================================
def importResults():
    dataFile = open("results.txt","r")
    linhas = dataFile.readlines()
   
    for linha in linhas:
        for i in range(0,2*nBus,2):
            modulo = float(linha.split(" ",2*nBus)[i])
            angulo = float(linha.split(" ",2*nBus)[i+1])
            moduloTensao.append(modulo)
            anguloTensao.append(angulo*180/math.pi)
        

importResults()

id = id*24
hora=[]
ihora = 1

for j in range(24):
    hora.append(ihora)
    ihora = ihora+1

df = pd.DataFrame({
    "Id": id,
    "Tensao": moduloTensao,
    "Angulo": anguloTensao,
})

#===========================================================================================
#Making the voltage Vector used to construct the voltage figure
#===========================================================================================
tensoes = []
for i in range(1,nBus+1,1):
    newdf = df.query('Id == "{}"'.format(i))
    tensaoAtual = newdf["Tensao"].tolist()
    tensoes.append(tensaoAtual)
#===========================================================================================
#Making the angle Vector used to construct the angle figure
#===========================================================================================
angulos = []
for i in range(1,nBus+1,1):
    newdf = df.query('Id == "{}"'.format(i))
    angAtual = newdf["Angulo"].tolist()
    angulos.append(angAtual)


#===========================================================================================
#Making some Analysis
#===========================================================================================
#Voltage Analysis
maxTensaoHoraria = max(tensoes)
maxTensao = max(maxTensaoHoraria)
horaPico_inf = maxTensaoHoraria.index(maxTensao) + 1


minTensaoHoraria = min(tensoes)
minTensao = min(minTensaoHoraria)
horaPico_sup = minTensaoHoraria.index(min(minTensaoHoraria)) + 1


#===========================================================================================
#Making the voltage Figure
#===========================================================================================
fig_tensao = go.Figure(data=[go.Scatter(name="Barra {}".format(1),x=hora, y=tensoes[0])])
for i in range(1,nBus):
    fig_tensao.add_trace(go.Scatter(name = "Barra {}".format(i+1),x=hora, y=tensoes[i]))

fig_tensao.update_layout(legend_valign="middle")

#===========================================================================================
#Making the angle Figure
#===========================================================================================
fig_angulo = go.Figure(data=[go.Scatter(name="Barra {}".format(1),x=hora, y=angulos[0])])
for i in range(1,nBus):
    fig_angulo.add_trace(go.Scatter(name = "Barra {}".format(i+1),x=hora, y=angulos[i]))

fig_angulo.update_layout(legend_valign="middle")




layout = html.Div(children=[
    
    #Grafico de Tensao
        html.Div([
            html.H1(children='Dados de Barra',className='titulo_secao'),
        ],className='div_titulo_secao'),

         html.Div([
        html.Div([
            html.P('Módulo de Tensão Horário [p.u.]'),
            
            dcc.Graph(
                id='grafico_tensao',
                figure=fig_tensao
            )
        ],id="wideGraph"),
    #------------------------------------------------------------------------------------------
    #Analise de Tensao
    html.Div([

        html.Div([
            html.P('Máxima Tensão'),
            html.H1(children="{:.3f} [p.u.]".format(maxTensao),id="id_maxTensao"),
         ],id="halfGraph_green"),


          html.Div([
            html.P('Mínima Tensão'),
            html.H1(children="{:.3f} [p.u.]".format(minTensao),id="id_minTensao"),
            ],id="halfGraph_red"), 

            html.Div([
            html.P('Horas Críticas'),
            html.H2(children="Máx.: {:02d}:00 h".format(horaPico_inf),id="id_horaPicoInf"),
            html.H2(children="Mín. : {:02d}:00 h".format(horaPico_sup),id="id_horaPicoSup"),
            ],id="halfGraph_blue"), 
    ],className="halfDivConfig"),
    ]),
    #------------------------------------------------------------------------------------------
    #Grafico de Angulo de fase
    html.Div([
        html.Div([
            html.P('Ângulo de Fase Horário [deg]'),
            
            dcc.Graph(
                id='grafico_angulo',
                figure=fig_angulo
            )
        ],id="wideGraph_blue"),
    ]),

],className="bodyContent")