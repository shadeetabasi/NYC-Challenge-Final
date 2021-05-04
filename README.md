# Machine Learning - Real Estate Valuations
Group Members: Stephen Brescher, Shadee Tabassi, Alison Sadel, Manny Mejia

<img align= "center" src="NYC.gif" width="1000" height="500"/> 


# OVERVIEW
* The datasets created and utilized for our analysis and visualizations took data on New York City (crime, public school rankings, tree health, proximity to and status of brownfield clean-up sites, socio-economic indicators like subway access for the disabled, subway proximity and walkability and the percentage of students qualifying for subsidized school meals, filtered by zipcode. After initial exploratory analysis and cleaning, we decided to move foward with a Linear Regression and Random Forest Machine Learning Models.

* Technologies Used: 
  * Back End: Flask, PostgreSQL, Python, Pandas, sqlalchemy [create_engine], numpy, os, dotenv[load_dotenv], sklearn.preprocessing [oneHotEncoder], scipy.stats, geopy[distance], geopy.geocoders[Nominatim], geopy.exc[GeoCoderTimedOut], geopy.extra.rate_limiter[RateLimiter], geopandas, plotly_express, tqdm, tqdm.pandas(), sklearn.neighbors, tqd, datetime, tqdm_notebook, sklearn[import tree], sklearn.model_selection [train_test_split], sklearn.impute [SimpleImputer], sklearn.ensemble [RandomForestClassifier]
  * Front End: Javascript, Leaflet, HTML, CSS, Bootstrap 


# Machine Learning - Random Forest Regression

<img align= "center" src="3d.png" width="475" height="300"/> | <img align= "center" src="randomforestregression.png" width="475" height="300"/> 

After initial exploratory analysis of the categorical and numeric data we had within the 6 original datasets, we ultimately decided to train the model using Random Forest Regression. Random Forest is an algorithm characterized as being both a supervised learning algorithm and an ensemble method. Supervised learning is defined by its use of labeled datasets to train algorithms to classify data and predict outcomes accurately. As input data (features) is fed into the model, it adjusts its weights through a reinforcement learning process, which ensures that the model is fitted appropriately. Random Forest can also be classified as an ensemble method because it uses multiple learning algorithms to obtain better predictive performance than could be obtained from any of the constituent learning algorithms alone. The algorithm is comprised of an n number of decision trees which collectively predict an estimate of the expected outcome by way of voting. The goal of ensemble methods is to combine the predictions of several base estimators built with a given learning algorithm in order to improve generalizability. The Ensemble Method's accuracy is consequently enhanced by the collective wisdom of the many decision trees which helps prioritize features and reduce noise. At its foundation Random Forest is a collection of if/or conditionals that can be used to understand the important decision nodes and how they led to the final output (dependent variable). For each new input, each tree in the forest predicts a value for Y (output). The final value can be calculated by taking the average of all the values predicted by all the trees in forest.

# TRANSFORM
### General clean up
  * ``str.lower()`` to convert all strings to lowercase
  * Rename columns to eliminate spaces and capitalization
  * Drop irrelevant columns
   * ``df[df.columns.difference([])``
  * Merge duplicative column values with slightly different naming conventions with ``.replace({})`` 
  * Drop all rows where zipcode column contained NaN values
  ``df = df.dropna(subset=['zipcode'])``
  * Datatype Conversion
  ``df['column_name'] = df['column_name'].astype('')``
  * Use strip method combined with a slicer to ensure zipcodes were exactly five characters in length
   ``df['zipcode'] = df['zipcode'].str[:5]``
   

### NYC Brownfields Data Set
  * Use ``str.contains()`` method to remove all records that were outside New York City (original dataset was for NY State brownfield records)
  * Group status of the clean-up site using ``str.replace()`` method - data has different rating scale depending on funding of the clean up project so some descriptions could be merged.
  * Generate binary values using ``pd.get_dummies`` on health status:
     * Potential Threat
     * Completed - Maintenance Required - Continued Threat
     * Completed - Clean - No Further Action
     * Active - Significant Threat
     * Active - Mild Threat
 ```
 # Generate binary values using get_dummies for danger level
 dum_df1 = pd.get_dummies(df, columns=["danger_level"], prefix=["danger_level_is"] )
 ```

### NYC Crime Data Set
* Remove all complaint that were records before 2020
``df = df[df['Start_Date'].str.contains("2020", na=False)] ``
* Ensure that each complaint_id value was unique
``df = df.drop_duplicates(subset=['complaint_id'])``
* Convert complaint_date to datetime
``df.complaint_date = pd.to_datetime(df.complaint_date, format='%m/%d/%Y')``
* Create a column to denote if the danger level is low or high
  ```
  # Create empty column
  df["danger_level"] = ""
  
  # Assign specific complaint descriptions as having a higher danger level based on the gravity of the crime
  df.loc[df["complaint_desc"] == 'sex crimes', "danger_level"] = 'high' 
  df.loc[df["complaint_desc"] == 'rape', "danger_level"] = 'high' 
  df.loc[df["complaint_desc"] == 'dangerous weapons', "danger_level"] = 'high' 
  df.loc[df["complaint_desc"] == 'felony sex crimes', "danger_level"] = 'high'
  df.loc[df["complaint_desc"] == 'burglary', "danger_level"] = 'high' 
  df.loc[df["complaint_desc"] == 'robbery', "danger_level"] = 'high' 
  df.loc[df["complaint_desc"] == 'arson', "danger_level"] = 'high' 
  
  # Fill all empty values in the newly created 'danger_level' column with NaNs and use fillna() to create high/low dichotomy 
  df['danger_level'] = df['danger_level'].replace('', np.nan, regex=True)
  df['danger_level'] = df['danger_level'].fillna('low')
  ```

* Generate binary values using ``pd.get_dummies`` on category of crime (violation, misdemeanor and felony) and on newly created feature - whether the crime is defined as violent and therefore the danger level is higher:

### NYC School Rankings (Elementary, Middle, High) Datasets
* Drop all rows where county is not the Bronx, Brooklyn, Richmond, Queens and/or New York County
 ```
 # Filter out any counties outside NYC 5 Boroughs
 elem['county'].value_counts()
 elem = elem[elem['county'].str.contains("Richmond County|New York|Brooklyn|Kings County|Queens|Bronx")]

 # Reclassify inaccurate column values by replacing School District assignment with county that district is located in
 elem.loc[elem['county'].str.contains('7|8|9|10|11|12'), 'county'] = 'Bronx County'
 elem.loc[elem['county'].str.contains('13|14|17|21|22|24|27'), 'county'] = 'Kings County'
 elem.loc[elem['county'].str.contains('3|4|5|6'), 'county'] = 'New York County'
 ```

* Create a new feature and corresponding classification for Generating Binary Values for School Rankings relative to the State rankings
  * ``Use pd.cut( )`` method to bin School Rankings into Top 25th, 50th Percentile, 75th Percentile and Bottom 25th Percentile
  * Use``pd.get_dummies`` on the newly created feature (binned school rankings)
* Create a new feature and corresponding classification for generating binary values on a schools free lunch recipient status
  * Within NYC 72% of students are eligible for discounted or free lunch
  * Use ``np.where`` method to create Boolean column - true denotes that at that school the percentage of those eligible for subsidized food is greater than 72%
    * True denotes greater that the  72% of students are eligible for free lunch
    ``elem['lunch_eligibity_high'] = np.where(elem['free_lunch_recipient'] > 72, True, False)``
  * Use``pd.get_dummies`` on the newly created feature showcasing if the school was above the city average in student eligibility of subsidized breakfast/lunch
   

### NYC Tree Dataset

* Strip out the month and day values to leave only the year the tree was planted
```
# Ensure date planted only reflects the year planted
df['year_planted'] = pd.DatetimeIndex(df['created_at']).year
```
* Add Categorical Encoding & Binary Values for the heath status of the tree - good, fair, poor, dead
```
# Convert type of columns to 'category'
df['health'] = df['health'].astype('category')

# Assign numerical values and store in another column
df['health_level'] = df['health'].cat.codes

# Create instance of OneHotEncoder
enc1 = OneHotEncoder(handle_unknown='ignore')

# Pass tree health category column (label encoded values of health_status)
enc_df1 = pd.DataFrame(enc1.fit_transform(df[['health_level']]).toarray())

# Merge with main df on key values
df = df.join(enc_df1)

# Rename columns that were added from encoder array
df[[0, 1, 2, 3]] = df[[0, 1, 2, 3]].astype(str)
df = df.rename(columns={0: 'health_level_dead', 1: 'health_level_fair', 2: 'health_level_good', 3: 'health_level_poor'}) 
```

### NYC Subway Stations Dataset

* Use``pd.get_dummies`` to generate binary values for whether the subway station is ADA-Accessiblle - Yes, No, Partially
* CHALLENGE: 
 * Ultimately, all datasets needed to share zipcode as a common column to later perform a groupby function. The dataset provide latitude and longitude values  however there was no zipcode field. The Geopy library was used to create an API to find all location descriptor, using the latitude longitude pairs.

```
# Import Libaries
from tqdm import tqdm
tqdm.pandas()
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="emailhere@gmail.com")
from geopy.extra.rate_limiter import RateLimiter

reverse = RateLimiter(geolocator.reverse, min_delay_seconds=.01)

df['location'] = df.progress_apply(lambda row: reverse((row['lat_field'], row['lon_field'])),axis=1)
     
def parse_zipcode(location):
    if location and location.raw.get('address') and location.raw['address'].get('postcode'):
        return location.raw['address']['postcode']
    else:
        return None
df['zipcode'] = df['location'].apply(parse_zipcode)

```

### NYC Real Estate Dataset
* Use``pd.get_dummies`` to generate binary values for whether the subway station is ADA-Accessiblle - Yes, No, Partially
* CHALLENGE: Preparing the data for front end user input and Machine Learning 
  *  Beds, Baths, Sold Price
  *  Days on Market Fill NA with Average
  *  Create bins based on IQR


### Determiing Walkability - Real Estate & Subway Station Datasets

# MACHINE LEARNING - Random Forest Regression

*  Merge all dataframes outlined above, only keeping the binary encoded values to use as features (x variables)
*  Assign X values from the Real Estate Final table for the model & cast all as int 
*  Assign Y value (dependent variable) from the Real Estate Final table for the model (y = sold_price)
```
# Run test and training of the data
X_train, X_test, y_train, y_test = train_test_split(X1, y1, random_state = 101)

# Run the Random Forest Regression and then fit it to the x and y training data
model = RandomForestRegressor(n_estimators = 2000, max_depth = 150, random_state = 101)

# Use ``.ravel() method`` to convert dataframe to to 1 dimensional array to fit machine learning model
model.fit(X_train, y_train.values.ravel())


# Make a prediction 
y1_pred = model.predict(X_test)

# Enusre that y1_pred is not in scientific notation
pd.set_option('display.float_format', lambda x: '%.3f' % x)

result_regression = X_test
result_regression['sold_price'] = y_test
result_regression['y1_pred'] = y1_pred.tolist()
result_regression.sample(5)

# Score the y test data vs the predicted data
r2 = r2_score(y_test, y1_pred)
r2
print('R-squared scores:', round(r2, 3))

R-SQUARED SCORES: .77
```

# SQL QUERIES & FLASK
# FRONT END 


