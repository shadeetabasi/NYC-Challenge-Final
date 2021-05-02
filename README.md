# Machine Learning - Real Estate Valuations

# OVERVIEW

* The datasets created and utilized for our analysis and visualizations took data on New York City (crime, education, environment, socio-economic, subway-access) filtered by zipcode. After initial exploratory analysis and cleaning, we decided to move foward with a Linear Regression and Random Forest Machine Learning Models.

# EXTRACT
* Technologies Used: 
  * Back End: Pandas, sql-alchemy, numpy, sklearn.preprocessing [oneHotEncoder], scipy.stats, geopy[distance], geopy.geocoders[Nominatim], geopy.exc[GeoCoderTimedOut], geopy.extra.rate_limiter[RateLimiter], geopandas, plotly_express, tqdm, tqdm.pandas(), sklearn.neighbors, tqd, datetime, tqdm_notebook, 


Group Members: Stephen Brescher, Shadee Tabassi, Alison Sadel, Manny Mejia

# TRANSFORM
* General clean up
  * ``str.lower()`` to convert all strings to lowercase
  * Rename columns to eliminate spaces and capitalization
  * Drop irrelevant columns
   * ``df[df.columns.difference([])``
  * Merged duplicative column values with slightly different naming conventions with ``.replace({})`` 

* Brownfields Data Set
  * Used ``str.contains()`` method to remove all records that were outside New York City (original dataset was for NY State brownfield records)
  * Used strip method combined with a slicer to ensure zipcodes were exactly five characters in length
   * ``df['zipcode'] = df['zipcode'].str[:5]``
  * Grouped status of the clean-up site using ``str.replace()`` method - data has different rating scale depending on funding of the clean up project so some descriptions could be merged.
  * Generated binary values using ``pd.get_dummies`` on health status:
  (1) Potential Threat
  (2) Maintenance Required - Continued Threat
  (3) Completed - Clean
  (4) Active - Significant Threat
  (5) Active - Mild Threat

