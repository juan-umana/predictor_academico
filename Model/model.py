#%% Librerias
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.estimators import BayesianEstimator
from pgmpy.sampling import BayesianModelSampling
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

#%% Red bayesiana para predecir el éxito académico

# Estructura de la red
model_success = BayesianNetwork([("grade_1","grade_2"),("grade_2","success"),
                              ("age","success"),
                              ("inflation","success"),
                              ("scholarship","success"),
                              ("course","success"),
                              ("tuition","success"),
                              ("application","success")])

# Importar librerias
import pandas as pd
from sklearn.model_selection import train_test_split

# Subir csv
data = pd.read_csv('data_model.csv')

#%% Dividir datos en train y test
X_train, X_test = train_test_split(data, test_size=0.2, random_state=42)

#%% Emplear el módulo de ajuste de pgmpy para ajustar la CPDs del nuevo modelo
emv_success = MaximumLikelihoodEstimator(model = model_success, data = X_train)

# Obtener las CPDs ajustadas
cpds = emv_success.get_parameters()
for cpd in cpds:
    print(cpd)

#%%
cpdem_grade_1 = emv_success.estimate_cpd (node = "grade_1")
print(cpdem_grade_1)
cpdem_grade_2 = emv_success.estimate_cpd(node = "grade_2")
print(cpdem_grade_2)
cpdem_age =emv_success.estimate_cpd(node = "age")
print(cpdem_age)
cpdem_inflation = emv_success.estimate_cpd (node = "inflation")
print(cpdem_inflation)
cpdem_scholarship = emv_success.estimate_cpd(node = "scholarship")
print(cpdem_scholarship)
cpdem_course = emv_success.estimate_cpd(node = "course")
print(cpdem_course)
cpdem_tuition = emv_success.estimate_cpd(node = "tuition")
print(cpdem_tuition)
cpdem_application = emv_success.estimate_cpd(node = "application")
print(cpdem_application)

#%% Predecir para la variable de lung

from pgmpy.inference import VariableElimination

#Asociar las CPDs al modelo
model_success.add_cpds(cpdem_grade_1,
                       cpdem_grade_2,
                       cpdem_age,
                       cpdem_inflation,
                       cpdem_scholarship,
                       cpdem_course,
                       cpdem_tuition,
                       cpdem_application)

#Revisar que el modelo esté completo
print(model_success.check_model())

#%%

# Crear un objeto de inferencia
inference = VariableElimination(model_success)

# Crear una lista para guardar las predicciones
predictions = []

## TODO from here

for _, row in X_test.iterrows():

    # Crear un diccionario de evidencias con los datos de cada fila en datos de prueba
    evidence = {variable: row[variable] for variable in row.index if variable!="lung"}
    
    # Realizar la inferencia para obtener la CPD de "lung" dado la evidencia
    result = inference.query(variables=['lung'], evidence=evidence)
    
    # Agregar la predicción a la lista de predicciones
    predictions.append(int(result.values[1]))  # El índice 1 corresponde a 'lung' siendo 1 (cáncer de pulmón)

#%% Obtener metricas

from sklearn.metrics import accuracy_score, confusion_matrix

# Obtener el ground truth para comparar las predicciones
y_true = X_test['lung'].tolist()

# Calcular la exactitud del modelo
accuracy = accuracy_score(y_true, predictions)
print(f'Exactitud (Accuracy): {accuracy}')

# Calcular la matriz de confusión
confusion = confusion_matrix(y_true, predictions)

# Extraer los valores de Verdaderos positivos, falsos positivos, falsos negativos y verdaderos negativos.
tn, fp, fn, tp = confusion.ravel()
print(f'Verdaderos Positivos: {tp}')
print(f'Falsos Positivos: {fp}')
print(f'Verdaderos Negativos: {tn}')
print(f'Falsos Negativos: {fn}')
