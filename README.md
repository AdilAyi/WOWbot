# WOWbot
 Msc Thesis Adil Ayi - TU Delft

Columns definition of the final database csv:

| Field              | Definition                                              | Datatype       |
|--------------------|---------------------------------------------------------|----------------|
| Station ID         | Unique identification of the weather station            | Integer        |
| Position           | Geographical coordinates of the weather station         | Decimal        |
|                    | (Lat, Lon)                                              |                |
| Elevation          | Height of the weather station above sea level           | Integer        |
|                    | (meters)                                                |                |
| Time zone          | Time zone of the weather station                        | String         |
| Active station     | Indicates whether the weather station is active         | Boolean        |
| Download?          | Indicates whether downloading of data is allowed        | Boolean        |
| Website            | URL of the website of the weather station               | String (URL)   |
| Station motivation | Reason why the weather station was set up               | String         |
| Official station   | Indicates whether the weather station is officially recognized | Boolean |
| Organization       | Name of the organization that manages the weather station | String         |
| Location           | Address information of the weather station              | Categorical    |
| Air temperature    | Indicates whether air temperature is measured           | Categorical    |
| Precipitation      | Indicates whether precipitation is measured             | Categorical    |
| Wind               | Indicates whether wind speed and direction are measured | Categorical    |
| Urban area         | Indicates whether the weather station is located in an urban area | Categorical |
| Observation hours  | Period during which the weather station makes observations | Categorical |
| Star rating        | Rating of the weather station on a scale of 0 to 5 stars (more information in chapter 3.1) | Integer |
| Description        | Description of the weather station                      | String         |
|                    | (Free Text)                                             |                |
| Additional         | Additional information about the weather station        | String         |
|                    | (Free Text)                                             |                

