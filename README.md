# Machine Learning - Real Estate Valuations

# OVERVIEW

* The datasets created and utilized for our analysis and visualizations took data on New York City (crime, education, environment, socio-economic, subway-access) filtered by zipcode. After initial exploratory analysis and cleaning, we decided to move foward with a Linear Regression and Random Forest Machine Learning Models.

# EXTRACT
* Technologies Used: 
  * Back End: Pandas, sql-alchemy, numpy, sklearn.preprocessing [oneHotEncoder], scipy.stats, geopy[distance], geopy.geocoders[Nominatim], geopy.exc[GeoCoderTimedOut], geopy.extra.rate_limiter[RateLimiter], geopandas, plotly_express, tqdm, tqdm.pandas(), sklearn.neighbors, tqd


Group Members: Stephen Brescher, Shadee Tabassi, Alison Sadel, Manny Mejia



import plotly_express as px
from tqdm import tqdm
from tqdm._tqdm_notebook import tqdm_notebook
from datetime import datetime
tqdm.pandas()
import sklearn.neighbors
