# Geocoding a tsv column of "geographic_location" in R
# http://www.storybench.org/geocode-csv-addresses-r/

setwd("C:\\Users\\ktmea\\Programs\\NCBInfect\\database")

#load ggmap
library(ggmap)

#AIzaSyAqtJ3uHrXes8rSwUqPp-_1MiP4M50s6Vc

# Select the file from the file chooser
#fileToLoad <- file.choose(new = TRUE)

# Read in the CSV data and store it in a variable 
#origAddress <- read.table(fileToLoad, stringsAsFactors = FALSE, header = TRUE, quote="",sep = '\t')

#geoAddress <- data.frame(strainsAsFactors = FALSE)


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
for(i in 1:nrow(origAddress))
{
  if(is.na(origAddress$lon[i]) || is.na(origAddress$lat[i]))
  {
      result <- geocode(origAddress$geographic_location[i], output = "latlona", source = "google")
      origAddress$lon[i] <- as.numeric(result[1])
      if(is.na(result[1])) break
      origAddress$lat[i] <- as.numeric(result[2])
      origAddress$geoAddress[i] <- as.character(result[3])
      Sys.sleep(5)
  }
}
# Write a CSV file containing origAddress to the working directory
write.table(origAddress, "geocoded.txt", row.names=FALSE, sep = '\t', quote=FALSE)
