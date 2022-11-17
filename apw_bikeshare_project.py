import time

import numpy as np
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all','january','february','march','april','may','june']
weekdays = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
#pretend like I refactored something with the weekdays variable 

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
   
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Which city would you like to analyze? Please enter "chicago" "new york city" or "washington"').lower().rstrip()
    while True: 
        if city in CITY_DATA:
            break
        else: 
            city = input("Sorry, I didn't understand that. Please enter 'chicago' 'new york city' or 'washington' with no quotations.").lower().rstrip()
    print("Thanks! Now accessing data from",city.title())

    # get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to analyze? Please enter the name of a month January through June, or type 'all' with no quotations.").lower().rstrip()
    while True:
        if month in months:
            break
        else:
            month = input("Sorry, I didn't understand that. Please enter the name of a month January through June, or type 'all' with no quotations.").lower().rstrip()
    if month == months[0]:
        print("Thanks! Now accessing data from all months.")
    else:
        print("Thanks! Now accessing data from {}.".format(month.title()))

    # get user input for day of week (all, monday, tuesday, ... sunday)
    weekdays = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    weekday = input("Which day of the week would you like to analyze? Please enter a day of the week or type 'all' with no quotations.").lower().rstrip()
    while True:
        if weekday in weekdays:
            break
        else: 
            weekday = input("Sorry, I didn't understand that. Please enter a day of the week or type 'all' with no quotations.").lower().rstrip()
    if weekday == weekdays[0]:
        print("Thanks! Now accessing data from all days of the week.")
    else:
        print("Thanks! Now accessing data from {}s.".format(weekday.title()))

    print('-'*40)
    return city, month, weekday


def load_data(city, month, months, weekday, weekdays):
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
    
    # convert time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and weekday and hour
    df['month'] = df['Start Time'].dt.month
    df['weekday'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month
    if month != months[0]:
        month = months.index(month)
        df = df[df['month'] == month]

    # filter by weekday
    if weekday != weekdays[0]:
        weekdays = weekdays[1:]
        df = df[df['weekday'] == weekdays.index(weekday)]

    return df


def time_stats(df,month,weekday):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == months[0]:
        popular_month = df['month'].mode()[0]
        print('The most common month is {}.'.format(months[popular_month].title()))

    # display the most common day of week
    if weekday == weekdays[0]:
        popular_day = df['weekday'].mode()[0]
        print('The most common weekday is {}.'.format(weekdays[popular_day].title()))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most common start hour is {}.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print("The most commonly used start station is {}.".format(popular_start.title()))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print("The most commonly used end station is {}.".format(popular_end.title()))

    # display most frequent combination of start station and end station trip
    df['Route'] = list(zip(df['Start Station'],df['End Station']))
    popular_route = list(df['Route'].mode()[0])
    print('The most popular route starts at {} and ends at {}.'.format(popular_route[0],popular_route[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['duration'] = df['End Time'] - df['Start Time']

    # display total travel time
    total_travel = df['duration'].sum()
    print("The total time users travelled during the period you specified was {}.".format(total_travel))

    # display mean travel time
    mean_travel = df['duration'].mean()
    print("The average trip duration during the period you specified was {}.".format(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_count = df['User Type'].value_counts()
    print("Here's a breakdown of the types of users during the specified time period:\n{}".format(user_type_count.to_string()))

    # Display counts of gender
    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print("Users during the specified period reported their gender as follows:\n{}".format(gender_count.to_string()))

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]
        print("Of the users during the specified period, the oldest was born in {}, the youngest was born in {}, and the most common birth year was {}.".format(earliest,recent,common))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, weekday = get_filters()
        df = load_data(city, month, months, weekday, weekdays)

        time_stats(df,month,weekday)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
    
#this line is to show a change for the git repo