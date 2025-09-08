import streamlit as st

def start():
    return st.markdown("""
Another Saturday night, another neon run—**Midnattsloppet Stockholm 10K** done and dusted!  
Second year in a row, and this time I cracked the sub‑60 barrier with an official **59:38**.  
It’s definitely an improvement from last year’s run, and seeing that finish clock start with a 5 felt ridiculously good.

For someone who does not know what is Midnattsloppet: 

> It's 10K is a late‑night run around Södermalm with thousands of
> runners, samba beats, and a street‑festival vibe. Check out this page for more info: [Midnattsloppet 2025](https://midnattsloppet.com/midnattsloppet-stockholm)

---

### Post-Race Thoughts

After shaking off the race buzz, there are some questions popped into my head.
This blog is mostly to scratch that curiosity using factual "DATA". Mostly, I am trying to answer: 

---
1. **How many people are actually running this race?**

Globally, fewer than **1–2% of adults** can run 10 km continuously!  
Source: [YouTube – Are You Part of the 1 Percent Who Can Run 10KM?](https://www.youtube.com/shorts/bkW1jkhGXvk)  
As always, social media stats need salt, but at least I can look at the local turnout for Stockholm.

---

2. **Where do I stand among all the racers?**

This bit is just me figuring where I land compared to the average runner here.  
I’m not super sporty, but it’s fun to see how I stack up.

---



""", unsafe_allow_html=True)


def race_data():
    return st.markdown("""
# Data
The data for this analysis is coming from directly from their result website - [Midnattsloppet 2025 Result](https://results.midnattsloppet.com/stockholm/?q). I scraped all the data from the results table into a parquet file, that is then used for analysis and visualization. 
From the race-results table tells me that around ~30k people ran the race. Middnastsloppet divides these people in 3 genders and 14 age groups - derived from the "class" definition in the results table.
Also, arounf 85% of the total participants actually finihsed the race and have registed a final place in the leaderboard.
    """, unsafe_allow_html=True)

def scb_data():
    return st.markdown("""
Some of the socio-demographic on distribution on age, gender for year 2025 is retrieved from SCB website as a CSV. Its a open-source data platform to collect aggregates about Swedish population - [Mean population (by year of birth) by region, age and sex. Year 2006 - 2024](https://www.statistikdatabasen.scb.se/pxweb/en/ssd/START__BE__BE0101__BE0101D/MedelfolkFodelsear/).

The table below shows a snippet of 2025 distribution for Stockholm County:
    """, unsafe_allow_html=True)







def age_gender_pyramid():
    return st.markdown("""
# Participants Demographics
So, first things fisrt, I want to know who is running the Middnastsloppet 10KM \n. 

For this analysis, I used the Results and SCB data to see the AGE-vs-GENDER distribution for Stockholm city.
The chart below shows the normalized AGE-VS-GENDER distribution for both SCB and Race dataset.

Surprizingly the race participation follows very closely with the Stockholm population. Also, the male-to-female ratio is also quite similar, however, it is bit skewed towards men in actual race participation.
Also, most people running in the race are in age group between 23-34, very similar to the Stockholm population.

From the data, the average person running the race is: **MALE** in age group of **23-34**.

    Caveat:
        * I specifically remove the gender labelled as "U" because there is no way for me to analysize against SCB dataset that only have two gender labels.  
        * The race is not only restricted to Stockholmer and people from all around the world have participated in this.
            
    """, unsafe_allow_html=True)



def finish_time_1():
    return st.markdown("""
# Finish Time Distribution
Now focusing just on the finish time for the participants.
For all the 25781 participants that finished the race, the average finish time for men is smaller than female.
The men (at an average) are 8.3 min faster than women in this race.

    """, unsafe_allow_html=True)

def finish_time_2():
    return st.markdown("""
Even when we analyze this data divided across age and gender, in all cases the men are faster than women, except for age group 70-74 where females are faster.

    Caveat:
        * This analysis is only for the participants that finihsed the race and have a place.
        * I ignored the "U" section, as there is too less data under this label.

    """, unsafe_allow_html=True)