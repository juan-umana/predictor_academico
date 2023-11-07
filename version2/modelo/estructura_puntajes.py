import pandas as pd

df = pd.read_csv("C:/Users/jd.umana10/Documents/GitHub/predictor_academico_2/aprendizaje_estructura/data_modified.csv")
print(df.head())
print(df.describe())
print(df.columns)

excluded_edges = [
    # No deben existir enlaces hacia la ocupación o cualificación de los padres
                  ('marital_status','father_occupation'), ('application_mode','father_occupation'), ('application_order','father_occupation'), ('course','father_occupation'),
                  ('attendance','father_occupation'), ('prev_qualification','father_occupation'), ('prev_qualification_grade','father_occupation'),
                  ('nationality','father_occupation'), ('mother_qualification','father_occupation'), ('father_qualification','father_occupation'),
                  ('mother_occupation','father_occupation'), ('age','father_occupation'), ('admission_grade','father_occupation'),
                  ('displaced','father_occupation'), ('special_needs','father_occupation'), ('debtor','father_occupation'), ('tuition','father_occupation'), ('gender','father_occupation'),
                  ('scholarship','father_occupation'), ('international','father_occupation'), ('units_1_credited','father_occupation'),
                  ('units_1_enrolled','father_occupation'), ('units_1_evaluations','father_occupation'), ('units_1_approved','father_occupation'),
                  ('units_1_grade','father_occupation'), ('units_1_wo_evaluations','father_occupation'), ('units_2_credited','father_occupation'),
                  ('units_2_enrolled','father_occupation'), ('units_2_evaluations','father_occupation'), ('units_2_approved','father_occupation'),
                  ('units_2_grade','father_occupation'), ('units_2_wo_evaluations','father_occupation'), ('unemployment_rate','father_occupation'),
                  ('inflation_rate','father_occupation'), ('gdp','father_occupation'), ('target','father_occupation'),
                  ('marital_status','mother_occupation'), ('application_mode','mother_occupation'), ('application_order','mother_occupation'), ('course','mother_occupation'),
                  ('attendance','mother_occupation'), ('prev_qualification','mother_occupation'), ('prev_qualification_grade','mother_occupation'),
                  ('nationality','mother_occupation'), ('mother_qualification','mother_occupation'), ('father_qualification','mother_occupation'),
                  ('father_occupation','mother_occupation'), ('age','mother_occupation'), ('admission_grade','mother_occupation'),
                  ('displaced','mother_occupation'), ('special_needs','mother_occupation'), ('debtor','mother_occupation'), ('tuition','mother_occupation'), ('gender','mother_occupation'),
                  ('scholarship','mother_occupation'), ('international','mother_occupation'), ('units_1_credited','mother_occupation'),
                  ('units_1_enrolled','mother_occupation'), ('units_1_evaluations','mother_occupation'), ('units_1_approved','mother_occupation'),
                  ('units_1_grade','mother_occupation'), ('units_1_wo_evaluations','mother_occupation'), ('units_2_credited','mother_occupation'),
                  ('units_2_enrolled','mother_occupation'), ('units_2_evaluations','mother_occupation'), ('units_2_approved','mother_occupation'),
                  ('units_2_grade','mother_occupation'), ('units_2_wo_evaluations','mother_occupation'), ('unemployment_rate','mother_occupation'),
                  ('inflation_rate','mother_occupation'), ('gdp','mother_occupation'), ('target','mother_occupation'),
                  ('marital_status','father_qualification'), ('application_mode','father_qualification'), ('application_order','father_qualification'), ('course','father_qualification'),
                  ('attendance','father_qualification'), ('prev_qualification','father_qualification'), ('prev_qualification_grade','father_qualification'),
                  ('nationality','father_qualification'), ('mother_qualification','father_qualification'), ('father_occupation','father_qualification'),
                  ('mother_qualification','father_qualification'), ('age','father_qualification'), ('admission_grade','father_qualification'),
                  ('displaced','father_qualification'), ('special_needs','father_qualification'), ('debtor','father_qualification'), ('tuition','father_qualification'), ('gender','father_qualification'),
                  ('scholarship','father_qualification'), ('international','father_qualification'), ('units_1_credited','father_qualification'),
                  ('units_1_enrolled','father_qualification'), ('units_1_evaluations','father_qualification'), ('units_1_approved','father_qualification'),
                  ('units_1_grade','father_qualification'), ('units_1_wo_evaluations','father_qualification'), ('units_2_credited','father_qualification'),
                  ('units_2_enrolled','father_qualification'), ('units_2_evaluations','father_qualification'), ('units_2_approved','father_qualification'),
                  ('units_2_grade','father_qualification'), ('units_2_wo_evaluations','father_qualification'), ('unemployment_rate','father_qualification'),
                  ('inflation_rate','father_qualification'), ('gdp','father_qualification'), ('target','father_qualification'),
                  ('marital_status','mother_qualification'), ('application_mode','mother_qualification'), ('application_order','mother_qualification'), ('course','mother_qualification'),
                  ('attendance','mother_qualification'), ('prev_qualification','mother_qualification'), ('prev_qualification_grade','mother_qualification'),
                  ('nationality','mother_qualification'), ('mother_occupation','mother_qualification'), ('father_qualification','mother_qualification'),
                  ('father_qualification','mother_qualification'), ('age','mother_qualification'), ('admission_grade','mother_qualification'),
                  ('displaced','mother_qualification'), ('special_needs','mother_qualification'), ('debtor','mother_qualification'), ('tuition','mother_qualification'), ('gender','mother_qualification'),
                  ('scholarship','mother_qualification'), ('international','mother_qualification'), ('units_1_credited','mother_qualification'),
                  ('units_1_enrolled','mother_qualification'), ('units_1_evaluations','mother_qualification'), ('units_1_approved','mother_qualification'),
                  ('units_1_grade','mother_qualification'), ('units_1_wo_evaluations','mother_qualification'), ('units_2_credited','mother_qualification'),
                  ('units_2_enrolled','mother_qualification'), ('units_2_evaluations','mother_qualification'), ('units_2_approved','mother_qualification'),
                  ('units_2_grade','mother_qualification'), ('units_2_wo_evaluations','mother_qualification'), ('unemployment_rate','mother_qualification'),
                  ('inflation_rate','mother_qualification'), ('gdp','mother_qualification'), ('target','mother_qualification'),
    # No deben existir enlaces hacia la edad
                  ('marital_status','age'), ('application_mode','age'), ('application_order','age'), ('course','age'),
                  ('attendance','age'), ('prev_qualification','age'), ('prev_qualification_grade','age'),
                  ('nationality','age'), ('mother_qualification','age'), ('father_qualification','age'),
                  ('mother_occupation','age'), ('father_occupation','age'), ('admission_grade','age'),
                  ('displaced','age'), ('special_needs','age'), ('debtor','age'), ('tuition','age'), ('gender','age'),
                  ('scholarship','age'), ('international','age'), ('units_1_credited','age'),
                  ('units_1_enrolled','age'), ('units_1_evaluations','age'), ('units_1_approved','age'),
                  ('units_1_grade','age'), ('units_1_wo_evaluations','age'), ('units_2_credited','age'),
                  ('units_2_enrolled','age'), ('units_2_evaluations','age'), ('units_2_approved','age'),
                  ('units_2_grade','age'), ('units_2_wo_evaluations','age'), ('unemployment_rate','age'),
                  ('inflation_rate','age'), ('gdp','age'), ('target','age'),
    # No deben existir enlaces hacia el género 
                  ('marital_status','gender'), ('application_mode','gender'), ('application_order','gender'), ('course','gender'),
                  ('attendance','gender'), ('prev_qualification','gender'), ('prev_qualification_grade','gender'),
                  ('nationality','gender'), ('mother_qualification','gender'), ('father_qualification','gender'),
                  ('mother_occupation','gender'), ('father_occupation','gender'), ('admission_grade','gender'),
                  ('displaced','gender'), ('special_needs','gender'), ('debtor','gender'), ('tuition','gender'), ('age','gender'),
                  ('scholarship','gender'), ('international','gender'), ('units_1_credited','gender'),
                  ('units_1_enrolled','gender'), ('units_1_evaluations','gender'), ('units_1_approved','gender'),
                  ('units_1_grade','gender'), ('units_1_wo_evaluations','gender'), ('units_2_credited','gender'),
                  ('units_2_enrolled','gender'), ('units_2_evaluations','gender'), ('units_2_approved','gender'),
                  ('units_2_grade','gender'), ('units_2_wo_evaluations','gender'), ('unemployment_rate','gender'),
                  ('inflation_rate','gender'), ('gdp','gender'), ('target','gender'),
    # No deben existir enlaces hacia la tasa de inflación, excepto gdp y unemployement_rate
                  ('marital_status','inflation_rate'), ('application_mode','inflation_rate'), ('application_order','inflation_rate'), ('course','inflation_rate'),
                  ('attendance','inflation_rate'), ('prev_qualification','inflation_rate'), ('prev_qualification_grade','inflation_rate'),
                  ('nationality','inflation_rate'), ('mother_qualification','inflation_rate'), ('father_qualification','inflation_rate'),
                  ('mother_occupation','inflation_rate'), ('father_occupation','inflation_rate'), ('admission_grade','inflation_rate'),
                  ('displaced','inflation_rate'), ('special_needs','inflation_rate'), ('debtor','inflation_rate'), ('tuition','inflation_rate'), ('age','inflation_rate'),
                  ('scholarship','inflation_rate'), ('international','inflation_rate'), ('units_1_credited','inflation_rate'),
                  ('units_1_enrolled','inflation_rate'), ('units_1_evaluations','inflation_rate'), ('units_1_approved','inflation_rate'),
                  ('units_1_grade','inflation_rate'), ('units_1_wo_evaluations','inflation_rate'), ('units_2_credited','inflation_rate'),
                  ('units_2_enrolled','inflation_rate'), ('units_2_evaluations','inflation_rate'), ('units_2_approved','inflation_rate'),
                  ('units_2_grade','inflation_rate'), ('units_2_wo_evaluations','inflation_rate'),
                  ('gender','inflation_rate'), ('target','inflation_rate'),
    # No deben existir enlaces hacia el gdp, excepto inflation_rate y unemployement_rate
                  ('marital_status','gdp'), ('application_mode','gdp'), ('application_order','gdp'), ('course','gdp'),
                  ('attendance','gdp'), ('prev_qualification','gdp'), ('prev_qualification_grade','gdp'),
                  ('nationality','gdp'), ('mother_qualification','gdp'), ('father_qualification','gdp'),
                  ('mother_occupation','gdp'), ('father_occupation','gdp'), ('admission_grade','gdp'),
                  ('displaced','gdp'), ('special_needs','gdp'), ('debtor','gdp'), ('tuition','gdp'), ('age','gdp'),
                  ('scholarship','gdp'), ('international','gdp'), ('units_1_credited','gdp'),
                  ('units_1_enrolled','gdp'), ('units_1_evaluations','gdp'), ('units_1_approved','gdp'),
                  ('units_1_grade','gdp'), ('units_1_wo_evaluations','gdp'), ('units_2_credited','gdp'),
                  ('units_2_enrolled','gdp'), ('units_2_evaluations','gdp'), ('units_2_approved','gdp'),
                  ('units_2_grade','gdp'), ('units_2_wo_evaluations','gdp'),
                  ('gender','gdp'), ('target','gdp'),
    # No deben existir enlaces entre variables del segundo semestre y el primer semestre
                  ('units_2_credited','units_1_credited'),
                  ('units_2_enrolled','units_1_enrolled'),
                  ('units_2_evaluations','units_1_evaluations'),
                  ('units_2_approved','units_1_approved'),
                  ('units_2_grade','units_1_grade'),
                  ('units_2_wo_evaluations','units_1_wo_evaluations'),
    # No deben existir enlaces de target a otras variables
                  ('target','marital_status'), ('target','application_mode'), ('target','application_order'), ('target','course'),
                  ('target','attendance'), ('target','prev_qualification'), ('target','prev_qualification_grade'),
                  ('target','nationality'), ('target','mother_qualification'), ('target','father_qualification'),
                  ('target','mother_occupation'), ('target','father_occupation'), ('target','admission_grade'),
                  ('target','displaced'), ('target','special_needs'), ('target','debtor'), ('target','tuition'),
                  ('target','gender'), ('target','scholarship'), ('target','age'), ('target','international'),
                  ('target','units_1_credited'), ('target','units_1_enrolled'), ('target','units_1_evaluations'),
                  ('target','units_1_approved'), ('target','units_1_grade'), ('target','units_1_wo_evaluations'),
                  ('target','units_2_credited'), ('target','units_2_enrolled'), ('target','units_2_evaluations'),
                  ('target','units_2_approved'), ('target','units_2_grade'), ('target','units_2_wo_evaluations'),
                  ('target','unemployment_rate'), ('target','inflation_rate'), ('target','gdp')]

from pgmpy.estimators import HillClimbSearch
from pgmpy.estimators import BicScore

scoring_method = BicScore(data=df)
esth = HillClimbSearch(data=df)
estimated_modelh_2 = esth.estimate(
    scoring_method=scoring_method, max_indegree=2,
    black_list=excluded_edges, max_iter=int(1e4)
)
print(estimated_modelh_2)
print(estimated_modelh_2.nodes())
print(estimated_modelh_2.edges())

print(scoring_method.score(estimated_modelh_2))

# Visualization https://public.flourish.studio/visualisation/15582966/