#%% Librerias
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.estimators import BayesianEstimator
from pgmpy.sampling import BayesianModelSampling
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD

#%% Red bayesiana para diagnosticar cáncer de pulmón

# Estructura de la red
model_lung = BayesianNetwork([("asia","tub"),("tub","either"),("either","xray"),("either","dysp"),("bronc","dysp"),("lung","either"),("smoke","lung"),("smoke","bronc")])

# Importar librerias
import pandas as pd
from sklearn.model_selection import train_test_split

# Subir csv
data = pd.read_csv('data_asia.csv')
data = data.replace({'yes': 1, 'no': 0})
data = data.drop('index', axis=1)

#%% Dividir datos en train y test
X_train, X_test = train_test_split(data, test_size=0.2, random_state=42)

#%% Emplear el módulo de ajuste de pgmpy para ajustar la CPDs del nuevo modelo
emv_lung = MaximumLikelihoodEstimator(model = model_lung, data = X_train)

# Obtener las CPDs ajustadas
cpds = emv_lung.get_parameters()
for cpd in cpds:
    print(cpd)

#%%
cpdem_asia = emv_lung.estimate_cpd (node = "asia")
print(cpdem_asia)
cpdem_tub = emv_lung.estimate_cpd(node = "tub")
print(cpdem_tub)
cpdem_either =emv_lung.estimate_cpd(node = "either")
print(cpdem_either)
cpdem_xray = emv_lung.estimate_cpd (node = "xray")
print(cpdem_xray)
cpdem_dysp = emv_lung.estimate_cpd(node = "dysp")
print(cpdem_dysp)
cpdem_bronc = emv_lung.estimate_cpd(node = "bronc")
print(cpdem_bronc)
cpdem_lung = emv_lung.estimate_cpd(node = "lung")
print(cpdem_lung)
cpdem_smoke = emv_lung.estimate_cpd(node = "smoke")
print(cpdem_smoke)

#%% Predecir para la variable de lung

from pgmpy.inference import VariableElimination

#Asociar las CPDs al modelo
model_lung.add_cpds(cpdem_asia,cpdem_tub,cpdem_either,cpdem_xray,cpdem_dysp,cpdem_bronc,cpdem_lung,cpdem_smoke)

#Revisar que el modelo esté completo
print(model_lung.check_model())

#%%

# Crear un objeto de inferencia
inference = VariableElimination(model_lung)

# Crear una lista para guardar las predicciones
predictions = []

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
