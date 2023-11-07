from pgmpy.inference import VariableElimination
import pickle

# Read model from PKL file 
filename='model.pkl'
file = open(filename, 'rb')
model_success = pickle.load(file)
file.close()

# Infering the posterior probability
infer = VariableElimination(model_success)

evidence = {'marital_status': 1, 'application_mode': 44, 'application_order': 1,
            'course': 9003, 'attendance': 1, 'prev_qualification': 39, 'nationality': 1,
            'displaced': 1, 'debtor': 0, 'tuition': 1, 'gender': 1, 'scholarship': 0,
            'international': 0, 'units_1_credited': 0, 'units_1_enrolled': 6,
            'units_1_approved': 6, 'units_1_grade': 14, 'units_2_credited': 0,
            'units_2_enrolled': 6, 'units_2_approved': 6, 'units_2_grade': 15,
            'unemployment_rate': 12, 'inflation_rate': 1, 'gdp': 2}

posterior_p = infer.query(["target"], evidence=evidence)
print(posterior_p)
