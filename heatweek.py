import pandas as pd
import numpy as np
import datetime

import matplotlib.pyplot as plt

# Converts a datetime to minutes
def time_to_minutes(time):

    return time.hour * 60.0 + time.minute + time.second / 60.0


# Determines time-of-day index
def get_time_index(time, bin_width=15.0):

    minutes = time_to_minutes(time)
    return minutes / bin_width


# Filters dataframe of parsed entries 
# Keeps (or rejects) all rows with `colname` matching `keys` 
def filter_entries(entries, colname, keys, keep_keys=True):

    if keep_keys:
        indices = np.isin(entries[colname], keys)
        filtered = entries[indices]

    else:
        indices = np.isin(entries[colname], keys, invert=True)
        filtered = entries[indices]

    return filtered


# Add one time entry to the week (2D-) histogram
def add_entry_to_week(week, start, end, bin_width=15.0):

    # Find weekday index (Monday == 0, Tuesday == 1, etc.)
    day_index = start.weekday()

    # Find the time-of-day index for start time and end time
    # Days are broken into 15 min intervals (00:00-00:15 == 0, 00:15-00:30 == 1, etc.)
    start_index = get_time_index(start, bin_width)

    # Find time-of-day index for end time
    end_index = get_time_index(end, bin_width)

    # Increment histogram bins
    # "Full" bins are incremented by one
    # Weight is calculated for partial coverage in start and end bins

    # Need to be careful if time entry spans multiple days
    if start.date() != end.date():

        #!# Double yikes: if time entry spans multiple weeks
        #!# Safest approach is probably date-by-date approach
        print("Heck to working over midnight")  #!#

    # Special case for time entries within one time bin
    elif int(start_index) == int(end_index):

        weight = end_index - start_index
        week[int(start_index), day_index] += weight

    else:

        start_weight = int(start_index) + 1.0 - start_index
        week[int(start_index), day_index] += start_weight

        end_weight = end_index - int(end_index)
        week[int(start_index), day_index] += start_weight

        middle_indices = np.arange(int(start_index), int(end_index))[1:]

        for i in middle_indices:

            week[i, day_index] += 1.0

    return week


# Visualization of weekly activity
#!# Currently assumes time bins of 15 min
def plot_week(week, save_plot=False):

    fig, ax = plt.subplots(); 
    plt.imshow(week, aspect = 0.05)

    ax.set_xticks(np.arange(0,7,1))
    ax.set_xticklabels(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    ax.set_yticks(np.arange(-0.5, 92, 4))
    ax.set_yticklabels(["12 AM", "1 AM", "2 AM", "3 AM", "4 AM", "5 AM", "6 AM", "7 AM", "8 AM", 
                        "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM", 
                        "6 PM", "7 PM", "8 PM", "9 PM", "10 PM", "11 PM"])

    # Setting up grid along (invisible) minor ticks
    ax.set_xticks(np.arange(-0.5, 6, 1), minor=True)
    ax.set_yticks(np.arange(11.5, 95.5, 12), minor=True)
    ax.tick_params(which='minor', length=0)
    ax.grid(which='minor', color='w', linewidth=1)

    plt.tight_layout()

    if save_plot:
        fig.savefig(save_plot, figsize=(14,11))

    else:
        plt.show()

# Read in tables of Toggl time entries
entries_raw = pd.read_csv(
    "Toggl_time_entries_2020-01-01_to_2020-12-31.csv",
    parse_dates=[["Start date", "Start time"], ["End date", "End time"]],
)

entries_raw2 = pd.read_csv(
    "Toggl_time_entries_2019-01-01_to_2019-12-31.csv",
    parse_dates=[["Start date", "Start time"], ["End date", "End time"]],
)

# Combine data from both files into one dataframe
#!# Is there a better way to do this with read_csv()?
entries = entries_raw.append(entries_raw2)

#!# Could make resolution of final chart a user-defined variable?
#!# Would need to check that it divides well into 24 hours, and move to more granular underlying histogram
week = np.zeros((96, 7))

for index, row in entries.iterrows():

    #!# Could add condition based on Project, Tags, etc
    week = add_entry_to_week(
        week, row["Start date_Start time"], row["End date_End time"]
    )  #!# Ugly names

plot_week(week, save_plot='test_plot_0.png')


# Filtering dataframe based on project name
# Here I'm picking out all of my work-related projects 
# Other useful rows could be client or tags
keys = ["Department service / volunteering",
        "Meetings", "Online courses", "Other work",
        "Productivity", "Professional development",
        "Projects", "Research", "TAing", "Talks and seminars",
        "Thesis"]

work_entries = filter_entries(entries, "Project", keys)

work_week = np.zeros((96, 7))

for index, row in work_entries.iterrows():

    #!# Could add condition based on Project, Tags, etc
    work_week = add_entry_to_week(
        work_week, row["Start date_Start time"], row["End date_End time"]
    )  #!# Ugly names

plot_week(work_week, save_plot='test_plot_1.png')