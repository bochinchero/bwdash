from dash import Dash, html, dcc, callback, Output, Input, register_page
import plotly.express as px
import pandas as pd
import datetime
import dash_bootstrap_components as dbc



# some constants
# range selection buttons
btnDailyList = dict(
                buttons=list([
                        dict(count=7,
                             label="7d",
                             step="day",
                             stepmode="backward"),
                        dict(count=30,
                             label="30d",
                             step="day",
                             stepmode="backward"),
                        dict(count=90,
                             label="90d",
                             step="day",
                             stepmode="backward"),
                        dict(step='all')
            ]))
btnMonthlyList = dict(
                buttons=list([
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=12,
                             label="12m",
                             step="month",
                             stepmode="backward"),
                        dict(count=24,
                             label="24m",
                             step="month",
                             stepmode="backward"),
                        dict(step='all')
            ]))

# color scale
dcrColorScale = [
[0, 'rgb(15, 16, 63)'],
[0.5, 'rgb(50, 213, 162)'],
[1, 'rgb(72, 100, 251)']
]
# bootstrap style for cards
cardStyle = "w-100 shadow-sm bg-white rounded border border-light"

# this function prepares the sliced data for pie charts, etc.
def dataSlicer(data,slice):
    # take the slice
    output = data.iloc[slice]
    # remove zero values
    output = output[output!=0]
    # sort descending
    output = output.sort_values(ascending=False)
    # return
    return output

# plotting and styling for pie chart
def pieChart(data, colorScale):
    # resample colors to the length provided
    colors = px.colors.sample_colorscale(colorScale, [n / (len(list(data.values)))
                                                      for n in range(len(list(data.values)))])
    figure = px.pie(data, values=data.values, names=data.index, hole=.3,
                             color_discrete_sequence=colors)
    figure.update_layout(legend=dict(
        bgcolor='rgba(255,255,255,0.7)',
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ))
    return figure

# this function does the plotting, styling, etc.
def stackedBsars(data, fTitle, fHeight, yTitle, colorsScale):
    # resample colors to the length provided
    colors = px.colors.sample_colorscale(colorsScale, [n / (len(list(data.columns.values)))
                                                      for n in range(len(list(data.columns.values)))])
    # estimate freq and set the btnDict accordingly
    freq = pd.infer_freq(data.index)
    match freq:
        case 'MS':
            btnDict = btnMonthlyList
        case 'M':
            btnDict = btnMonthlyList
        case 'W-MON':
            btnDict = btnMonthlyList
        case 'W':
            btnDict = btnMonthlyList
        case 'D':
            btnDict = btnDailyList
        case _:
            btnDict = btnDailyList

    figure = px.bar(data, x=data.index, y=list(data.columns.values),
                      color_discrete_sequence=colors, height=fHeight)

    figure.update_layout(
        xaxis=dict(
            rangeselector=btnDict,
            type="date"
        ),
        xaxis_title="Date",
        yaxis_title=yTitle,
        font=dict(family="Arial", size=12, color="#091440"),
        yaxis_tickprefix='$', yaxis_tickformat=',.0f'
    )
    figure.update_layout(
        plot_bgcolor='#F3F6F6'
    )
    figure.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='#596D81',
        gridcolor='#C4CBD2'
    )
    figure.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='#596D81',
        gridcolor='#C4CBD2'
    )
    figure.update_layout(legend=dict(
        title=None,
        bgcolor= 'rgba(255,255,255,0.7)',
        orientation="h",
        yanchor="top",
        y=0.99,
        xanchor="center",
        x=0.5
    ))
    return figure

data = pd.read_csv('https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/stream/dex_decred_org_VolUSD.csv')
data['date'] = pd.to_datetime(data['date'], utc=True, format='%Y-%m-%d')
data = data.set_index('date')

# prepare daily data
dailyData = data[-365:]
dailyData = dailyData.loc[(dailyData.sum(axis=1) != 0), (dailyData.sum(axis=0) != 0)]
dailyData = dailyData[dailyData.sum().sort_values(ascending=False).index]

# prepare weekly data
weeklyData = data.groupby(pd.Grouper(freq='W-MON')).sum()
weeklyData = weeklyData.loc[(weeklyData.sum(axis=1) != 0), (weeklyData.sum(axis=0) != 0)]
weeklyData = weeklyData[weeklyData.sum().sort_values(ascending=False).index]

# prepare monthly data
monthlyData = data.groupby(pd.Grouper(freq='MS')).sum()
monthlyData = monthlyData.loc[(monthlyData.sum(axis=1) != 0), (monthlyData.sum(axis=0) != 0)]
monthlyData = monthlyData[monthlyData.sum().sort_values(ascending=False).index]

# prepare data for the slices
lastMonthSplit = dataSlicer(monthlyData,-2)
curMonthSplit = dataSlicer(monthlyData,-1)
lastDaySplit = dataSlicer(dailyData,-1)
lastMonthSplitTitle = lastMonthSplit.name.strftime("%B %Y")
curMonthSplitTitle = curMonthSplit.name.strftime("%B %Y")
lastDaySplitTitle = lastDaySplit.name.strftime("%B %d, %Y")
last90dSplit = data[-90:].sum()
last6mo = monthlyData[-6:].sum()
lastyear = weeklyData[-52:].sum()


register_page(
    __name__,
    path='/',
    title='DCRDEX Statistics',
    name='DCRDEX Statistics'
)

figDaily = stackedBsars(dailyData, None, 600, 'Daily Volume (USD)', dcrColorScale)
figWeekly = stackedBsars(weeklyData, None, 600, 'Weekly Volume (USD)', dcrColorScale)
figMonthly = stackedBsars(monthlyData, None, 600, 'Monthly Volume (USD)', dcrColorScale)
figCurMonth = pieChart(curMonthSplit, dcrColorScale)
figLastMonth = pieChart(lastMonthSplit, dcrColorScale)

# building the dashboard at the top
appDashValues = []
dashValuesDict = [
    {'title': f"24h vol. on {lastDaySplitTitle}", 'value':f'$ {format(sum(lastDaySplit), ",.0f")}','div':''},
    {'title': f"Monthly vol. on {curMonthSplitTitle}", 'value':f'$ {format(sum(curMonthSplit), ",.0f")}'},
    {'title': f"Monthly vol. on {lastMonthSplitTitle}", 'value': f'$ {format(sum(lastMonthSplit), ",.0f")}'},
    {'title': f"Cumulative vol. last 90 days", 'value': f'$ {format(sum(last90dSplit), ",.0f")}'},
    {'title': f"Cumulative vol. last 6 months", 'value': f'$ {format(sum(last6mo), ",.0f")}'},
    {'title': f"Cumulative vol. last year", 'value': f'$ {format(sum(lastyear), ",.0f")}'},]

ix = 0
for item in dashValuesDict:
    x = dbc.Col(dbc.Card(
        dbc.CardBody(
            html.Div([
                html.Div(item['title'], className='pb-1'),
                html.H3(item['value'], className="card-title")
            ]),
        ), className=cardStyle), className='col my-2')
    appDashValues.append(x)
    ix += 1
    if ix % 2 == 0:
        appDashValues.append(html.Div(className="w-100 d-xxl-none"))
    appDashValues.append(html.Div(className="w-100 d-sm-none"))


layout = [
    dbc.Container(
        [
            dbc.Row(
            html.H1(children='DCRDEX Statistics - dex.decred.org', style={'textAlign':'center'}),
                className="m-3"),
            dbc.Row(appDashValues, align="center", className="m-2"),
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Monthly Trading Volume", className="card-title"),
                            html.Div(dcc.Graph(figure=figMonthly), )
                        ]
                    ), className=cardStyle),
                align="center", className="m-2"
            ),
            dbc.Row([
                dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(lastMonthSplitTitle + " - Monthly Breakdown", className="card-title"),
                            html.Div(dcc.Graph(figure=figCurMonth), )
                        ]
                    ), className=cardStyle),),
                html.Div(className="w-100 d-md-none"),
                dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4(curMonthSplitTitle + " - Monthly Breakdown", className="card-title"),
                            html.Div(dcc.Graph(figure=figLastMonth), )
                        ]
                    ), className = cardStyle))
                ],
                align="center", className="m-2"
            ),
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Weekly Trading Volume", className="card-title"),
                            html.Div(dcc.Graph(figure=figWeekly), )
                        ]
                    ), className=cardStyle),
                align="center", className="m-2"
            ),
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Daily Trading Volume", className="card-title"),
                            html.Div(dcc.Graph(figure=figDaily), )
                        ]
                    ), className=cardStyle),
                align="center", className="m-2"
            ),
            dbc.Row(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("About", className="card-title"),
                            html.Div(['This dashboard is updated daily, with the 24 hour volume data collected via '
                                     '',html.A("dcrsnapcsv", href='https://github.com/bochinchero/dcrsnapcsv'),' and converted'
                                     ' to USD using the Coinmetrics daily reference price.'])
                        ]
                    ), className=cardStyle),
                align="center", className="m-2"
            ),
        ],
        fluid=True
    )
]