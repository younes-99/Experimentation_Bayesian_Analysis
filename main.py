import pandas as pd 
import numpy as np
import streamlit as st
st.set_page_config(layout="wide")
from stats_engine import mvt_bayesian_calculator_manual




st.markdown('\n')
st.markdown('\n')
mi_variants = st.number_input('Insert Number of Variation',value = 2,step = 1)
manual_input_columns = st.columns(2) 
mi_sample_size_dict = {}
mi_sample_conversion_dict = {}
 
with manual_input_columns[0]:
    for variant in range(0,mi_variants):
        if variant == 0:
            mi_sample_size_dict[variant] = st.number_input(f"Sample Size for Control",step =1,value  = 500)
        else:
            mi_sample_size_dict[variant] = st.number_input(f"Sample Size for Variant {variant}",step = 1,value = 500)

with manual_input_columns[1]:
    for variant in range(0,mi_variants):
        if variant == 0 :
            mi_sample_conversion_dict[variant] = st.number_input(f"Conversion for Control",step = 1,value = 200)
        else:
            mi_sample_conversion_dict[variant] = st.number_input(f"Conversion for Variant {variant}",step = 1, value = 200)
expected_loss_type = st.radio('Expected loss type', ['Relative (%)','Absolute (%)'],horizontal=True)
expected_loss_threshold = st.number_input('Expected loss threshold',min_value=0.0,format='%f',value=2.0)
# if show_sql == 'Yes':                
    # code = f'''PUT file://<file_path>/<file_name> @{st.session_state['table']}/ \n\nCOPY INTO "SANDBOX"."DATA_LOADING"."{st.session_state['table']}" FROM @/ui1675186369009\nON_ERROR = 'SKIP_FILE_0' PURGE = TRUE;'''
    # st.code(code, language='plsql')  


if st.button("Submit"):
    analysis = mvt_bayesian_calculator_manual(mi_sample_size_dict,mi_sample_conversion_dict,expected_loss_threshold,expected_loss_type)
    analysis.get_probablities()
    st.write("")
    analysis.plotting_graph()