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



    #---------- Participant Data Analysis----------#
    race = Race()
    scb = SCB()

    st.markdown("""
             <div class="page-header">
                <h2>Participant Demographics</h2>
            </div>
        """, unsafe_allow_html=True)



    #---------- Participant Demographics----------#
    # AGE and GENDER based participation
    race_grp = race.get_age_gender_table()
    scb_grp  = scb.get_age_gender_table(age_grp=race_grp.index)
    fig = age_vs_gender_pyramid(scb_grp, normalized(scb_grp), race_grp, normalized(race_grp))
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Associated Data"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("## SCB Data")
            st.data_editor(scb_grp)
        with col2: 
            st.markdown("## Race Data")
            st.dataframe(race_grp)

    # MEAN Finish time based on class-gender
    fig, plot_data = race.plot_hist_times_gender_class()
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Associated Data"):
        st.markdown("## Mean Finish Time [minutes] based on Gender/Age ")
        df = plot_data.groupby(["age_grp", "gender"])["time"].mean().dt.total_seconds()/60
        df = df.reset_index()
        st.dataframe(df.pivot(index="age_grp", columns="gender", values="time"))












if __name__ == "__main__":
    main()

