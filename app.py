import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

app=dash.Dash()


df=pd.read_excel('Опросник .xlsx')
df=df.fillna(0)
selo=df['Адрес расположения Район'].unique()
regions=df['Cело/ джамоат'].unique()
area=df['Количество кустов (шт)'].unique()
buyers=df['Кто покупает лимоны'].unique()
max_distance=df['Расстояние от Фермерского хозяйства, земельного участка до центра района (км)2км'].max()
area_max=df['Количество кустов (шт)'].max()
area_min=df['Количество кустов (шт)'].min()
rows_numbers=df['Количество рядов посадки (ряда)'].unique()
max_row=df['Количество рядов посадки (ряда)'].max()
max_urozhaynost=df['Урожайность теплиц'].max()
max_optovaya=df['Оптовая цена продажи лимонов. Цена Фермер'].max()
columns_name=df.columns

app.layout = html.Div(
   
    [

        html.Div([
        html.Div([html.H1("Опросник")],
        style={'text-align':'center','color':'green'}),

        html.Div([
        html.H2("Адрес расположения Район") ,
        dcc.Dropdown(
            id='name-dropdown',
            options=selo,
            value = "All",
            style={'width':'80%', 'text-align':'center'},
            ),
            ],style={'width': '25%','text-align':'center', 'height':'9rem',  'display': 'inline-block', 'border': '1px solid black',}),
       
        html.Div([
        html.H2("Количество кустов (мин мах)") ,

        html.Div([
        dcc.Dropdown(
            id='area_min',
            options=area,
            value=area_min,
            style={'width':'50%', 'display': 'inline-block', },
            
            ),
        dcc.Dropdown(
             id='area_max',
            options=area,
            value=area_max,
            style={'width':'50%', 'display': 'inline-block'},
        )
        ]),
        ],
            style={'width': '30%','height':'9rem','vertical-align':'top', 'text-align':'center', 'display': 'inline-block', 'border': '1px solid black',}
        ),
         html.Div([
        html.H2("Расстояние от Фермерского хозяйства(км)") ,
        dcc.RangeSlider(0,max_distance, 1, value=[0,max_distance],
            id='distance',
            
            ),
            ],style={'width': '40%', 'height':'9rem','vertical-align':'top', 'text-align':'center',  'display': 'inline-block', 'border': '1px solid black',}
        ),
        html.Div([
        html.H2("Село/Чамоат") ,
        dcc.Checklist(
            id='opt-dropdown',
            options=regions, 
            value="All",
            className='checklist-new-line'
            ),
            ],style={'width': '25%', 'height':'20.17rem','display': 'inline-block', 'vertical-align':'top','border': '1px solid black',}
        ),
       
        html.Div([
        html.H2("Кто покупает лимоны") ,
        dcc.Checklist(
            id='buyers',
            options=buyers,
            value="All",
            className='checklist-new-line'
            ),
            ],
            style={'width': '30%', 'height':'20.17rem','display': 'inline-block', 'border': '1px solid black',}
        ),
        html.Div([
             html.Div([
        html.H2("Количество рядов посадки") ,
        dcc.RangeSlider(0,max_row, 1, value=[0,max_row],
            id='number_rows',
            ),            ],
             style={'border': '1px solid black',}
           
        ),


        html.Div([
        html.H2("Урожайность теплиц") ,
        dcc.RangeSlider(0,max_urozhaynost, value=[0,max_urozhaynost],
            id='urozhaynost',
            ),
            ],
            style={'border': '1px solid black',}        ),

        html.Div([
        html.H2("Оптовая цена продажи") ,
        dcc.RangeSlider(0,max_optovaya, value=[0,max_optovaya],
            id='optovaya_cena',
            ),
            ],
             style={'border': '1px solid black',}
            
        ),
        ],style={'width': '40%', 'display': 'inline-block','vertical-align':'top', 'border': '1px solid black',}
        ),
        html.Div([
        html.H2("Cтолбцы") ,
        dcc.Checklist(
            id='columns',
            options=columns_name, 
            className="columns",
            style={'margin':'0px'}
            ),
            ],
            style={'border': '1px solid black',}        ),
   
        ]),
        html.Hr(),
        html.Div(
            html.Iframe(id = 'display-selected-values', height = 500, width = 1200),)
            
     
    ]
)


@app.callback(
    dash.dependencies.Output('display-selected-values', 'srcDoc'),
    
    [
    dash.dependencies.Input('opt-dropdown', 'value'),
    dash.dependencies.Input('distance', 'value'),
    dash.dependencies.Input('area_min', 'value'),
    dash.dependencies.Input('area_max', 'value'),
    dash.dependencies.Input('buyers', 'value'),
    dash.dependencies.Input('number_rows', 'value'),
    dash.dependencies.Input('urozhaynost', 'value'),
    dash.dependencies.Input('optovaya_cena', 'value'),
    dash.dependencies.Input('columns', 'value'),
    ])
def set_display_children(v1, v2, v3,v4, v5, v6, v7, v8, v9):

    if v1=="All":
        new=df.loc[df['Cело/ джамоат'].isin(regions)]
    else:
        new=df.loc[df['Cело/ джамоат'].isin(v1)]

    rasstoyanie=[i for i in range(v2[0],v2[1]+1)]
    new1=new.loc[new['Расстояние от Фермерского хозяйства, земельного участка до центра района (км)2км'].isin(rasstoyanie)]
    
    
    kol_kustov=[i for i in range(v3,v4+1)]
    new2=new1.loc[new1['Количество кустов (шт)'].isin(kol_kustov)]
   

    if v5=="All":
        new3=new2.loc[new2['Кто покупает лимоны'].isin(buyers)]
    else:
        print(v5)
        new3=new2.loc[new2['Кто покупает лимоны'].isin(v5)]
    
  
    row_num=[i for i in range(v6[0],v6[1]+1)]
    new4=new3.loc[new3['Количество рядов посадки (ряда)'].isin(row_num)]
    
    urozhaynost_num=[i for i in range(v7[0],v7[1]+1)]
    new5=new4.loc[new4['Урожайность теплиц'].isin(urozhaynost_num)]

    optom_num=[i for i in range(v8[0],v8[1]+1)]
    new6=new5.loc[new5['Оптовая цена продажи лимонов. Цена Фермер'].isin(optom_num)]
       
    new7=new6[v9]
 
    distanceA=[new6['Расстояние от Фермерского хозяйства, земельного участка до центра района (км)2км'].mean(),new6['Расстояние от Фермерского хозяйства, земельного участка до центра района (км)2км'].median(), new6['Расстояние от Фермерского хозяйства, земельного участка до центра района (км)2км'].sum()]
    kolichestvo_kustovA=[new6['Количество кустов (шт)'].mean(),new6['Количество кустов (шт)'].median(), new6['Количество кустов (шт)'].sum()]
    kolichestvo_ryadov=[new6['Количество рядов посадки (ряда)'].mean(), new6['Количество рядов посадки (ряда)'].median(), new6['Количество рядов посадки (ряда)'].sum()]
    urozhaynost = [new6['Урожайность теплиц'].mean(), new6['Урожайность теплиц'].median(), new6['Урожайность теплиц'].sum()]
    optovaya_cena = [new6['Оптовая цена продажи лимонов. Цена Фермер'].mean(), new6['Оптовая цена продажи лимонов. Цена Фермер'].median(), new6['Оптовая цена продажи лимонов. Цена Фермер'].sum()]
    finalWrapped={' ':['Mean', 'Median','Sum'],'Расстояние от Фермерского хозяйства':[distanceA[0],distanceA[1],distanceA[2]],'Количество кустов (шт)':[kolichestvo_kustovA[0], kolichestvo_kustovA[1], kolichestvo_kustovA[2]], 'Количество рядов посадки (ряда)':[kolichestvo_ryadov[0],kolichestvo_ryadov[1],kolichestvo_ryadov[2]], 'Урожайность теплиц':[urozhaynost[0],urozhaynost[1],urozhaynost[2]], 'Оптовая цена продажи лимонов':[optovaya_cena[0],optovaya_cena[1],optovaya_cena[2]],}    
    finalTable=pd.DataFrame(finalWrapped)

    return new7.to_html(), finalTable.to_html()

if __name__ == '__main__':
    app.run_server()



