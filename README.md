# Machine Learning - Real Estate Valuations

<img src="Subway.gif" width="500" height="250"/> | <img src="Police.gif" width="500" height="250"/>

# OVERVIEW

* The datasets created and utilized for our analysis and visualizations took data on New York City (crime, education, environment, socio-economic, subway-access) filtered by zipcode. After initial exploratory analysis and cleaning, we decided to move foward with a Linear Regression and Random Forest Machine Learning Models.

# EXTRACT
* Technologies Used: 
  * Back End: Pandas, sql-alchemy, numpy, sklearn.preprocessing [oneHotEncoder], scipy.stats, geopy[distance], geopy.geocoders[Nominatim], geopy.exc[GeoCoderTimedOut], geopy.extra.rate_limiter[RateLimiter], geopandas, plotly_express, tqdm, tqdm.pandas(), sklearn.neighbors, tqd, datetime, tqdm_notebook, 


Group Members: Stephen Brescher, Shadee Tabassi, Alison Sadel, Manny Mejia

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
   

### NYC Brownfields Data Set
  * Use ``str.contains()`` method to remove all records that were outside New York City (original dataset was for NY State brownfield records)
  * Use strip method combined with a slicer to ensure zipcodes were exactly five characters in length
   ``df['zipcode'] = df['zipcode'].str[:5]``
  * Group status of the clean-up site using ``str.replace()`` method - data has different rating scale depending on funding of the clean up project so some descriptions could be merged.
  * Generate binary values using ``pd.get_dummies`` on health status:
     * Potential Threat
     * Completed - Maintenance Required - Continued Threat
     * Completed - Clean - No Further Action
     * Active - Significant Threat
     * Active - Mild Threat

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

