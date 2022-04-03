import pandas as pd
import statistics as stats
from currency_converter import CurrencyConverter

c = CurrencyConverter()

df = pd.read_csv('AAMSS.csv')


def fill_blanks(df):
    df["Other monetary comp"].fillna(0, inplace=True)
    df["Additional context on job title"].fillna('N/A', inplace=True)
    df["Additional context on income"].fillna('N/A', inplace=True)
    df["Currency - other"].fillna('N/A', inplace=True)
    df["State"].fillna('not stated', inplace=True)
    df["City"].fillna('not stated', inplace=True)
    df["Highest level of education completed"].fillna('not stated', inplace=True)
    df["Gender"].fillna('Other or prefer not to answer', inplace=True)
    df["Race"].fillna('Another option not listed here or prefer not to answer', inplace=True)

    return df


# simple function that changes lots of simple values and replaces all blank space where possible


def convert_dtype(df):
    for x in df.index:
        df.loc[x, 'Annual salary'] = int(df.loc[x, 'Annual salary'].replace(',', ''))
        df.loc[x, 'Gender'] = df.loc[x, 'Gender'].replace('Prefer not to answer', 'Other or prefer not to answer')

    df['Annual salary'] = pd.to_numeric(df['Annual salary'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    return df


# converts certain columns into different data types which better suit the data inside it

def remove_empty(df):
    new_df = df.dropna()
    return new_df

# removes all data empty spaces that haven't been cleaned by other catagories

def remove_dup(df):
    df.drop_duplicates(inplace=True)
    # removes duplicate data
    return df

# removes all duplicate data

def changing_currency(df):
    for x in df.index:
        df.loc[x, 'Currency'] = df.loc[x, 'Currency'].replace('AUD/NZD', 'AUD') 
        # changes AUD/NZD to AUD so the API can recognise it

        to_change = df.loc[x, 'Annual salary'] # stores all the salaries in a list
        current = df.loc[x, 'Currency']    #stores all current salaries' orignal currency
        try:
            z = c.convert(to_change, current, 'GBP') 
            #z is the new currency that has now been changed to great britiss pounds
            df.loc[x, 'Annual salary'] = int(z) #replaces the old value with new one
            df.loc[x, 'Currency'] = 'GBP' #changes currency to be GBP
        except:
            df.drop(x) #if the currency cannot be changed the whole row is removed 

    return df

# uses an API to find out the current exchange rates to change all currencies into GBP

def counting_countries(df):
    country_totals = {}
    for x in df['Country']:
        if x not in country_totals:
            country_totals[x] = 1
        elif x in country_totals:
            amount = country_totals[x]
            country_totals[x] = amount + 1
    print(country_totals)

# counts the amount of each country after it has been changed


def fixing_countries(df):
    lists = fixing_countries_spellings() # calls a dictionary of all the country inputs
    for x in df.index:
        if x % 1000 == 0:
            print(x) # prints how many have been changed, every 1000 changed
        for key in lists.keys(): # loops through each item within the key
            # print(key)
            if df.loc[x, 'Country'].strip() in lists[key]: # checks to see if the current subject with the loop is in the key
                df.loc[x, 'Country'] = key # if it is, it gets changed into the correct value
            else:
                df.drop(x) # removes the entry if it is not in the list
    print('FINISHED')
    return df

# changes all the countries, so they are the same and are easier to quantify

def fixing_countries_spellings():
    not_changed = []
    Remove = ["Y", 'Contracts', "Policy",
              "We don't get raises, we get quarterly bonuses, but they periodically asses income in the area you work, so I got a raise because a 3rd party assessment showed I was paid too little for the area we were located",
              "Global", "Currently finance",
              "I earn commission on sales. If I meet quota, I'm guaranteed another 16k min. Last year i earned an additional 27k. It's not uncommon for people in my space to earn 100k+ after commission. ",
              "I was brought in on this salary to help with the EHR and very quickly was promoted to current position but compensation was not altered. ",
              "Remote", "europe", "n/a (remote from wherever I want)", "Canada and USA", "Africa",
              "bonus based on meeting yearly goals set w/ my supervisor", "$2,175.84/year is deducted for benefits"]
    USA = ["USA", "United states of America", "United statew", "For the United States government, but posted overseas",
           " United States", "U.s.a.", "The US", "U. S. ", "U.S.", " U.S.", "United Status", "Uniyed states",
           "Uniyes States", "United States of Americas",
           "Worldwide (based in US but short term trips aroudn the world)", "United States of American ",
           "United States", "U.S", "United States of America", "USa", "Usa", " US", "usa", "uSa", "uSA",
           "Uniteed States", "UsA", "U.S.A", "U.S.", "uS", "USaa", "USAB", "US", "us", "USA ", "US ", "U.S>", "Us",
           "U.S.A.", "u.s.", "u.s.a.", "United States ", "United Stated", "United Statws", "U.S. ",
           "United States of Amrtica", "united states", "United state", "United states", "The United States",
           "UNITED STATES", "unites States", "Unites states", "United States of Amrtica ", "United STates",
           "united States of American ", "Uniited States", "United Stateds", "United states", "United Sates",
           "United Sates of America", "United States (I work from home and my clients are all over the US/Canada/PR",
           "Unted States", "United Statesp", "United Stattes", "United Statea", "Unites States", "United Statees",
           "UNited States", "United States of America ", "ISA", "United State", "United States of American", "America",
           "U.SA", "Unite States", "Unites states", "Us ", "united states ", "United states ",
           "united states of america", "United states ", "United State of America", "US of A", "united States", "U. S.",
           "United States of america ", "UnitedStates", "U.A.", "🇺🇸 ", "United State of America", "U.s.", "Usa ",
           "U.S.A ", "Unites states ", "United States is America", "United States of america", "Unites States ",
           "U.S.A. ", "USA-- Virgin Islands", "USA, but for foreign gov't", "U. S. '",
           "I work for an US based company but I'm from Argentina.", "Unitef Stated", "United Stares ", "California ",
           "San Francisco", 'Usat', "Uniter Statez", "United States Of America", "USA tomorrow ", "The US",
           "United Statss", "United Stares", "usa ", "United Sttes", "Virginia", "USS", "Hartford",
           "United states of America ", "United  States", "USD", "US govt employee overseas, country withheld",
           "I work for a UAE-based organization, though I am personally in the US.", "Unitied States", "united stated",
           "United States- Puerto Rico", "United states of america", "United Statues", "Untied States", "United y",
           "U. S ", "america"]
    UK = ["UK", "U.K. (northern England)", "Wales (United Kingdom)", "Englang", "UK (Northern Ireland)", "England, UK",
          "uk", "England, Gb", "UK, remote", "Britain ", "U.K. ", "United Kingdom (England)", "United Kingdom.",
          "United Kingdom", "U.K.", "Britain", "UK ", "England", "Uk", "United Kingdom ", "United Kingdom ",
          "United Kindom", "Great Britain", "England ", "U.K", "Unites kingdom ", "Scotland", "Great Britain ",
          "United kingdom", "United kingdom", "United kingdom ", '"England, UK"', "ENGLAND", "Uk ", "Scotland ",
          "England/UK", "England, UK.", "England, United Kingdom", "england",
          "UK, but for globally fully remote company", "UK for U.S. company", "Northern Ireland ", "United Kingdomk",
          "Jersey, Channel islands", "Wales (UK)", "Isle of Man", "England, United Kingdom ", "united kingdom",
          "UK (England)", "Wales, UK", "Scotland, UK", "Wales", "Northern Ireland, United Kingdom"]
    Canada = ["Canada", "Canda", "Can", "canada", "Canada", "CANADA", "Canada ", "canada ",
              "I am located in Canada but I work for a company in the US", "CANADA ", "Canadw", "Canadá",
              "Canada, Ottawa, ontario", "Csnada", "Canad"]
    Netherlands = ["Netherlands", "netherlands", "The Netherlands", "Nederland", "Netherlands ", "The netherlands",
                   "The Netherlands ", "the Netherlands", "the netherlands"]
    Finland = ["Finland", "finland"]
    Germany = ["Germany", "germany", "Germany ", "GERMANY", "germany", "Germany "]
    Australia = ["Australia", "Australia ", "Australia   ", "australia", "Australian "]
    France = ["France", "FRANCE", "france", "France "]
    Sweden = ["Sweden", "Sweden ", "sweden"]
    New_Zealand = ["New_Zealand", "New zealand", "New Zealand Aotearoa", "NZ", "NL", " New Zealand", "New_zealand",
                   "New Zealand ", "New Zealand", "new zealand", "Aotearoa New Zealand",
                   "From New Zealand but on projects across APAC"]
    India = ["India", "INDIA"]
    Ireland = ["Ireland", "Ireland ", "Northern Ireland", "Ireland ", "Ireland ", "ireland"]
    Croatia = ["Croatia", "croatia", "Croatia "]
    Pakistan = ["Pakistan", "Company in Germany. I work from Pakistan."]
    Mexico = ["Mexico", "Mexico ", "México"]
    China = ["China", "Mainland China", "Hong Kong ", "Hong Kong", "hong konh"]
    Japan = ["Japan", "Japan ", "Japan, US Gov position", "japan"]
    Spain = ["Spain", "Spain ", "spain"]
    Russia = ["Russia", "Russia ", "russia"]
    Bangladesh = ["Bangladesh", "Bangladesh ", "bangladesh"]
    Brazil = ["Brazil", "Brasil", "brazil", "Brazil "]
    Czech_Republic = ["Czech_Republic", "Czech Republic", "czech republic", "Czech republic", "czech Republic"]
    South_Africa = ["South_Africa", "South Africa", "south africa", "South africa", "south Africa", "South Africa "]
    Uzbekistan = ["Uzbekistan", "uzbekistan", "UXZ"]
    Belgium = ["Belgium", "belgium", "Belgium "]
    Denmark = ["Denmark", "denmark", "Denmark ", "Danmark"]
    Switzerland = ["Switzerland", "switzerland", "Switzerland ", "SWITZERLAND"]
    Italy = ["Italy", "italy", "Italy (South)"]
    Argentina = ["Argentina", "ARGENTINA BUT MY ORG IS IN THAILAND"]
    Norway = ["Norway", "Norway ", "norway"]
    Israel = ["Israel", "IS", "I.S."]
    Austria = ["Austria", "Austria, but I work remotely for a Dutch/British company",
               "Austria, but I work remotely for a Dutch/British company"]
    Poland = ['Poland', 'poland']
    Thailand = ['Thailand', 'thailand']
    Ukraine = ['Ukraine', "UA", "Ukraine "]
    Latvia = ['Latvia', "latvia"]
    North_Korea = ['North_Korea', "North Korea", "north korea", "North korea", "north Korea"]
    South_Korea = ["South_Korea", "South Korea", "south korea", "South korea", "south Korea", "South Korea "]
    United_Arab_Emirates = ["United_Arab_Emirates", "United Arab Emirates", "UAE", "United Arab Emirates "]
    Greece = ["Greece", "Greece ", "greece"]
    Romania = ["Romania", "From Romania, but for an US based company"]
    Malaysia = ["Malaysia", "malaysia"]
    Portugal = ["Portugal", "Portugal"]
    Namibia = ["Namibia", "na"]
    Philippines = ["Philippines", "philippines", "Remote (philippines)"]
    Singapore = ["Singapore", "singapore"]
    Cyprus = ["Cyprus", "cyprus"]
    Kenya = ['Kenya', 'kenya']
    Taiwan = ['Taiwan', 'taiwan']
    Bermuda = ['Bermuda', 'bermuda']
    Kuwait = ['Kuwait', 'kuwait']
    Sri_Lanka = ['Sri_Lanka', 'Sri lanka', 'Sri Lanka']
    Hungary = ['Hungary', 'hungary']
    Luxembourg = ['Luxembourg', 'luxembourg']
    Colombia = ['Colombia', 'colombia']
    Trinidad_and_Tobago = ['Trinidad_and_Tobago', 'Trinidad and Tobago']
    Cayman_Islands = ['Cayman_Islands', 'Cayman Islands']
    Czechia = ['Czechia', 'czechia']
    Puerto_Rico = ['Puerto_Rico', 'Puerto Rico']
    Lithuania = ['Lithuania', 'lithuania']

    lists = {'USA': USA,
             'UK': UK,
             'Canada': Canada,
             'Netherlands': Netherlands,
             'Finland': Finland,
             'Germany': Germany,
             'Australia': Australia,
             'France': France,
             'Sweden': Sweden,
             'New_zealand': New_Zealand,
             'India': India,
             'Ireland': Ireland,
             'Croatia': Croatia,
             'Pakistan': Pakistan,
             'Mexico': Mexico,
             'China': China,
             'Japan': Japan,
             'Spain': Spain,
             'Russia': Russia,
             'Bangladesh': Bangladesh,
             'Brazil': Brazil,
             'Czech_Republic': Czech_Republic,
             'South_Africa': South_Africa,
             'Uzbekistan': Uzbekistan,
             'Belgium': Belgium,
             'Denmark': Denmark,
             'Switzerland': Switzerland,
             'Italy': Italy,
             'Argentina': Argentina,
             'Norway': Norway,
             'Israel': Israel,
             'Austria': Austria,
             'Poland': Poland,
             'Thailand': Thailand,
             'Ukraine': Ukraine,
             'Latvia': Latvia,
             'North_Korea': North_Korea,
             'South_Korea': South_Korea,
             'United_Arab_Emirates': United_Arab_Emirates,
             'Greece': Greece,
             'Romania': Romania,
             'Malaysia': Malaysia,
             'Portugal': Portugal,
             'Namibia': Namibia,
             'Philippines': Philippines,
             'Singapore': Singapore,
             'Cyprus': Cyprus,
             'Kenya': Kenya,
             'Taiwan': Taiwan,
             'Bermuda': Bermuda,
             'Kuwait': Kuwait,
             'Sri_Lanka': Sri_Lanka,
             'Hungary': Hungary,
             'Luxembourg': Luxembourg,
             'Colombia': Colombia,
             'Trinidad_and_Tobago': Trinidad_and_Tobago,
             'Cayman_Islands': Cayman_Islands,
             'Czechia': Czechia,
             'Puerto_Rico': Puerto_Rico,
             'Lithuania': Lithuania

             }

    return lists

# lists all the dirty countries and the lists are then put into a dictionary which is then passed into the fixing countries function


def big_clean(df):
    df = fill_blanks(df)
    df = convert_dtype(df)
    df = remove_empty(df)
    df = remove_dup(df)
    df = changing_currency(df)
    df = fixing_countries(df) #this function took about 3 hours to run - so be warned it's kind of stinky
    print(df.info())
    df.to_csv('cleandata.csv', index=False)
