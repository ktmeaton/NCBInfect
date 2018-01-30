
library(ggplot2)

# Select the file from the file chooser
fileToLoad <- file.choose(new = TRUE)

# Read in the CSV data and store it in a variable 
geocode_input <- read.table(fileToLoad, stringsAsFactors = FALSE, header = TRUE, quote="",sep = '\t')

#Using GGPLOT, plot the Base World Map
mp <- NULL
mapWorld <- borders("world", colour="gray50", fill="gray50") # create a layer of borders
mp <- ggplot() +   mapWorld

#Now Layer the cities on top
mp <- mp + geom_point(aes(x=geocode_input$lat, y=geocode_input$lon) ,color="blue", size=1) 


