# Machine Learning - Real Estate Valuations

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

### NYC Brownfields Data Set
  * Use ``str.contains()`` method to remove all records that were outside New York City (original dataset was for NY State brownfield records)
  * Use strip method combined with a slicer to ensure zipcodes were exactly five characters in length
   ``df['zipcode'] = df['zipcode'].str[:5]``
  * Group status of the clean-up site using ``str.replace()`` method - data has different rating scale depending on funding of the clean up project so some descriptions could be merged.
  * Generate binary values using ``pd.get_dummies`` on health status:
     * Potential Threat
     * Completed - Maintenance Required - Continued Threat
     *  Completed - Clean - No Further Action
     *  Active - Significant Threat
     *  Active - Mild Threat

### NYC Crime Data Set
* Remove all complaint that were records before 2020
``df = df[df['Start_Date'].str.contains("2020", na=False)] ``
* Ensure that each complaint_id value was unique
``df = df.drop_duplicates(subset=['complaint_id'])``
* Convert complaint_date to datetime
``df.complaint_date = pd.to_datetime(df.complaint_date, format='%m/%d/%Y')``
* Create a column to denote if the danger level is low or high
  <code> df["danger_level"] = ""
  <br>
  df.loc[df["complaint_desc"] == 'sex crimes', "danger_level"] = 'high' 
  <br>
  df.loc[df["complaint_desc"] == 'rape', "danger_level"] = 'high' 
  <br>
  df.loc[df["complaint_desc"] == 'dangerous weapons', "danger_level"] = 'high' 
  <br>
  df.loc[df["complaint_desc"] == 'felony sex crimes', "danger_level"] = 'high'
  <br>
  df.loc[df["complaint_desc"] == 'burglary', "danger_level"] = 'high' 
  <br>
  df.loc[df["complaint_desc"] == 'robbery', "danger_level"] = 'high' 
  <br>
  df.loc[df["complaint_desc"] == 'arson', "danger_level"] = 'high' 
  <br>
  df['danger_level'] = df['danger_level'].replace('', np.nan, regex=True) 
  <br>
  df['danger_level'] = df['danger_level'].fillna('low') </code> 

* Generate binary values using ``pd.get_dummies`` on category of crime (violation, misdemeanor and felony) and on newly created feature - whether the crime is defined as violent and therefore the danger level is higher:

