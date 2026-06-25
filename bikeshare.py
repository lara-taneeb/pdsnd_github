import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("Please enter the city (Chicago/New York City/Washington)")
    response = input()
    response = response.rstrip().lower()
    while((response not in CITY_DATA)):    
        print("please re-enter the city: ")
        response = input()
        response = response.rstrip().lower()

    city = response

    # TO DO: get user input for month (all, january, february, ... , june)
    print("Please enter the month (From January to June)")
    months = {"january", "february", "march", "april", "may", "june"}
    response = input()
    response = response.rstrip().lower()
    
    month = ""

    while((response not in months) and (response != "all")):
        print("please re-enter the month: ")
        response = input()
        response = response.rstrip().lower()
        
    month = response


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    print("Please enter the day of the week")
    dayofweek = {"monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}

    response = input()
    response = response.rstrip().lower()
    
    day = ""

    while((response not in dayofweek) and (response != "all")):
        print("please re-enter the dayofweek: ")
        response = input()
        response = response.rstrip().lower()
        
    day = response

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # TO DO: display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print("The most popular month to travel is: {0}".format(popular_month))

    # TO DO: display the most common day of week
    df['dayofweek'] = df['Start Time'].dt.dayofweek
    popular_dayofweek = df['dayofweek'].mode()[0]
    print("The most popular day of the week to travel is: {0}".format(popular_dayofweek))
    
    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("The most popular start hour to travel is: {0}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common starting station is: {0}".format(common_start_station))
    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common ending station is: {0}".format(common_end_station))


    # TO DO: display most frequent combination of start station and end station trip
    df['combined'] = df['Start Station'] + " to " + df['End Station']
    common_start_end_route = df['combined'].mode()[0]
    print("The most common route is from {0}".format(common_start_end_route))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def seconds_to_str(seconds):
    """Print seconds into a human-readable format"""
    days, remainder = divmod(seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    retstr = ""
    if(days != 0):
        retstr += str(days) + " days, "
    if(hours != 0):
        retstr += str(hours) + " hours, "
    if(minutes != 0):
        retstr += str(minutes) + " minutes "
    if(seconds != 0):
        retstr += str(seconds) + " seconds."
    
    return retstr
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    
    print("The total travel time is: {0}".format( seconds_to_str(total_travel_time.astype(int)) ))
    
    
    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("The mean travel time is: {0}".format(seconds_to_str(mean_travel_time.astype(int))))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def value_counts_to_str(val_cnt):
    """Print value counts in a more human-readable format"""
    retstr = "There are: \n"
    for value, count in val_cnt.items():
        if(count == 1):
            retstr += "    " + str(count) + " " + value + "\n"
        else:
            retstr += "    " + str(count) + " " + value + "s \n"
    
    return retstr
    
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts() # returns series.Series
    print(value_counts_to_str(user_types))
    
    # TO DO: Display counts of gender
    if(city == "chicago" or city == "new york city"):
        gender = df['Gender'].value_counts()
        print(value_counts_to_str(gender))


    # TO DO: Display earliest, most recent, and most common year of birth
    
    if(city == "chicago" or city == "new york city"):
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
    
        print("The earliest birth year is: {0}".format(earliest.astype(int)))
        print("The most recent birth year is: {0}".format(most_recent.astype(int)))
        print("The most common birth year is: {0}".format(most_common.astype(int)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    start_loc = 0
    
    
    response = input("Would you like to see the first 5 rows of data?\n")
    response = response.lower().rstrip()
    while True:
        if response.lower() != 'yes':
            break
        
        print(df.iloc[start_loc : start_loc + 5])
        start_loc += 5
        
        response = input("Would you like to see the next 5 rows of data?\n")
        response = response.lower().rstrip()
        
        
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
