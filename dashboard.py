import streamlit as st
from data_model import Race, SCB, age_vs_gender_pyramid, normalized

def custom_css():
    """Load custom CSS for styling"""
    st.markdown(
        """
    <style>
    .page-header h1 {
        font-size: 80px;
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
             use_container_width=True, caption="Midnattslopper-official-logo")
    st.markdown("""
                <div class="page-header">
                    <h1>RACE ANALYSIS</h1>
                </div>
            """, unsafe_allow_html=True)

    #---------- Participant Data Analysis----------#
    race = Race()
    scb = SCB()

    # Get tables
    race_grp = race.get_age_gender_table()
    race_nrl = normalized(race_grp)
    scb_grp  = scb.get_age_gender_table(age_grp=race_grp.index)
    scb_nrl = normalized(scb_grp)




    #---------- Participant Demographics----------#
    # AGE and GENDER based participation
    fig = age_vs_gender_pyramid(scb_grp, scb_nrl, race_grp, race_nrl)
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("Associated Data"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("## SCB Data")
            st.data_editor(scb_grp)
        with col2: 
            st.markdown("## Race Data")
            st.data_editor(race_grp)

    # MEAN Finish time based on class-gender
    fig = race.plot_hist_times_gender_class()
    st.plotly_chart(fig, use_container_width=True)













if __name__ == "__main__":
    main()

