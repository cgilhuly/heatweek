import heatweek as hw
import numpy as np

# Read time entries exported from Toggl into a dataframe
entries = hw.read_CSVs(["Toggl_entries_2020.csv", "Toggl_entries_2019.csv"])

#!# Could make resolution of final chart a user-defined variable?
#!# Would need to check that it divides well into 24 hours, and move to more granular underlying histogram
week = np.zeros((96, 7))

for index, row in entries.iterrows():

    week = hw.add_entry_to_week(
        week, row["Start date_Start time"], row["End date_End time"]
    )  #!# Ugly names

hw.plot_week(week, save_plot="test_plot_0.png")


# Filtering dataframe based on project name
# Here I'm picking out all of my work-related projects
# Other useful rows could be client or tags
keys = [
    "Department service / volunteering",
    "Meetings",
    "Online courses",
    "Other work",
    "Productivity",
    "Professional development",
    "Projects",
    "Research",
    "TAing",
    "Talks and seminars",
    "Thesis",
]

work_entries = hw.filter_entries(entries, "Project", keys)

work_week = np.zeros((96, 7))

for index, row in work_entries.iterrows():

    #!# Could add condition based on Project, Tags, etc
    work_week = hw.add_entry_to_week(
        work_week, row["Start date_Start time"], row["End date_End time"]
    )  #!# Ugly names

hw.plot_week(work_week, save_plot="test_plot_1.png")