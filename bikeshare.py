import time
import pandas as pd

#set amount of displayed df columns to 8
pd.set_option('display.max_columns', 8)

#set width of the terminal window to 1000
pd.options.display.width = 1000

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

days = ['monday','tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    #get user input for city (chicago, new york city, washington).
    city_question = input('What the city do you want explore? Please enter Chicago, New York City or Washington: ').lower()
    while city_question not in CITY_DATA.keys():
        city_question = input('The city you entered is not on the list. Try again: ').lower()

    #get user input for month (all, january, february, ... , june)
    month_question = input('Are you interested in filtering data by months?\n Enter the month from January to June or type "all" if you want to check all months: ').lower()
    while month_question not in months:
        month_question = input('Not in the list. Try again: ').lower()

    #get user input for day of week (all, monday, tuesday, ... sunday)
    day_question = input('What day of week do you want to explore?\n Type "all" if you interested in all weekdays: ').lower()
    while day_question not in days:
        day_question = input('Oops! This is not a weekday. Type a weekday or "all": ').lower()

    city = city_question
    month = month_question
    day = day_question

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

    # extract month and day of week from Start Time to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

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
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame containing city data
    """

    print('\nCalculating The Most Frequent Times of Travel...\n')

    # get timestamp of the moment in which the function execution started and store it in start_time
    start_time = time.time()

    #display the most common month

    popular_month = df['month'].mode()[0]
    print('The most popular month: ', popular_month)

    #display the most common day of week

    popular_dayweek = df['day_of_week'].mode()[0]
    print('The most popular dayweek: ', popular_dayweek)

    #display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour: ', popular_hour)

    # get timestamp of the moment in which the function execution finished and substract the start_time from it to get the function execution time
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """
    Displays statistics on the most popular stations and trip.

     Args:
        df - Pandas DataFrame containing city data
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #display most commonly used start station

    popular_start_s = df['Start Station'].mode()[0]
    print('Most commonly start station: ', popular_start_s)

    #display most commonly used end station

    popular_end_s = df['End Station'].mode()[0]
    print('Most commonly end station: ', popular_end_s)

    #display most frequent combination of start station and end station trip

    df['combination'] = 'From "' + df['Start Station'] + '" to "' + df['End Station'] + '"'
    frequent_comb = df['combination'].mode()[0]
    print('Most commonly combination of start station and end station trip: ', frequent_comb)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """
    Displays statistics on the total and average trip duration.

     Args:
        df - Pandas DataFrame containing city data
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time

    total_time = df['Trip Duration'].sum()
    #Convert total_time into hours, minutes and seconds
    t_convert = time.strftime("%H hours %M minutes %S seconds", time.gmtime(total_time))
    print('Total travel time: ', t_convert)

    #display mean travel time

    mean_total_time = df['Trip Duration'].mean()
    #Convert mean_total_time into hours, minutes and seconds
    m_convert = time.strftime("%H hours %M minutes %S seconds", time.gmtime(mean_total_time))
    print('Mean of travel time: ', m_convert)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """
    Displays statistics on bikeshare users.

     Args:
        df - Pandas DataFrame containing city data
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types

    user_types = df.groupby(['User Type']) ['User Type'].count()
    print(user_types)

    #Display counts of gender

    try:
        gender = df.groupby(['Gender']) ['Gender'].count()
        print('User types - ', gender)

    except KeyError:
        print("There is no gender information in this city.")

    #Display earliest, most recent, and most common year of birth

    try:
        earliest_year = int(df['Birth Year'].min())
        recent_year = int(df['Birth Year'].max())
        common_year =int(df['Birth Year'].mode()[0])
        print('The earliest year of birth: ', earliest_year)
        print('The most recent year of birth: ', recent_year)
        print('The most common year of birth: ', common_year )

    except KeyError:
         print("There is no information about birth year in this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """
    Displays raw data.

     Args:
        df - Pandas DataFrame containing city data
    """

    i = 5
    #get user input for raw data display
    while True:
         raw_question = input('Would you like to display raw data? Type yes or no: ').lower()
         if(raw_question == 'yes'):
             #display first five rows of data
             temp_df = df.drop(columns = ['Unnamed: 0', 'month','day_of_week', 'hour', 'combination'])
             print(temp_df.head(i))
             break
         elif(raw_question == 'no'):
             break

    #get user input for next five lines of raw data display
    while raw_question == 'yes':
        next_data = input('Would you like to display the next 5 lines of raw data? Type yes or no: ').lower()
        if(next_data == 'yes'):
            i += 5
            #stop displaying raw data after displaying last row
            if(i <= df.shape[0]):
                print(temp_df.head(i), '\n', '-' * 60)
                continue
            else:
                print('You reached the end of data.')
                break
        elif(next_data == 'no'):
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
