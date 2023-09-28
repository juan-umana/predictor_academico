from dash.dependencies import Input, Output
import matplotlib.image as mpimg
import plotly.express as px
from dash import dcc  
from dash import html 
import pandas as pd
import dash
import os
from Model.model import inference

print(inference)

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
        De acuerdo con los resultado obtenidos en el análisis descriptivo anterior, se seleccionaron las sigueintes variables como factores de riesgo importantes para predecir la necesidad de acompañamiento de un estudiante. 
        A continuación, ingrese valores para las variables y así observar el comportamiento del estado estudiantil de los estudiantes.
    '''),
    html.Div(["Variable 1: ",
              dcc.Input(id='var1', value='Ingrese un valor', type='text')]),
    html.Div(["Variable 2: ",
              dcc.Input(id='var2', value='Ingrese un valor', type='text')]),
    html.Div(["Variable 3: ",
              dcc.Input(id='var3', value='Ingrese un valor', type='text')]),
    html.Div(["Variable 4: ",
              dcc.Input(id='var4', value='Ingrese un valor', type='text')]),
    html.Div(["Variable 5: ",
              dcc.Input(id='var5', value='Ingrese un valor', type='text')]),
    html.Div(["Variable 6: ",
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
