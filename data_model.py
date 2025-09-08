import pandas as pd
import re
from datetime import timedelta
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

class Race:
    def __init__(self, datasetPath="data/midnattsloppet_result_Stockholm_2025_Individual_10k.feather"):

        # Loading dataset
        self.data = pd.read_feather(datasetPath)
        #----- EDITS TO DATA -----#
        self.add_age_gender()
        self.format_time()
        self.add_finish_status()

    def add_age_gender(self, ):
        self.data["age_grp"] = self.data['class'].apply(lambda x: re.split(r'(?<=[A-Za-z])', x)[1])
        self.data["gender"] = self.data['class'].apply(lambda x: re.split(r'(?<=[A-Za-z])', x)[0])
        # Convert the age group 1-15 to 13-15
        idx = self.data[self.data["age_grp"] == "1-15"].index
        self.data.loc[idx, "age_grp"] = "13-15"

    def format_time(self, ):
        def mmss_to_timedelta(s: str) -> timedelta:
            splt = s.split(":")
            if len(splt) == 2:
                return timedelta(minutes=int(splt[0]), seconds=int(splt[1]))
            elif len(splt) == 3:
                return timedelta(hours=int(splt[0]), minutes=int(splt[1]), seconds=int(splt[2]))
            else:
                raise ValueError('Wrong format of time')

        self.data["time"] = self.data["time"].apply(lambda x: mmss_to_timedelta(x))
        # Time to minutes
        self.data["time_min"] = self.data["time"].dt.total_seconds() / 60.0

    def add_finish_status(self, ):
        self.data["finished"] = True
        # False at places that did not finish
        idx = self.data[self.data["place"] == ""].index
        self.data.loc[idx, "finished"] = False

    def get_age_gender_table(self):
        race_group = self.data.groupby(["age_grp", "gender"])["name"].count().reset_index().pivot(index="age_grp" ,columns="gender", values='name')
        return race_group

    def get_age_gender_finish_time(self, ):
        # Drop the "U" gender categories
        df = self.data.drop(self.data[self.data["gender"] == "U"].index)
        table = df.groupby(["age_grp", "gender"])["time_min"].mean().reset_index().pivot(index="age_grp" ,columns="gender", values='time_min')
        table["delta[F-M]"] = table["F"] - table["M"]
        return table

    def get_gender_ratio(self, ):
            gender_counts = self.data['gender'].value_counts()
            male_count = gender_counts.get('M', 0)
            female_count = gender_counts.get('F', 0)

            if female_count > 0:
                return male_count / female_count
            else:
                raise ValueError("No female participants found")


    def plot_hist_times_gender(self, ):
        # Preparing for plotting
        plot_data = self.data.copy()
        # Drop the participants that did not finish the race
        plot_data = plot_data[plot_data["finished"]]
        # Drop the "U" gender categories
        plot_data = plot_data.drop(plot_data[plot_data["gender"] == "U"].index)
 
        hist_data = [plot_data[plot_data["gender"] == "F"]["time_min"],
                    plot_data[plot_data["gender"] == "M"]["time_min"]]
        group_labels = ['Female', 'Male']
        colors=['#FF0000', '#008000']
        fig = ff.create_distplot(hist_data, group_labels, bin_size=1,
                                 curve_type='normal',
                                 show_hist=True, show_rug=False, colors=colors)

        for gender in ['M', 'F']:
            gender_data = plot_data[plot_data['gender'] == gender]
            median_time = gender_data['time_min'].median()

            # Add vertical line for median
            fig.add_vline(
                x=median_time,
                line_dash="dash",
                line_color="black",
                annotation_text=f"{median_time:.1f}",
                annotation_position="top",
                col=1 if gender == 'M' else 2  # Specify which column (facet)
            )
        fig.update_xaxes(title="Finish time (min)")
        fig.update_yaxes(title="Normal Distribution")
        return fig, plot_data

    def plot_hist_times_class(self, classes: list):
        # Preparing for plotting
        plot_data = self.data.copy()
        # Drop the participants that did not finish the race
        plot_data = plot_data[plot_data["finished"]]

        hist_data, mean_time, group_label = list(), list(), list()
        for cl in classes:
            data = plot_data[plot_data["class"] == cl]["time_min"]
            if len(data) > 0: 
                mean_time.append(data.mean())
                hist_data.append(data)
                group_label.append(cl)

        fig = ff.create_distplot(hist_data, group_label, bin_size=1,
                                 curve_type='normal',
                                 show_hist=True, show_rug=False)
        mean_time = pd.DataFrame(mean_time, index=group_label, columns=["time_min"]).sort_values(by="time_min")
        return fig, mean_time



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

    def get_gender_ratio(self, ):
            gender_counts = self.data.sum()
            male_count = gender_counts.get('men')
            female_count = gender_counts.get('women')

            if female_count > 0:
                return male_count / female_count
            else:
                raise ValueError("No female participants found")





def normalized(df):
    df_copy = df.copy()
    # for col in df.columns:
    #     df_copy[col] = (df_copy[col] - df_copy[col].min())/(df_copy[col].max() - df_copy[col].min())
    df_sum = sum(df.sum())
    df_copy /= df_sum
    return df_copy



#--------------------------- PLOT FUNCTIONS ---------------------------#
def age_vs_gender_pyramid(scb_grp, scb_nrl, race_grp, race_nrl):
    # AGE-VS-GENDER Pyramid PLOT
    layout = go.Layout(
                    yaxis=go.layout.YAxis(
                        tickvals=list(range(scb_nrl.shape[0])),
                        ticktext=scb_nrl.index.to_list(),
                        title='Age'),
                    xaxis=go.layout.XAxis(
                        range=[-0.3, 0.3],
                        tickvals=[-0.25, -0.2, -0.15, -0.1, -0.05, 0, 0.05, 0.1, 0.15, 0.2, 0.25],
                        ticktext=[0.25, 0.2, 0.15, 0.1, 0.05, 0, 0.05, 0.1, 0.15, 0.2, 0.25],
                        title='Normlized Values'),
                    barmode='overlay',
                    bargap=0.15)
    # Counts bins
    data = [go.Bar(
                x=scb_nrl["men"],
                orientation='h',
                name='Men',
                marker=dict(color='green'), 
                legendgroup="scb",
                legendgrouptitle_text="SCB",
                opacity=0.5,
                ),
            go.Bar(
                x=-scb_nrl["women"],
                orientation='h',
                name='Women',
                marker=dict(color='red'),
                legendgroup="scb",
                opacity=0.5,
                ),
            go.Bar(
                x=race_nrl["M"],
                orientation='h',
                name="M",
                marker=dict(color='green'),
                legendgroup="race",
                legendgrouptitle_text="RACE",
                opacity=0.5,
                ),
            go.Bar(
                x=-race_nrl["F"],
                orientation='h',
                name="F",
                marker=dict(color='red'),
                legendgroup="race",
                opacity=0.5,
                )]
    return go.Figure(layout=layout, data=data)


if __name__ == "__main__":
    model = Race()
