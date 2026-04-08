import time
import pandas as pd
import numpy as np

USECOLS = [
    'Start Time',
    'Trip Duration',
    'Start Station',
    'End Station',
    'User Type',
    'Gender',
    'Birth Year'
]

DTYPES = {
    'Trip Duration': 'int32',
    'User Type': 'category',
    'Gender': 'category',
    'Start Station': 'category',
    'End Station': 'category'
}

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
    # Prompt the user to select a city (chicago, new york city, washington)
    cities = ['chicago', 'new york city','washington']
    while True:
        city = input("Please select a city: Chicago, New York City, or Washington:").strip().lower()
        if city in cities:
           break
        else:
            print("Invalid input. Please enter one of the selected cities.")

    # Prompt the user input for month (all, january, february, ... , june)
    months = ['january','february','march','april','june','all']
    while True:
        month = input("Choose a month (January-June) or 'all':").lower()
        if month in months:
            break
        else:
            print("Invalid month input. Please enter a valid month name or 'all'.")

    # Prompt the user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']
    while True:
        day = input("Choose a day of the week or 'all':").lower()
        if day in days:
            break
        else:
            print("Invalid day input. Please enter a valid day or 'all'.")

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

    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # Extract month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    
    # Filter by month if applicable
    if month != 'all':
        month_index = [
            'january', 'february', 'march',
            'april', 'may', 'june'
        ].index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day if applicable    
    if day != 'all':
        df = df[df['day_of_week'] == day]

    
 # Memory usage (in MB)
    memory_mb = df.memory_usage(deep=True).sum() / 1_048_576
    print(f"DataFrame memory usage: {memory_mb:.2f} MB")


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Determine the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is:", common_month)

    # Determine the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day is:", common_day)

    # Determine the most common start hour
    common_hour = df['Start Time'].dt.hour.mode()[0]
    print("The most common hour is:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Determine the most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print("The most common start station is:", common_start)

    # Determine the most commonly used end station
    common_end = df['End Station'].mode()[0]
    print("The most common end station is:", common_end)

    # Determine the most frequent combination of start station and end station trip
    df['trip_combo'] = df['Start Station'] + " - " + df['End Station']
    common_combo = df['trip_combo'].mode()[0]
    print("The most common trip combination is:", common_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Determine the total travel time
    travel_time = df['Trip Duration'].sum()
    print("The total travel time is:", travel_time,"seconds")

    # Determine the mean travel time
    travel_mean = df['Trip Duration'].mean()
    print("The mean travel time is:", travel_mean, "seconds")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Determine the counts of user types
    print("User Types:\n", df['User Type'].value_counts(), "\n")

    # Determine the counts of gender
    if 'Gender' in df.columns:
        print("Gender counts:\n", df['Gender'].value_counts(), "\n")
    else:
        print("There is no gender data available for this city. \n")

    # Determine the earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
       earliest = int(df['Birth Year'].min())
       recent = int(df['Birth Year'].max())
       common = int(df['Birth Year'].mode()[0])
              
       print("The earliest birth year is:", earliest)
       print("The most recent birth year is:", recent)
       print("The most common birth year is:", common)
    else:
        print("No birth year data is available for this city.")
                   

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
              
              
def longest_trips_per_day(df):
    """Displays which day has the longest average trips"""
              
    avg_duration = (df.groupby('day_of_week')['Trip Duration'].mean().sort_values(ascending=False))
    print("\nAverage Trip Duration per Day:")
    print(avg_duration)
              

def display_raw_data(df):
    """Displays raw data upon user request for 5 rows."""        
              
    start = 0
    show = input("Would you like to see 5 lines of raw data? Enter yes or no:\n").strip().lower()
              
    while show == 'yes':
          print(df.iloc[start:start + 5])
          start += 5
              
          if start >= len(df):
              print("No more raw data to display.")
              break
              
          show = input("Would you like to see 5 more lines of raw data? Enter yes or no:\n").lower()     

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        longest_trips_per_day(df)
        display_raw_data(df)

        restart = input("Would you like to restart? Enter yes or no:").strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
