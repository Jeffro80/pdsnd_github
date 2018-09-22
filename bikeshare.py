import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def check_raw_data():
    """Check if user wishes to display raw data.
    
    Returns:
        (bool) - True if wish to review raw data, False otherwise.
    """
    while True:
        show_data = input('\nDo you wish to view the raw data? yes or no: ')
        if show_data.lower() == 'yes':
            return True
        elif show_data.lower() == 'no':
            return False
        else:
            print('\nThat is not a valid response! Please enter either \'yes\''
                  ' or \'no\'')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington).
    while True:
        print('\nWhich city would you like to filter the data by? Your options'
              ' are:')
        print('\nChicago, New York City, Washington.')
        city = input('\nPlease enter city to filter by: ').lower()
        if city in ('chicago', 'new york city', 'washington'):
            break
        else:
            print('\nThat is not a valid city! Please enter from the available'
                  ' cites.')
        
    # get user input for month (all, january, february, ... , june)
    while True:
        print('\nWhich month would you like to filter the data by? Your '
              ' options are:')
        print('\nJan, Feb, Mar, Apr, May, Jun, or All to use all months.')
        month = input('\nPlease enter month to filter by: ').lower()
        if month in ('jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all'):
            break
        else:
            print('\nThat is not a valid month! Please enter from the '
                  ' available months.')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']
        allowed_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        print('\nWhich day would you like to filter the data by? Your '
              ' options are:')
        print('\nMon, Tue, Wed, Thu, Fri, Sat, Sun, or All to use all days.')
        raw_day = input('\nPlease enter day to filter by: ').lower()
        if raw_day == 'all':
            day = 'all'
            break
        elif raw_day in allowed_days:
            # Get full name from days list
            day = days[allowed_days.index(raw_day)]
            break
        else:
            print('\nThat is not a valid day! Please enter from the '
                  ' available days.')

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Load data for the specified city and filter by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" for no filter
        (str) day - name of day of week to filter by, or "all" for no filter
    
    Returns:
        (DataFrame) df - City data filtered by month and day.
    """
    # load desired city
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] =  pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def main():
    while True:
        # Get data for desired city and desired filters
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        # Perform analysis on data using filters
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        # Check if want to see raw data and display
        raw_data(city)

        # Check if run analysis again
        restart = input('\nWould you like to restart? Enter yes or no. \n')
        if restart.lower() != 'yes':
            print('\nGoodbye!')
            break


def raw_data(city):
    """Display raw data if requested by user."""
    # Load the raw data
    data = pd.read_csv(CITY_DATA[city])
    # counter for returning correct rows from data
    n = 0
    while True:
        if check_raw_data():
            # Getting a list of column names taken from:
            # https://stackoverflow.com/a/19483025/4340630
            column_names = list(data)
            print('\nRaw data:\n')
            for i in range (5):
                row = data.iloc[n]
                c = 0 # for aligning column names to data
                for item in row:
                    print('{}: {}'.format(column_names[c], item))
                    c += 1
                print('\n')
                n += 1
        else:
            return
        

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_start = df['Start Station'].mode()[0]
    # Count of specific value in column from:
    # https://stackoverflow.com/a/20076611/4340630
    count_most_start = df['Start Station'].value_counts()[most_start]
    print('Most common starting station: {}, Count: {}'.format(most_start,
          count_most_start))
    
    # display most commonly used end station
    most_end = df['End Station'].mode()[0]
    count_most_end = df['End Station'].value_counts()[most_end]
    print('Most common ending station: {}, Count: {}'.format(most_end,
          count_most_end))
    
    # display most frequent combination of start station and end station trip
    # Combine start and end columns
    df['Combined Stations'] = df['Start Station'] + ' and ' + df['End Station']
    most_combined =  df['Combined Stations'].mode()[0]
    count_most_combined = df['Combined Stations'].value_counts()[most_combined]
    print('Most common station combination: {}, Count: {}'.format(
            most_combined, count_most_combined))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # List of months for displaying output
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    # display the most common month
    most_common_month = months[df['month'].mode()[0]-1]
    count_most_common_month = df['month'].value_counts()[df['month'].mode()[0]]
    print('Most common month: {}, Count: {}'.format(most_common_month,
          count_most_common_month))
    
    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    # count_most_common_day = df['day_of_week'].values_count()[most_common_day]
    print('Most common day of week: {}'.format(most_common_day))
    
    # display the most common start hour
    # Convert Start Time to an hour
    df['Start Hour'] = df['Start Time'].dt.hour
    most_common_start_hour = df['Start Hour'].mode()[0]
    print('Most common start hour: {}'.format(most_common_start_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total trip duration: {}'.format(df['Trip Duration'].sum()))
    
    # display mean travel time
    print('Mean travel time: {}'.format(df['Trip Duration'].mean()))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print('Number of each user type:\n')
    for user, count in user_counts.iteritems():
        print('{}: {}'.format(user, count))
        
    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
    except KeyError:
        print('\nGender data not available')
    else:
        print('\nNumber of each gender:\n')
        for gender, count in gender_counts.iteritems():
            print('{}: {}'.format(gender, count))

    # Display earliest, most recent, and most common year of birth 
    try:
        earliest_birth_year = df['Birth Year'].min()
    except KeyError:
        print('\nBirth year data not available')
    else:
        print('\nEarliest birth year: {}'.format(int(earliest_birth_year)))
        print('Most recent birth year: {}'.format(int(df['Birth Year'].max())))
        print('Most common birth year: {}'.format(int(
                df['Birth Year'].mode()[0])))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


if __name__ == "__main__":
	main()
