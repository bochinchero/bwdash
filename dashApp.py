from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import datetime

data = pd.read_csv('https://raw.githubusercontent.com/bochinchero/dcrsnapcsv/main/data/stream/dex_decred_org_VolUSD.csv')
data['date'] = pd.to_datetime(data['date'], utc=True, format='%Y-%m-%d')
data = data.set_index('date')

# prepare daily data
dailyData = data[-90:]
dailyData = dailyData.loc[(dailyData.sum(axis=1) != 0), (dailyData.sum(axis=0) != 0)]
dailyData = dailyData[dailyData.sum().sort_values(ascending=False).index]
dailyDataLen = len(list(dailyData.columns.values))
colorsDaily = px.colors.sample_colorscale("deep_r", [n/(dailyDataLen+1) for n in range(dailyDataLen)])

# prepare monthly data
monthlyData = data.groupby(pd.Grouper(freq='MS')).sum()
monthlyData = monthlyData[-12:]
monthlyData = monthlyData.loc[(monthlyData.sum(axis=1) != 0), (monthlyData.sum(axis=0) != 0)]
monthlyData = monthlyData[monthlyData.sum().sort_values(ascending=False).index]
monthlyDataLen = len(list(monthlyData.columns.values))
colorsMonthly = px.colors.sample_colorscale("deep_r", [n/(monthlyDataLen+1) for n in range(monthlyDataLen)])


app = Dash()

figDaily = px.bar(dailyData, x=dailyData.index, y=list(dailyData.columns.values), title="Daily Volume",
                            color_discrete_sequence=colorsDaily, height=500)

figDaily.update_layout(
    xaxis=dict(
        rangeselector=dict(
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
                     stepmode="todate")
            ])
        ),
        type="date"
    )
)
figDaily.update_xaxes(title_text='Date')
figDaily.update_yaxes(title_text='Daily Volume')

figMonthly = px.bar(monthlyData, x=monthlyData.index, y=list(monthlyData.columns.values), title="Monthly Volume",
                    color_discrete_sequence=colorsMonthly, height=500)
figMonthly.update_layout(
    xaxis=dict(
        type="date"
    )
)
figMonthly.update_xaxes(title_text='Date')
figMonthly.update_yaxes(title_text='Monthly Volume')

app.layout = [
    html.H1(children='Trading Volume - dex.decred.org', style={'textAlign':'center'}),
    dcc.Graph(figure=figDaily),
    dcc.Graph(figure=figMonthly)
]


if __name__ == '__main__':
    app.run(debug=True)