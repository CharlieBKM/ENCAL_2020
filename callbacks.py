import dash_table as dt
import dash_core_components as dcc
#import plotly.express as pxxs
import plotly.express as px
import dash_html_components as html
# import dash IO and graph objects
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
# Plotly graph objects to render graph plots

# Import dash html, bootstrap components, and tables for datatables
import dash_table

# Import app
from app import app
import pandas as pd

# Import custom data.py
import data



# Import data from data.py file


eni_complete=data.eni_complete

preguntas=data.preguntas

etiquetas=data.etiquetas



listado_resultados=['Edad', 'Sexo', 
                    'Órgano de Operación Administrativa Desconcentrado (OOAD)', 'Regiones', 
                    'Nivel']



#Resultados

@app.callback(
    Output('container', 'children'),
    [Input('add-chart', 'n_clicks')],
    [State('container', 'children')]
)
def display_graphs(n_clicks, div_children):
    new_child = html.Div(
        style={'width': '100%', 'display': 'inline-block', 'padding': 0, 'font-family': 'Montserrat',},
        children=[

            dcc.Dropdown(
                style={'color':'#13322B','background':'#D4C19C', 'font-weight': 'bold', 'cursor': 'pointer'},
                id={
                    'type': 'dynamic-dpn-s',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in preguntas.seccion.unique()],
                value= 'Satisfacción y Atención',
                clearable=False
            ),


            dcc.RadioItems(
                id={
                    'type': 'dynamic-choice',
                    'index': n_clicks
                },
                labelStyle={'display': 'block'},
                inputStyle={"margin-right": "20px"} 
            ),

            html.Hr(style={'border':'none'},),

            dcc.Dropdown(
                style={'width': '550px','color':'#13322B','background':'#DDCEB1', 'font-weight': 'bold', 'cursor': 'pointer'},
                id={
                    'type': 'dynamic-dpn-subs',
                    'index': n_clicks
                },
                options=[{'label': s, 'value': s} for s in listado_resultados],
                value='Nivel', 
                multi=False
            ),

            html.Div(id={
                          'type': 'title-sec-preg-des', 
                          'index': n_clicks
                        }, 
                        style={"textAlign": "center"}
            ),

            html.Div(id={
                        'type': 'dynamic-table',
                        'index': n_clicks
                }              
            ),
            
            html.Hr(style={'border':'none'},),
            html.Div(id={
                          'type': 'regiones', 
                          'index': n_clicks
                        }
            ),

            dcc.Graph(
                id={
                    'type': 'dynamic-graph',
                    'index': n_clicks
                },
                figure={}
            )
        ]
    )
    div_children.append(new_child)
    return div_children

#Radio options

@app.callback(
    Output({'type': 'dynamic-choice', 'index': MATCH}, 'options'),
    Input({'type': 'dynamic-dpn-s', 'index': MATCH},'value'))
def set_variable_options(chosen_seccion):
    return [{'label': i, 'value': i} for i in preguntas[preguntas['seccion']==chosen_seccion].pregunta]


@app.callback(
    Output({'type': 'dynamic-choice', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-choice', 'index': MATCH},'options'))
def set_variable_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output({'type': 'dynamic-dpn-subs', 'index':MATCH}, 'options'),
    Output({'type': 'dynamic-dpn-subs', 'index':MATCH}, 'value'),
     Input({'type': 'dynamic-choice', 'index': MATCH},'value')
    )
def set_subcat(pregunta):
    if pregunta != '¿Cuál fue el motivo o problema de salud por el que acudió a la unidad médica en su última visita?':
        return [[{'label': s, 'value': s} for s in listado_resultados],'Nivel']
    else:
        return [[{'label': 'Nacional', 'value': 'Nacional'}],'Nacional']

####Title: Section - Question - Reported


@app.callback(
     Output({'type': 'title-sec-preg-des', 'index': MATCH}, 'children'),
    [Input({'type': 'dynamic-dpn-s', 'index': MATCH},'value'),
     Input({'type': 'dynamic-choice', 'index': MATCH}, 'value'),
     Input({'type': 'dynamic-dpn-subs', 'index': MATCH},'value')]
    )
def display_title(seccion, pregunta, desglose):
    return html.Div([
        html.H3('{}'.format(seccion)),
        html.H3('{}'.format(pregunta)),
        html.H3('{}'.format(desglose))
        ])

####Result table
@app.callback(
    Output({'type': 'dynamic-table', 'index': MATCH}, 'children'),
    [Input({'type': 'dynamic-choice', 'index': MATCH}, 'value'),
     Input({'type': 'dynamic-dpn-subs', 'index': MATCH}, 'value')])
def set_display_table(pregunta_percep, subsecciones_percep):
    if (pregunta_percep != None):
        eninac_df_filter = eni_complete[eni_complete['pregunta'] == pregunta_percep]
        eninac_df_filter_nac = eninac_df_filter[eninac_df_filter['sub_cat'] == 'Nacional']
        eninac_df_filter_nac = eninac_df_filter_nac.sort_values('Codigo')
        column_list = eninac_df_filter_nac["lab_categoria"].tolist()
        column_list=['Desglose'] + column_list
        if pregunta_percep != '¿Cuál fue el motivo o problema de salud por el que acudió a la unidad médica en su última visita?':
            eninac_df_filter = eninac_df_filter[eninac_df_filter['sub_cat'] == subsecciones_percep]
            eninac_df_filter = eninac_df_filter_nac.append(eninac_df_filter)
            enanic_df_pivot = eninac_df_filter.pivot(index='Desglose', columns='lab_categoria')['Porcentaje'].reset_index()
            enanic_df_pivot = enanic_df_pivot.reindex(columns=column_list)
            enanic_df_pivot = enanic_df_pivot.sort_values(column_list[1], ascending=False)
            return  [dt.DataTable(style_data={'textAlign': 'center',},
                              style_header={'textAlign': 'center', 'font-weight':'bold',},
                              style_cell={'font-family':'Montserrat',
                              'width':95, 'maxWidth':95, 'minWidth':95, 'whiteSpace':'normal'},
                    id='table',
                    columns=[{"name": i, "id":i} for i in enanic_df_pivot.columns],
                    data=enanic_df_pivot.to_dict('records'),
                    style_data_conditional=(
                        [{ 'if': {
                                    'filter_query': '{Desglose} = Nacional'
                                 },
                                 'backgroundColor': '#EBEDEF',
                         },
                        ])
                    )]
        else:
            eninac_df_filter = eninac_df_filter[eninac_df_filter['sub_cat'] == "Nivel"]
            eninac_df_filter = eninac_df_filter_nac.append(eninac_df_filter)
            enanic_df_pivot = pd.pivot_table(eninac_df_filter, values='Porcentaje',
                    index=['lab_categoria'], columns=['Desglose'])
            enanic_df_pivot = enanic_df_pivot.reset_index()
            enanic_df_pivot = enanic_df_pivot.sort_values(by=['Nacional'], ascending=False)
            enanic_df_pivot = enanic_df_pivot.drop(['Primer nivel', 'Segundo nivel', 'Tercer nivel'],
                                 axis = 1) 
            enanic_df_pivot = enanic_df_pivot.rename(columns={'lab_categoria': 'Desglose', 
                                                    'Nacional': 'Porcentaje'})    
            return  [dt.DataTable(style_data={'textAlign': 'center',},
                              style_header={'textAlign': 'center', 'font-weight':'bold',},
                              style_cell={'font-family':'Montserrat',
                              'width':'180px', 'maxWidth':'180px', 'minWidth':'180px', 'whiteSpace':'normal'},

                    id='table',
                    columns=[{"name": i, "id":i} for i in enanic_df_pivot.columns],
                    data=enanic_df_pivot.to_dict('records'),
                    style_data_conditional=(
                        [{ 'if': {
                                    'column_id': 'Desglose'
                                 },
                                 'textAlign': 'right',
                         },
                        ])
                    )]
    else:
        print("Información no disponible")
        return[]

####Regions


@app.callback(
     Output({'type': 'regiones', 'index': MATCH}, 'children'),
     Input({'type': 'dynamic-dpn-subs', 'index': MATCH},'value')
    )
def display_title(desglose):
    if desglose == 'Regiones':
        return html.Div(
                    [
                    html.Div([
                        html.Div('Norte: AGS, COAH, CHIH, DGO, NL, SLP, TMS, ZAC'),
                        html.Div('Centro: CDMX S, CDMX N, MEX O, MEX P, HGO, GTO, MOR, PUE, QRO, TLAX'),
                        html.Div('Occidente: BC, BCS, COL, JAL, MICH, NAY, SIN, SON'),
                        html.Div('Sureste: CAMP, CHIS, GRO, OAX, QR, TAB, VER N, VER S, YUC')
                    ],style={'width': '49%', 'display':'inline-block', 'position': 'relative',
                             'float': 'left', 'top':'-25%', 'left': '25%', 
                             'transform': 'translate(-45%, 80%)'}),

                    html.Div(
                        html.Img(src=app.get_asset_url('Mapa de regiones Eni 2021.png'), 
                            style = {'height':'60%', 'width':'60%'}),
                        style={'width': '49%', 'display': 'flex',
                                'justify-content': 'center', 'align-items': 'center'}
                        )
        ])
    else:
        return  html.Div([
        html.Div(''),
        ])



####Callback to a Bar Chart Results, takes data request from dropdown
@app.callback(
    Output({'type': 'dynamic-graph', 'index': MATCH}, 'figure'),
    [Input({'type': 'dynamic-choice', 'index': MATCH}, 'value'),
    Input({'type': 'dynamic-dpn-subs', 'index': MATCH},'value')])
def update_bar_chart(pregunta_percep, subsecciones_percep):
    if (pregunta_percep != None):
        eninac_df_filter = eni_complete[eni_complete['pregunta'] == pregunta_percep]
        eninac_df_filter_nac = eninac_df_filter[eninac_df_filter['sub_cat'] == 'Nacional']
        eninac_df_filter_nac = eninac_df_filter_nac.sort_values('Codigo')
        column_list = eninac_df_filter_nac["lab_categoria"].tolist()
        column_list=['Desglose'] + column_list
        if pregunta_percep != '¿Cuál fue el motivo o problema de salud por el que acudió a la unidad médica en su última visita?':
            eninac_df_filter = eninac_df_filter[eninac_df_filter['sub_cat'] == subsecciones_percep]
            eninac_df_filter = eninac_df_filter_nac.append(eninac_df_filter)
            eninac_df_filter = eninac_df_filter.sort_values(by=['Codigo'])
            enanic_df_pivot = eninac_df_filter.pivot(index='Desglose', columns='lab_categoria')['Porcentaje'].reset_index()
            enanic_df_pivot = enanic_df_pivot.reindex(columns=column_list)
            enanic_df_pivot = enanic_df_pivot.sort_values(column_list[1], ascending=False)
            category_list = enanic_df_pivot["Desglose"].tolist()
            fig = px.bar(eninac_df_filter, x="Desglose", y="Porcentaje", color='lab_categoria',
                text = 'Porcentaje', template = "seaborn")
            fig.update_traces(texttemplate='%{text:2.0f}', textposition = "inside",
                     insidetextanchor = 'middle', textfont_size=14)
            fig.update_layout({
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)'
                            })
            fig.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')
            fig.update_layout(
                xaxis={'categoryorder':'array', 'categoryarray':category_list},
                font=dict(
                        size = 14
                        ),
                legend=dict(title=None))
            return fig
        else:
            eninac_df_filter = eninac_df_filter[eninac_df_filter['sub_cat'] == "Nivel"]
            eninac_df_filter = eninac_df_filter_nac.append(eninac_df_filter)
            enanic_df_pivot = pd.pivot_table(eninac_df_filter, values='Porcentaje',
                    index=['lab_categoria'], columns=['Desglose'])
            enanic_df_pivot = enanic_df_pivot.reset_index()
            enanic_df_pivot = enanic_df_pivot.sort_values(by=['Nacional'])
            enanic_df_pivot = enanic_df_pivot.drop(['Primer nivel', 'Segundo nivel', 'Tercer nivel'],
                                 axis = 1)
            enanic_df_pivot = enanic_df_pivot.rename(columns={'lab_categoria': 'Desglose'})
            fig = px.bar(enanic_df_pivot, x="Nacional", y="Desglose",
                text = 'Nacional', template = "seaborn")
            fig.update_traces(texttemplate='%{text:2.0f}', textposition = "inside",
                     insidetextanchor = 'middle', textfont_size=14)
            fig.update_layout({
                        'plot_bgcolor': 'rgba(0, 0, 0, 0)'
                            })
            fig.update_layout(uniformtext_minsize=14, uniformtext_mode='hide')
            fig.update_layout(
                font=dict(
                        size = 14
                        ),
                legend=dict(title=None))
            return fig     
    else:
        print("Información no disponible")
        return[]


