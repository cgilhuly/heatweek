import pandas as pd
import numpy as np
import datetime

# Converts a datetime to minutes
def time_to_minutes( time ) :

    return time.hour * 60. + time.minute + time.second / 60.


# Determines time-of-day index
def get_time_index( time, bin_width = 15. ) : 

    minutes = time_to_minutes( time )
    return minutes / bin_width


# Add one time entry to the week (2D-) histogram
def add_entry_to_week( week, start, end, bin_width = 15. ) :
   
    # Find weekday index (Monday == 0, Tuesday == 1, etc.)
    day_index = start.weekday()

    # Find the time-of-day index for start time and end time
    # Days are broken into 15 min intervals (00:00-00:15 == 0, 00:15-00:30 == 1, etc.)
    start_index = get_time_index( start, bin_width )
    
    # Find time-of-day index for end time
    end_index = get_time_index( end, bin_width )
      
    # Increment histogram bins
    # "Full" bins are incremented by one
    # Weight is calculated for partial coverage in start and end bins
    
    # Need to be careful if time entry spans multiple days
    if start.date() != end.date():
    
        #!# Double yikes: if time entry spans multiple weeks
        #!# Safest approach is probably date-by-date approach
        print( "Heck to working over midnight" ) #!#

    # Special case for time entries within one time bin        
    elif int(start_index) == int(end_index):
    
        weight = end_index - start_index
        week[int(start_index), day_index] += weight
        
    else:
    
        start_weight = int(start_index) + 1. - start_index
        week[int(start_index), day_index] += start_weight
        
        end_weight = end_index - int(end_index)
        week[int(start_index), day_index] += start_weight  

        middle_indices = np.arange( int(start_index), int(end_index) )[1:]
        
        for i in middle_indices :
        
            week[i, day_index] += 1.
        
    return week
    
# Read in tables of time entries
entries_raw = pd.read_csv('Toggl_time_entries_2020-01-01_to_2020-12-31.csv',
                           parse_dates=[['Start date', 'Start time'], ['End date', 'End time']]
                          )

entries_raw2 = pd.read_csv('Toggl_time_entries_2019-01-01_to_2019-12-31.csv',
                           parse_dates=[['Start date', 'Start time'], ['End date', 'End time']]
                          )

# Combine data from both files into one dataframe
#!# Is there a better way to do this with read_csv()?
entries = entries_raw.append(entries_raw2)  

#!# Could make resolution of final chart a user-defined variable?
#!# Would need to check that it divides well into 24 hours, and move to more granular underlying histogram                        
week_bins = np.zeros((96,7))

for index, row in entries_raw.iterrows() :

    #!# Could add condition based on Project, Tags, etc
    week_bins = add_entry_to_week( week_bins, row['Start date_Start time'], row['End date_End time'] ) #!# Ugly names
    