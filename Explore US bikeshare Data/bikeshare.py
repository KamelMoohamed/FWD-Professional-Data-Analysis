import time
import pandas as pd
# import numpy as np

CITY_DATA = {'chicago': r'chicago.csv',
             'new york city': r"new_york_city.csv",
             'washington': r'washington.csv'}

months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Getting user input for city (chicago, new york city, washington).
    cities = ['chicago', "new york city", 'washington']
    while True:
        city = input("please choose the city that you want to explore from: \n - Chicago.\n"
                     " - New York city.\n - Washington.\n")
        city = city.lower()
        if city in cities:
            break
        else:
            print("Invalid Input, please try again.")

    # Getting user input for month (all, january, february, ... , june)
    while True:
        month = input("Please choose the month form:  \n - All.\n - January.\n - February.\n"
                      " - March.\n - April.\n - May.\n - June.\n")
        month = month.lower()
        if month in months:
            break
        else:
            print("Invalid Input, please try again.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("please choose the day from: \n - All.\n - Monday.\n - Tuesday."
                    " - Wednesday.\n - Thursday.\n - Friday.\n - Saturday.\n - Sunday.\n")
        day = day.lower()
        if day in days:
            break
        else:
            print("Invalid Input, please try again.")

    print('-' * 40)
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
    # Importing the CSV file of specific city
    df = pd.read_csv(CITY_DATA[city])

    # Converting the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracting month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        day = days.index(day) - 1
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displaying the most common month
    print("Most common month: ", months[(df['month'].mode()[0])])

    # Displaying the most common day of week
    print("Most common day: ", days[(df['day_of_week'].mode()[0]) +1])

    # Displaying the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("Most common hour: ", df['day_of_week'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displaying most commonly used start station
    print(" - Most station used as start station: ", df['Start Station'].mode()[0])

    # Displaying most commonly used end station
    print(" - Most station used as end station: ", df['End Station'].mode()[0])

    # Displaying most frequent combination of start station and end station trip
    df['Stations Combination'] = list(zip(df['Start Station'], df['End Station']))

    stationKeys = df['Stations Combination'].value_counts().keys().tolist()
    stationValues = df['Stations Combination'].value_counts().tolist()
    print("\nMost combination of start and end stations: ", "--->", stationValues[0], "times.")
    print(" - Start Station: ", stationKeys[0][0])
    print("   End Station:   ", stationKeys[0][1], "\n")

    # if there is two values of combination that have the same value
    for i in range(len(stationKeys) - 1):
        if stationValues[i] == stationValues[i + 1]:
            print(" - Start Station: ", stationKeys[i + 1][0])
            print("   End Station:   ", stationKeys[i + 1][1], "\n")
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Duration'] = df['End Time'] - df['Start Time']

    # Displaying mean travel time
    print("Mean Travel Time: ")
    print(" - ", df['Travel Duration'].mean())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Extract counts of user type
    userKeys = df['User Type'].value_counts().keys().tolist()
    uservalues = df['User Type'].value_counts().tolist()
    # Display user type
    print("User Type statistics: ")
    for i in range(0, len(userKeys)):
        print(" - ", userKeys[i], " " * (20 - len(userKeys[i])), uservalues[i])

    # Checking if the city is washington or not
    if city != "washington":

        # Extract counts of gender and display it
        genderKeys = df['Gender'].value_counts().keys().tolist()
        genderValues = df['Gender'].value_counts().tolist()
        # Display gender
        print("\nGender statistics: ")
        for i in range(0, len(genderKeys)):
            print(" - ", genderKeys[i], " " * (20 - len(genderKeys[i])), genderValues[i])

        # Display earliest, most recent, and most common year of birth
        print("\nStatistics of users' year of birth: ")
        print(" - Earliest Year of Birth: ", df['Birth Year'].min())
        print(" - Most Recent Year of Birth: ", df['Birth Year'].max())
        print(" - Most Common Year of Birth: ", df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data?\n - Yes.\n - No.\n')
        view_data = view_data.lower()
        if view_data == 'yes':
            print('\nData is loading...\n')
            print(df.head())
            break
        elif view_data == 'no':
            return
        else:
            print("Invalid Input, please try again.")

    count = 1
    while True:
        exit2 = True
        while exit2:
            view_data = input('\nWould you like to view the next 5 rows of individual trip data?\n - Yes.\n - No.\n')
            view_data = view_data.lower()
            if view_data == 'yes':
                print('\nData is loading...\n')
                print(df[count * 5: count * 5 + 5])
                exit2 = False
            elif view_data == 'no':
                return
            else:
                print("Invalid Input, please try again.")
        count += 1


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