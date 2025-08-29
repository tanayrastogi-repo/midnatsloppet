from gpx_converter import Converter
import math


GPX_FILE_PATH    = 'data/Tanay.gpx'
EDITED_FILE_PATH = 'data/Tanay_midnattslopper_run.feather'


def haversine(coord1: tuple, coord2: tuple) -> float:
    """Function to calculate distance between two (lat, lon)

    Args:
        coord1 (tuple): (lat, lon) for the first  location as (float, float)
        coord2 (tuple): (lat, lon) for the second location as (float, float)

    Returns:
        float: The distance between the points in kms.
    """
    # Coordinates in decimal degrees (e.g., 59.3293, 18.0686)
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    # Earth radius in kilometers
    R = 6371.0
    # Convert degrees to radians
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in kilometers


# ----------- LOAD FILE ----------- #
print(f"Editing GPX {GPX_FILE_PATH}")
track = Converter(input_file=GPX_FILE_PATH).gpx_to_dataframe()

# ----------- TIME EDITS ----------- #
print("Time Edits, ", end= " ")
track["time"] = track.time.apply(lambda x: x.tz_convert('Europe/Stockholm'))
# Add time elapsed from the start
base_time = track.iloc[0].time
track["time_elp_sec"] = track["time"].apply(lambda x: (x - base_time))

# ----------- ADDING DISTANCE INFO ----------- #
print("Distance Edits, ", end= " ")
# Temporary lat lon values
track[["temp_lat", "temp_long"]] = track[["latitude", "longitude"]].shift(1)
# Distance between two nearby points
track["temp_dist"] = track.iloc[1:].apply(lambda x: haversine((x["latitude"], x["longitude"]), (x["temp_lat"], x["temp_long"])), axis=1)
# Cummulative distance
track["dist"] = track["temp_dist"].rolling(len(track), min_periods=1).sum()
# Just replace the NaN at first row to 0
track.fillna({"dist": 0.0}, inplace=True)

# ----------- ADDING PACE INFO ----------- #
print("Pace Edits, ", end= " ")
# Calculating spot pace
track["temp_time"] = (track["time"] - track["time"].shift(1))
track["temp_time"] = track["temp_time"].apply(lambda x: x.seconds/60)
track["pace"] = track["temp_time"] / track["temp_dist"] # min/km
track.fillna({"pace": 0.0}, inplace=True)

# Cummulative average pace
track["avg_pace"] = (track["time_elp_sec"].apply(lambda x: x.seconds) / 60) / track["dist"]
track.fillna({"avg_pace": 0.0}, inplace=True)

# # ----------- FINALIZING ----------- #
print("Saving to drive, ", end= " ")
# Drop irrelavant columns
track.drop(columns=["temp_lat", "temp_long", "temp_dist", "temp_time"], inplace=True)
# Save updated data to drive
track.to_feather(EDITED_FILE_PATH)
print("Done!")
print(f"\n File save to {EDITED_FILE_PATH}")