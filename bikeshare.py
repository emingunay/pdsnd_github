import time
import pandas as pd
import numpy as np
import calendar

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
    city=input("Which city's data would you like to see? Please choose from Chicago, New york city or Washington.\n").lower()
    while city not in['chicago','new york city','washington']:
        print('The input you specified is not valid')
        city=input("Which city's data would you like to see? Please choose from Chicago, New york city or Washington.\n").lower()
    month=input("Please specify month to filter data. Type 'all' for all months.\n").lower()
    while month not in['january','february','march','april','may','june','july','august','september','october','november','december','all']:
                       print('The input you specified is not valid')
                       month=input("Please specify month to filter data. Type 'all' for all months.\n").lower()

    day=input("Please specify day to filter data. Type 'all' for all days.\n").lower()
    while day not in ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']:
        print('The input you specified is not valid')
        day=input("Please specify day to filter data. Type 'all' for all days.\n").lower()


    print('-'*40)
    print("Selected city:", city)
    print("Selected month:", month)
    print("Selected day:", day)
    print("Getting statistics...")
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
    df['Start Time'] =pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january','february','march','april','may','june','july','august','september','october','november','december']
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

    popular_month=calendar.month_name[df['month'].mode()[0]]
    print("Most common month:", popular_month)

    popular_day=df['day_of_week'].mode()[0]
    print("Most common day:", popular_day)



    popular_hour = df['hour'].mode()[0]
    print("Most common hour:", popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station=df['Start Station'].mode()[0]
    print("Most common start station:", popular_start_station)


    popular_end_station=df['End Station'].mode()[0]
    print("Most common end station:", popular_end_station)    


    popular_station_combination=((df['Start Station'] + '-' + df['End Station']).mode()[0])
    print("Most frequent combination of start and end station:", popular_station_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_travel_time=sum(df['Trip Duration'])/60
    print("Total Travel Time:", total_travel_time, "minutes")


    mean_travel_time=df['Trip Duration'].mean()/60
    print("Mean Travel Time:", mean_travel_time, "minutes")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    count_user_types = df['User Type'].value_counts()
    print("Counts of user types:", count_user_types)


    if city in['chicago','new york city']:
       gender_count=df['Gender'].value_counts()
       print("Counts of gender:\n", gender_count)
    else:
       print("There is no gender data in the selected city.")


    if city in['chicago','new york city']:
       oldest_user=int(df['Birth Year'].min())
       youngest_user=int(df['Birth Year'].max())
       most_common_birth_year=int(df['Birth Year'].mode()[0])
       print("Birth Year of Oldest User:\n", oldest_user)
       print("Birth Year of Youngest User:\n", youngest_user)
       print("Most Common Year of Birth:\n", most_common_birth_year)
    else:
       print("There is no birth year data in the selected city.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    raw_data=input('Would you like to see 5 lines of raw data? Type Yes or No.\n').lower()
    line=0
    while 1==1:
        if raw_data=='yes':
            print(df.iloc[line : line+5])
            line=line+5
            raw_data=input('Would you like to see 5 more lines of raw data? Type Yes or No.\n').lower()
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)

        restart = input('\nWould you like to restart? Type yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
