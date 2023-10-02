#%%
import dash
from dash.dependencies import Input, Output
from dash import dcc  
from dash import html 
import pandas as pd
import plotly.express as px
import os
from model import inference

coolwarm_scale = [[0, 'blue'], [0.5, 'white'], [1, 'red']]

def correlation_plots_dash(correlation_matrix, title):
    fig = px.imshow(correlation_matrix,
                    labels=dict(color="Correlation"),
                    x=correlation_matrix.columns.tolist(),
                    y=correlation_matrix.columns.tolist(),
                    color_continuous_scale=coolwarm_scale,
                    zmin=-1, zmax=1)

    fig.update_layout(title_text=title, xaxis_title="Variables", yaxis_title="Variables")

    return fig

contin_correlations =  pd.read_excel("continuos_correlations.xlsx")
categ_correlations =  pd.read_excel("categorical_correlations.xlsx")

contin_plot = correlation_plots_dash(contin_correlations, "Mapa de correlaciones entre variables continuas")
categ_plot  = correlation_plots_dash(categ_correlations, "Mapa de calor de correlaciones entre variables categóricas")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Predictor de riesgo académico'),
    html.Div(children='''
        Bienvenido a la herramienta de analítica de datos académicos que le permitirá estudiar los factores por los cuales sus estudiantes no culminan sus estudios en el tiempo predestinado y tomar decisiones informadas de acuerdo a los resultados.
        A continuación se motrarán las correlaciones entre las variables a analizar:
    '''),
    dcc.Graph(id='continuous_correlations', figure=contin_plot),
    dcc.Graph(id='categorical_correlations', figure=categ_plot),
    html.Div(children='''
        De acuerdo con los resultado obtenidos en el análisis descriptivo anterior, se seleccionaron unos factores de riesgo importantes para predecir la necesidad de acompañamiento de un estudiante. 
        A continuación, ingrese los datos correspondientes del estudiante del cual quiere observar su riesgo académico.
    '''),
    html.Div(["Tipo de aplicación: ",
              dcc.Input(id='var1', value='', type='text')]),
    html.Div(["Número de curso: ",
              dcc.Input(id='var2', value='', type='text')]),
    html.Div(["¿El estudiante se encuentra al día con la matricula?: ",
              dcc.Input(id='var3', value='', type='text')]),
    html.Div(["¿El estudiante tiene beca?: ",
              dcc.Input(id='var4', value='', type='text')]),
    html.Div(["Edad: ",
              dcc.Input(id='var5', value='', type='text')]),
    html.Div(["Nota del estudiante en el primer semestre: ",
              dcc.Input(id='var6', value='', type='text')]),
    html.Div(["Nota del estudiante en el segundo semestre: ",
              dcc.Input(id='var7', value='', type='text')]),
    html.Div(["Tasa de inflación: ",
              dcc.Input(id='var8', value='', type='text')]),    
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
        Input(component_id='var6', component_property='value'),
        Input(component_id='var7', component_property='value'),
        Input(component_id='var8', component_property='value')
    ]
)

def update_output_div(val1, val2, val3, val4, val5, val6, val7, val8):
    values = [val1, val2, val3, val4, val5, val6, val7, val8]
    labels = ['application', 'course', 'tuition', 'scholarship', 'age', 'grade_1', 'grade_2', 'inflation']
    evidence = {}
    for i in range(len(values)):
        if values[i] != '':
            evidence[labels[i]]=int(values[i])
    result = inference.query(variables=['success'], evidence=evidence)
    try:
        list_result = list(result.values)
        max_val = list_result.index(max(result.values))
        if max_val == 0:
            prediction = 'Deserción'
        elif max_val == 1:
            prediction = 'Matriculado'
        else:
            prediction = 'Graduado'
    except:
        prediction = 'No se puede determinar'
    return 'La predicción del estado estudiantil es: {}'.format(prediction)

if __name__ == '__main__':
    app.run_server(debug=False)
