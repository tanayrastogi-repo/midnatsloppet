import plotly.express as px
import streamlit as st
import pandas as pd


if __name__ == "__main__":

    ## Visualization for my running data ##
    # Load GPS track
    tRun = pd.read_feather("data/Tanay_midnattslopper_run.feather")

    # Plot - Distance-vs-Elevation
    fig1 = px.area(tRun, x="dist", y="altitude")
    # Plot - Distance-vs-Pace
    fig2 = px.line(tRun, x="dist", y="pace")
    fig2.update_yaxes(range=[3, 30], autorange="reversed")

