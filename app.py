from dash.dependencies import Input, Output
import matplotlib.image as mpimg
import plotly.express as px
from dash import dcc  
from dash import html 
import pandas as pd
import dash
import os
from model import inference

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

categ_img_path = os.path.join('data_exploration','correlation_heat_map_categorical.png')
cont_img_path = os.path.join('data_exploration','correlation_heat_map_continous.png')

app.layout = html.Div(children=[
    html.H1(children='Predictor de riesgo académico'),

    html.Div(children='''
        Bienvenido a la herramienta de analítica de datos académicos que le permitirá estudiar los factores por los cuales sus estudiantes no culminan sus estudios en el tiempo predestinado y tomar decisiones informadas de acuerdo a los resultados.
        A continuación se motrarán las correlaciones entre las variables a analizar:
    '''),
    html.Img(src=categ_img_path, style={'width': '50%', 'height': 'auto'}),
    html.Img(src=cont_img_path, style={'width': '50%', 'height': 'auto'}),
    html.Div(children='''
        De acuerdo con los resultado obtenidos en el análisis descriptivo anterior, se seleccionaron unos factores de riesgo importantes para predecir la necesidad de acompañamiento de un estudiante. 
        A continuación, ingrese los datos correspondientes del estudiante del cual quiere observar su riesgo académico.
    '''),
    html.Div(["Tipo de aplicación: ",
              dcc.Input(id='var1', value='Ingrese un valor', type='text')]),
    html.Div(["Número de curso: ",
              dcc.Input(id='var2', value='Ingrese un valor', type='text')]),
    html.Div(["¿El estudiante se encuentra al día con la matricula?: ",
              dcc.Input(id='var3', value='Si o No', type='text')]),
    html.Div(["¿El estudiante tiene beca?: ",
              dcc.Input(id='var4', value='Si o No', type='text')]),
    html.Div(["Edad: ",
              dcc.Input(id='var5', value='Ingrese un valor', type='text')]),
    html.Div(["Nota del estudiante en el primer semestre: ",
              dcc.Input(id='var6', value='Ingrese un valor', type='text')]),
    html.Div(["Nota del estudiante en el segundo semestre: ",
              dcc.Input(id='var6', value='Ingrese un valor', type='text')]),
    html.Div(id='my-output'),
    ]
)

@app.callback(
    Output(component_id='my-output', component_property='children'),
    [
        Input(component_id='var1', component_property='value'),
        Input(component_id='var2', component_property='value'),
        Input(component_id='var3', component_property='value'),
        Input(component_id='var4', component_property='value'),
        Input(component_id='var5', component_property='value'),
        Input(component_id='var6', component_property='value')
    ]
)


def update_output_div(val1, val2, val3, val4, val5, val6):
    prediction = "MATRICULADO"
    return 'La predicción del estado estudiantil es: {}'.format(prediction)

if __name__ == '__main__':
    app.run_server(debug=True)
