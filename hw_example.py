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


# Adding filtering by date on top of filtering by project name
# Here I'm looking at the "before times" and the "after times"
# In Ontario, a state of emergency was declared on March 17th, 2020
#!# Have not checked the behaviour of only specifying date and not time
#!# (Probably defaults to 00:00:00?)
before_entries = hw.filter_entries_bydate(work_entries, end_date="16-03-2020 23:59:59")
after_entries = hw.filter_entries_bydate(work_entries, start_date="17-03-2020 00:00:00")

before_week = np.zeros((96, 7))
after_week = np.zeros((96, 7))

for index, row in before_entries.iterrows():

    before_week = hw.add_entry_to_week(
        before_week, row["Start date_Start time"], row["End date_End time"]
    )  #!# Ugly names

for index, row in after_entries.iterrows():

    after_week = hw.add_entry_to_week(
        after_week, row["Start date_Start time"], row["End date_End time"]
    )  #!# Ugly names

hw.plot_week(before_week, save_plot="test_plot_2_before.png")
hw.plot_week(after_week, save_plot="test_plot_2_after.png")
