# Improtant note: This data file would ordinarily be used to connect with a proper database server
# more likely PostgreSQL, but thats me. I do plan on rewritting this in the future for such implementations.
# With that said, this file will be be very slow to run and only to demonstrate data processing using
# functions and pandas along with providing a central file for data references
#
# Import Pandas
import pandas as pd



##Base de datos

eni_complete = pd.read_csv("data/EncalSS2020_complete_T_seccV3.csv")


preguntas=pd.read_csv("data/variables_EncalSS_2020.csv")

etiquetas=pd.read_csv("data/variables_etiquetas_EncalSS_2020.csv")
