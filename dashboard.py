import streamlit as st
from data_model import Race, SCB, age_vs_gender_pyramid, normalized
import page_text

def custom_css():
    """Load custom CSS for styling"""
    st.markdown(
        """
    <style>
    .page-header h1 {
        font-size: 70px;
        color: rgba(245, 245, 245, 1);
        text-align: center;
    }

    .page-header h2 {
        font-size: 40px;
        color: rgba(245, 245, 245, 1);
        text-align: center;
    }

    </style>
    """,
        unsafe_allow_html=True,
    )


def main():
    """ Main function for the streamlit dashboard.
    """
    custom_css ()

    #---------- Header ----------#
    st.image("data/midnattsloppet-logo.svg", 
             use_container_width=True)
    st.markdown("""
                <div class="page-header">
                    <h1>RACE ANALYSIS</h1>
                </div>
            """, unsafe_allow_html=True)

    # Introduction
    col1, col2 = st.columns(2)
    with col1:
        st.image("data/image1.jpg", use_container_width=False)
    with col2:
        st.image("data/image2.jpg", use_container_width=False)
    page_text.start()



    race = Race()
    scb = SCB()
    #---------- Data----------#  
    page_text.race_data()
    st.markdown("Race Data Statistics: ")
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.markdown(f"""
            * No. of participants: {race.data.shape[0]}
            * No. of participants who finihsed: {race.data[race.data['finished']].shape[0]}
        """)
    with col2:
        with st.container(border=True):
            st.markdown(f"""
            * Fastest 10km: {race.data.iloc[0]["time"].seconds / 60} min
            * Slowest 10km: {race.data["time"].max().seconds / 60} min
        """)
    st.markdown("The table below shows a small snippet of data: ")
    st.dataframe(race.data.head(5))

    page_text.scb_data()
    st.dataframe(scb.data.head(5))


    #---------- Participant Demographics----------#
    page_text.age_gender_pyramid()
    race_grp = race.get_age_gender_table()
    scb_grp  = scb.get_age_gender_table(age_grp=race_grp.index)
    fig = age_vs_gender_pyramid(scb_grp, normalized(scb_grp), race_grp, normalized(race_grp))

    col1, col2 = st.columns(2)
    with col1: 
        with st.container(border=True, horizontal_alignment="center", vertical_alignment="center"):
            st.markdown("**RACE:**")
            st.markdown(f"Male to Female ratio: {race.get_gender_ratio():0.3f}")
            st.markdown(f"Male: {race.data['gender'].value_counts()['M']} / Female: {race.data['gender'].value_counts()['F']} ")
    with col2: 
        with st.container(border=True):
            st.markdown("**SCB:** Male to Female ratio:")
            st.markdown(f"Male to Female ratio: {scb.get_gender_ratio():0.3f}")
            st.markdown(f"Male: {int(scb.data.sum()['men'])} / Female: {int(scb.data.sum()['women'])}")

    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Associated Data"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("## SCB Data")
            st.data_editor(scb_grp)
        with col2: 
            st.markdown("## Race Data")
            st.dataframe(race_grp)


    #---------- Finish Time Analysis----------#
    page_text.finish_time_1()
    fig, plot_data = race.plot_hist_times_gender()
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Associated Data"):
        st.markdown("## Mean Finish Time [minutes] based on Gender/Age ")
        df = plot_data.groupby(["age_grp", "gender"])["time"].mean().dt.total_seconds()/60
        df = df.reset_index()
        st.dataframe(df.pivot(index="age_grp", columns="gender", values="time"))

    # Class wise distribution
    # age_classes = race.data["age_grp"].unique()
    # # age_classes.sort()
    # # age_selection   = st.multiselect("Select AGE",    options=age_classes, default=age_classes)
    # # gender_classes = ["M", "F"]
    # # gender_selection= st.multiselect("Select GENDER", options=gender_classes, default=gender_classes)

    # # classes = [g+a for g in gender_selection for a in age_selection]
    # # fig, avg_times = race.plot_hist_times_class(classes)
    # # col1, col2 = st.columns([0.8, 0.2])
    # # with col1: 
    # #     st.plotly_chart(fig, use_container_width=True)
    # # with col2: 
    # #     st.dataframe(avg_times)

    st.dataframe(race.get_age_gender_finish_time())






if __name__ == "__main__":
    main()

