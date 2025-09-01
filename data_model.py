import pandas as pd
import re
from datetime import timedelta
import plotly.graph_objects as go

class Race: 
    def __init__(self, datasetPath="data/midnattsloppet_result_Stockholm_2025_Individual_10k.feather"):

        # Loading dataset
        self.data = pd.read_feather(datasetPath)
        #----- EDITS TO DATA -----#
        self.add_age_gender()
        self.format_time()

    def add_age_gender(self, ):
        self.data["age_grp"] = self.data['class'].apply(lambda x: re.split(r'(?<=[A-Za-z])', x)[1])
        self.data["gender"] = self.data['class'].apply(lambda x: re.split(r'(?<=[A-Za-z])', x)[0])

    def format_time(self, ):
        def mmss_to_timedelta(s: str) -> timedelta:
            return timedelta(minutes=int(s.split(':')[0]), seconds=int(s.split(':')[1]))
        self.data["time"] = self.data["time"].apply(lambda x: mmss_to_timedelta(x))


    def get_age_gender_table(self):
        race_group = self.data.groupby(["age_grp", "gender"])["name"].count().reset_index().pivot(index="age_grp" ,columns="gender", values='name')
        return race_group










class SCB:
    def __init__(self, datasetPath="data/MeanPop_by_year_Stockholm_age_sex.csv"):
        # Loading dataset
        self.data = pd.read_csv(datasetPath, sep=";")
        #----- EDITS TO DATA -----#
        self.age_to_int()

    def age_to_int(self, ):
        # SCB: Convert age to int type
        self.data.replace({"age": '100+'}, 100, inplace=True)
        self.data['age'] = self.data['age'].astype(int)


    def get_age_gender_table(self, age_grp):
        # Temp variable
        scb_group = pd.DataFrame(index=age_grp, columns=['F', 'M'])
        def get_pop_sum(range):
            if int(range[0]) == 75:
                return self.data[(self.data['age'] >=int(75)) & (self.data['age'] <=int(80))][["men", "women"]].sum()
            else:
                return self.data[(self.data['age'] >=int(range[0])) & (self.data['age'] <=int(range[1]))][["men", "women"]].sum()
        # AGE-VS-GENDER Table
        scb_group = scb_group.apply(lambda x: get_pop_sum(x.name.split('-')), axis=1)
        return scb_group







def normalized(df):
    df_copy = df.copy()
    for col in df.columns: 
        df_copy[col] = (df_copy[col] - df_copy[col].min())/(df_copy[col].max() - df_copy[col].min())
    return df_copy



#--------------------------- PLOT FUNCTIONS ---------------------------#
def age_vs_gender_pyramid(scb_grp, scb_nrl, race_grp, race_nrl):
    # AGE-VS-GENDER Pyramid PLOT
    layout = go.Layout(yaxis=go.layout.YAxis(title='Age'),
                    xaxis=go.layout.XAxis(
                        range=[-1, 1],
                        tickvals=[-1, -0.7, -0.3, 0, 0.3, 0.7, 1],
                        ticktext=[1, 0.7, 0.3, 0, 0.3, 0.7, 1],
                        title='Normlized Values'),
                    barmode='overlay',
                    bargap=0.1)
    # Age
    y = list(range(0, 100, 10))

    # Counts bins
    data = [go.Bar(y=y,
                x=scb_nrl["men"],
                orientation='h',
                name='Men',
                text=scb_grp["men"].astype('int'),
                textposition = "none",
                hoverinfo='text',
                marker=dict(color='powderblue')
                ),
            go.Bar(y=y,
                x=-scb_nrl["women"],
                orientation='h',
                name='Women',
                text=scb_grp["women"].astype('int'),
                textposition = "none",
                hoverinfo='text',
                marker=dict(color='seagreen')
                ),
            go.Bar(y=y,
                x=race_nrl["M"],
                orientation='h',
                text=race_grp["M"].astype('int'),
                textposition = "none",
                hoverinfo='text',
                showlegend=False,
                opacity=0.5,
                marker=dict(color='teal')
                ),
            go.Bar(y=y,
                x=-race_nrl["F"],
                orientation='h',
                text=race_grp["F"].astype('int'),
                textposition = "none",
                hoverinfo='text',
                showlegend=False,
                opacity=0.5,
                marker=dict(color='darkgreen')
                )]
    return go.Figure(layout=layout, data=data)


if __name__ == "__main__":
    model = Race()
