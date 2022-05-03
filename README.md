# Geo Location Extender
“Die Post” provides their address-data free accessible to use. Unfortunately, the coordinates of each address are not provided in the free version.
To enrich the postal addresses with <geo-location> information, we use a WebAPI which based on street, street number, zip, locality inoformation provides latitude and longitude data.
The enriched data is stored in a GeoJson format at the config file defined location and file name.

# Usage
Install the developed package within a new environment from the geolocation_extender folder: 
- `pip install -e .`

The package behavior is controlled by a given configuration file as well as the input/ouput files and their location
and name. If no value added to the <geolocation_repository> a dummy WebAPI sill be used.
- `/geolocation_extender/config/program_config.json`

The developed package can be run via the following command:
- `geo_loc_extend`

