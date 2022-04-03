import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import data_cleaner
import statistics as stat
from collections import Counter

figure(figsize=(8, 6), dpi=80)
df = pd.read_csv('cleandata.csv')


# function to add value labels
def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')



def race_salary_graph(df):
    #race compared with yearly salary
    totals =race_amount(df)
    gen_list=['White','Black or African American','Hispanic, Latino, or Spanish origin','Another option not listed here or prefer not to answer']
    raw_totals =[totals['White'],totals['Black or African American'],totals['Hispanic, Latino, or Spanish origin'],totals['Another option not listed here or prefer not to answer']]
    
    index = {
    'White' : 0,
    'Black or African American' : 1,
    'Hispanic, Latino, or Spanish origin' : 2,
    'Another option not listed here or prefer not to answer' : 3    
    }

    race_salary = [[],[],[],[]]
    
    for x in df.index:
        try:
            numbered_gen = index[df.loc[x,'Race']]
            race_salary[numbered_gen].append(df.loc[x,'Annual salary'])
        except:
            pass
    
    for x in range(len(race_salary)):
        race_salary[x] = stat.mean(race_salary[x])


    plt.bar((gen_list),race_salary)
    addlabels(gen_list,race_salary)
    plt.xlabel('Race')
    plt.xticks(rotation = 8, fontsize = 8)
    plt.text(-0.9,135000,f"""
             White:{raw_totals[0]}
             Black or African American:{raw_totals[1]}
             Hispanic, Latino, or Spanish origin:{raw_totals[2]}
             Another option or prefer not to answer:{raw_totals[3]}
             """
                                        )
    plt.title('Highest 4 races compared to salary')
    plt.savefig("Race Vs Salary.png")
    plt.show()

def gender_salary_graph(df):
    #gender compared with yearly slaray
    totals =gender_amount(df)
    gen_list=['Man','Woman','Non-binary','Other or prefer not to answer']
    raw_totals =[totals['Man'],totals['Woman'],totals['Non-binary'],totals['Other or prefer not to answer']]
    
    index = {
    'Man' : 0,
    'Woman' : 1,
    'Non-binary' : 2,
    'Other or prefer not to answer' : 3    
    }

    gender_salary = [[],[],[],[]]
    
    for x in df.index:
        try:
            numbered_gen = index[df.loc[x,'Gender']]
            gender_salary[numbered_gen].append(df.loc[x,'Annual salary'])
        except:
            pass
    
    for x in range(len(gender_salary)):
        gender_salary[x] = stat.mean(gender_salary[x])


    plt.bar((gen_list),gender_salary)
    addlabels(gen_list,gender_salary)
    plt.xlabel('Gender')
    plt.text(0.5,135000,f"""
             Men:{raw_totals[0]}
             Women:{raw_totals[1]}
             Non-binary:{raw_totals[2]}
             Other or prefer not to answer:{raw_totals[3]}
             """
                                        )
    
    plt.savefig("Gender Vs Salary.png")
    plt.show()
    

def age_graph(df):
    totals = race_amount(df)
    highest_races = dict(Counter(totals).most_common(5))
    names = list(highest_races.keys())
    values = list(highest_races.values())

    plt.bar(range(len(highest_races)), values, tick_label=names)
    plt.xlabel('Races')
    plt.xticks(rotation = 8, fontsize = 6)
    plt.savefig("top_races.png")
    plt.show()

def counting_countries(df):
    country_totals = {}
    for x in df['Country']:
        if x not in country_totals:
            country_totals[x] = 1
        elif x in country_totals:
            amount = country_totals[x]
            country_totals[x] = amount + 1

    return country_totals

def country_graph(df):
    totals = counting_countries(df)
    highest_countries = dict(Counter(totals).most_common(5))
    names = list(highest_countries.keys())
    values = list(highest_countries.values())

    plt.bar(range(len(highest_countries)), values, tick_label=names)
    plt.xlabel('Countries')
    #plt.xticks(rotation = 8, fontsize = 6)
    plt.savefig("top_Countries.png")
    plt.show()



def gender_amount(df):
    gender_totals = {
    'Man' : 0,
    'Woman' : 0,
    'Non-binary' : 0,
    'Other or prefer not to answer' : 0  
    }
    for x in df['Gender']:
        #print(x)
        amount=gender_totals[x]
        gender_totals[x]=amount+1
    #print(gender_totals)

    return gender_totals


def age_amount(df):
    age_totals = {}
    for x in df['How old are you?']:
        if x not in age_totals:
            age_totals[x]=1
        elif x in age_totals:
            amount=age_totals[x]
            age_totals[x]=amount+1
    #print(age_totals)

    return age_totals


def race_amount(df):
    race_totals = {}
    for x in df['Race']:
        if x not in race_totals:
            race_totals[x]=1
        elif x in race_totals:
            amount=race_totals[x]
            race_totals[x]=amount+1
    #print(race_totals)

    return race_totals


#gender_salary_graph(df)
#gender_totals = gender_amount(df)
#age_totals = age_amount(df)
#race_totals = race_amount(df)
#race_salary_graph(df)
#age_graph(df)
country_graph(df)