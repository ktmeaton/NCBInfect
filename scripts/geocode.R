# Geocoding a tsv column of "geographic_location" in R
# http://www.storybench.org/geocode-csv-addresses-r/

# Requires ggmap version 2.7 (custom Google API Key)
#register_google(key = 'AIzaSyAqtJ3uHrXes8rSwUqPp-_1MiP4M50s6Vc')

#load up the ggmap library
library(ggmap)

api_key <- 'AIzaSyAqtJ3uHrXes8rSwUqPp-_1MiP4M50s6Vc'


# Select the file from the file chooser
fileToLoad <- file.choose(new = TRUE)

# Read in the TXT data and store it in a variable 
data <- read.table(fileToLoad, stringsAsFactors = FALSE, header = TRUE, quote="",sep = '\t')

# get the address list
geo_locations = data$geographic_location


#define a function that will process googles server responses for us.
getGeoDetails <- function(address){   
  #use the gecode function to query google servers
  geo_reply = geocode(address, output='all', messaging=TRUE, override_limit=TRUE)
  #now extract the bits that we need from the returned list
  answer <- data.frame(lat=NA, long=NA, accuracy=NA, formatted_address=NA, address_type=NA, status=NA)
  answer$status <- geo_reply$status
  
  #if we are over the query limit - want to pause for an hour
  while(geo_reply$status == "OVER_QUERY_LIMIT"){
    print("OVER QUERY LIMIT - Pausing for 1 hour at:") 
    time <- Sys.time()
    print(as.character(time))
    Sys.sleep(60*60)
    geo_reply = geocode(address, output='all', messaging=TRUE, override_limit=TRUE)
    answer$status <- geo_reply$status
  }
  
  #return Na's if we didn't get a match:
  if (geo_reply$status != "OK"){
    return(answer)
  }   
  #else, extract what we need from the Google server reply into a dataframe:
  answer$lat <- geo_reply$results[[1]]$geometry$location$lat
  answer$long <- geo_reply$results[[1]]$geometry$location$lng   
  if (length(geo_reply$results[[1]]$types) > 0){
    answer$accuracy <- geo_reply$results[[1]]$types[[1]]
  }
  answer$address_type <- paste(geo_reply$results[[1]]$types, collapse=',')
  answer$formatted_address <- geo_reply$results[[1]]$formatted_address
  
  return(answer)
}











# Initialize the data frame
#geocoded <- data.frame(stringsAsFactors = FALSE)

#for(i in length(origAddress$geographic_location))
#{
#  origAddress$lon[i] <- NA
#  origAddress$lat[i] <- NA
#  origAddress$geoAddress[i] <- NA
#}

# Loop through the addresses to get the latitude and longitude of each address and add it to the
# origAddress data frame in new columns lat and lon
#for(i in 1:nrow(origAddress))
#{
#  if(is.na(origAddress$lon[i]) || is.na(origAddress$lat[i]))
#  {
#      result <- geocode(origAddress$geographic_location[i], output = "latlona", source = "google")
#      origAddress$lon[i] <- as.numeric(result[1])
#      if(is.na(result[1])) break
#      origAddress$lat[i] <- as.numeric(result[2])
#      origAddress$geoAddress[i] <- as.character(result[3])
#      Sys.sleep(2)
#  }
#}
# Write a CSV file containing origAddress to the working directory
#write.table(origAddress, "geocoded.txt", row.names=FALSE, sep = '\t', quote=FALSE)
