
library(ggplot2)
library(ggthemes)

# Select the file from the file chooser
fileToLoad <- file.choose(new = TRUE)

world <- map_data("world")
world <- world[world$region != "Antarctica",] # intercourse antarctica

# Read in the tsv data and store it in a variable 
data <- read.table(fileToLoad, header = TRUE, quote="",sep = '\t')

# Create the consensus count column
data$consensus_count <- rep(NA, nrow(data))

# Get counts of unique lat and lon elements
for(i in 1:nrow(data))
{
  # Store lat and lon for current row
  current_lat <- data$consensus_lat[i]
  current_lon <- data$consensus_lon[i]
  # Store count of current lat and lon occurring in data frame
  count_lat <- length(which(data$consensus_lat == current_lat))
  count_lon <- length(which(data$consensus_lon == current_lon))
  # populate consensus count column only if lat and lon counts agree
  if(count_lat == count_lon)
  {
    data$consensus_count[i] <- count_lat
  }
  else
  {
    minimal_count <- min(count_lat, count_lon)
    data$consensus_count[i] <- minimal_count
  }
}

distinct_data <- distinct(data, geographic_location, consensus_lat, consensus_lon, Pandemic, Established, consensus_count)





##########################################
#                PLOTTING                #
##########################################

#-------------------#
#  Plot by Pandemic #
#-------------------#
# Null ggplot
gg <- ggplot()
# Base world map
gg <- gg + geom_map(data=world, map=world,
                    aes(x=long, y=lat, map_id=region),
                    color="white", fill="#7f7f7f", size=0.05, alpha=2/4)
# Add data points
gg <- gg + geom_point(data=distinct_data, 
                      aes(x=consensus_lon, y=consensus_lat, size=consensus_count, 
                          fill=Pandemic), shape=21, alpha=0.8)

# Tableau color theme
#gg <- gg + scale_color_tableau()
# Theme: strip background, reposition legend
gg <- gg + theme_map()
gg <- gg + theme(strip.background=element_blank())
#gg <- gg + guides(fill=FALSE)
gg <- gg + guides(size=FALSE)
gg <- gg + ggtitle(expression(paste("Global distribution of ", 
                                    italic("Yersinia pestis"), " whole genome sequencing projects.")), 
                   subtitle = "Visualized by Pandemic")
gg <- gg + theme(plot.title = element_text(hjust = 0.5, face = "bold", size = 12))
gg <- gg + theme(plot.subtitle = element_text(hjust = 0.5, size = 8))
ggsave("testplot.pdf", device='pdf', width=10.185, height=5.67, dpi=600)



