import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
import psycopg2
from dotenv import load_dotenv # pip install python-dotenv
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from model import inference


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# path to env file
env_path=os.path.join("app.env")

# load env 
load_dotenv(dotenv_path=env_path)
# extract env variables
USER=os.getenv('USER')
PASSWORD=os.getenv('PASSWORD')
HOST=os.getenv('HOST')
PORT=os.getenv('PORT')
DBNAME=os.getenv('DBNAME')

#connect to DB
engine = psycopg2.connect(
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)
print(DBNAME)
print(USER)
print(PASSWORD)
print(HOST)
print(PORT)

# Upload correlations
contin_correlations =  pd.read_excel("continuos_correlations.xlsx")
categ_correlations =  pd.read_excel("categorical_correlations.xlsx")
contin_corr_target = contin_correlations["target_contin"][:-1].to_frame()
contin_corr_target.index = contin_correlations.columns[:-1]
contin_corr_target.columns = ["target"]
categ_corr_target = categ_correlations["target_categ"][:-1].to_frame()
categ_corr_target.index = categ_correlations.columns[:-1]
categ_corr_target.columns = ["target"]
target_corr = pd.concat([contin_corr_target, categ_corr_target], axis=0) 
# Ordenar correlaciones en orden descendente
sorted_correlations = target_corr.sort_values(by="target", ascending=False)

# Graficar correlaciones
corr_fig = px.bar(x=sorted_correlations.index, y=sorted_correlations['target'].values, color=sorted_correlations['target'].values,
             color_continuous_scale="RdBu", labels={"y": "Correlación con el éxito académico", "x": "Factores", "color": "Coeficiente de correlación"})
corr_fig.update_layout(xaxis_tickangle=-90, plot_bgcolor='white', paper_bgcolor='white', xaxis_tickfont_size=10, height=500)

cursor = engine.cursor()


app.layout = html.Div(
    [
    html.H1(children='Predictor de riesgo académico'),
    html.Div(children='''
        Bienvenido a la herramienta de analítica de datos académicos que le permitirá estudiar los factores por los cuales sus estudiantes no culminan sus estudios en el tiempo predestinado y tomar decisiones informadas de acuerdo a los resultados.
        A continuación se motrarán las correlaciones entre los factores a analizar y el éxito estudiantil:
    '''),
    dcc.Graph(id='correlations', figure=corr_fig),
    html.H6("Consulte las estadísticas de los cursos:"),
    html.Div(children='''
        A continuación puede seleccionar un curso de interés y ver el promedio de notas de los estudiantes en los primeros semestres, 
        así como el promedio general de notas de todos los estudiantes. También podrá ver la cantidad de estudiantes en cada uno de los estados
        académicos (Aprobado, Reprobado, Retirado) según el curso seleccionado:
    '''),
    html.Br(),
    html.Div(["Curso: ",
              dcc.Dropdown(id='curso', value=33, 
                           options=[33,171,8014,9003,9070,9085,9119,9130,9147,9238,9254,9500,9556,9670,9773,9853,9991])]),
    html.Br(),
    dcc.Graph(id='bar-promedios'),
    dcc.Graph(id='bar-exito'),
    html.Div(children='''
        De acuerdo con las correlaciones hayadas entre los factores y el éxito académico, se seleccionaron unos factores de riesgo
        importantes para predecir la necesidad de acompañamiento de un estudiante. 
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
    html.Div(children='''La predicción del estado estudiantil es:'''), 
    html.H6(html.B(id='my-output')),
    ]
)


@app.callback(
    Output(component_id='bar-promedios', component_property='figure'),
    Output(component_id='bar-exito', component_property='figure'),
    Input(component_id='curso', component_property='value')
)

def update_graphs(curso):

    # Consulta sobre los promedios del curso
    cursor = engine.cursor()
    query_curso = """
    SELECT 
    AVG("Curricular units 1st sem (grade)") AS Promedio_1er_Semestre,
    AVG("Curricular units 2nd sem (grade)") AS Promedio_2do_Semestre
    FROM academic
    WHERE "Course"= {};""".format(curso)
    cursor.execute(query_curso)
    result = cursor.fetchall()

    first = result[0][0]
    second = result[0][1]

    #Consulta sobre los promedios generales
    query_general = """
    SELECT 
    AVG("Curricular units 1st sem (grade)") AS Promedio_1er_Semestre,
    AVG("Curricular units 2nd sem (grade)") AS Promedio_2do_Semestre
    FROM academic;"""
    cursor.execute(query_general)
    result_general = cursor.fetchall()

    first_general = result_general[0][0]
    second_general = result_general[0][1]

    # Crear la figura del gráfico 
    fig_promedios = go.Figure()

    # Agregar las barras para primer semestre
    fig_promedios.add_trace(go.Bar(
        x=["Promedio 1er Semestre"],
        y=[first],
        name='1er Semestre',
        text=['{:.2f}'.format(first)],
        textposition='auto',
        marker=dict(color='#003399')
    ))

    fig_promedios.add_trace(go.Bar(
        x=["Promedio 1er Semestre (General)"],
        y=[first_general],
        name='1er Semestre (General)',
        text=['{:.2f}'.format(first_general)],
        textposition='auto',
        marker=dict(color='#0099FF')
    ))

    # Agregar las barras para segundo semestre

    fig_promedios.add_trace(go.Bar(
        x=["Promedio 2do Semestre"],
        y=[second],
        name='2do Semestre',
        text=['{:.2f}'.format(second)],
        textposition='auto',
        marker=dict(color='#660000')
    ))

    fig_promedios.add_trace(go.Bar(
        x=["Promedio 2do Semestre (General)"],
        y=[second_general],
        name='2do Semestre (General)',
        text=['{:.2f}'.format(second_general)],
        textposition='auto',
        marker=dict(color='#CC0000')
    ))

    fig_promedios.update_layout(barmode='group', title="Promedios por curso vs Promedios generales")

    #Consulta sobre el exito estudiantil
    query_exito = """
    SELECT "Target", COUNT(*) as number_of_students
    FROM academic
    WHERE "Course" = {}
    GROUP BY "Target"
    ORDER BY number_of_students DESC;
    """.format(curso)
    cursor.execute(query_exito)
    result_exito = cursor.fetchall()

    # Crear la figura del gráfico de exito
    fig_exito = go.Figure()

    fig_exito.add_trace(go.Bar(
        x=[result_exito[0][0]],
        y=[result_exito[0][1]],
        name=result_exito[0][0],
        text=['{:.2f}'.format(result_exito[0][1])],
        textposition='auto',
        marker=dict(color='#660000')
    ))

    fig_exito.add_trace(go.Bar(
        x=[result_exito[1][0]],
        y=[result_exito[1][1]],
        name=result_exito[1][0],
        text=['{:.2f}'.format(result_exito[1][1])],
        textposition='auto',
        marker=dict(color='#CC0000')
    ))

    fig_exito.add_trace(go.Bar(
        x=[result_exito[2][0]],
        y=[result_exito[2][1]],
        name=result_exito[2][0],
        text=['{:.2f}'.format(result_exito[2][1])],
        textposition='auto',
        marker=dict(color='#0099FF')
    ))

    fig_exito.update_layout(barmode='group', title="Exito estudiantil según curso")

    return fig_promedios, fig_exito

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
        
def update_prediction(val1, val2, val3, val4, val5, val6, val7, val8):
    # Predicción del estado estudiantil
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

    return prediction

if __name__ == '__main__':
    app.run_server(debug=False)