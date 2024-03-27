library(dplyr)
library(ggplot2)
library(lubridate)
library(stringr)

species <- "Humpback"
y.range <- c(0,20)   # Humpback: c(0,20), blue: c(0,5), gray: c(0,30)
workdir <- "C:/KAF/EntangledWhales/Working Group/RAMP framework/WW data/Processed_2020-03-17/"
infile <- paste0(workdir,"MBWW_",species," Whale_per_halfday_trip.csv")
infile <- "MBWW_Humpback Whale_per_halfday_trip.csv"

x <- read.csv(infile, stringsAsFactors = FALSE) %>% 
  mutate(Date = as.Date(Date), 
         year = year(Date), 
         month = month(Date), 
         day = day(Date), 
         day_interval = ifelse(day <= 15, 1, 16))

x.summ <- x %>% 
  group_by(year, month, day_interval) %>% 
  summarise(count = n(), 
            Whales_sum = sum(Whales, na.rm = TRUE), 
            Trips_sum = sum(Trips, na.rm = TRUE), 
            Whales_per_Trip = Whales_sum / Trips_sum) %>% 
  ungroup() %>% 
  mutate(Month_Half = paste(str_pad(month, 2, pad = "0"), str_pad(day_interval, 2, pad = "0"), 
                      sep = "."),
         year_fac = factor(year))


ggplot(x.summ, aes(x = Month_Half, y = Whales_per_Trip, fill = TRUE)) +
  geom_boxplot(outlier.shape=NA, show.legend = FALSE)
  ylim(c(-1, 20))

# Line
ggplot(x.summ, aes(x = Month_Half, y = Whales_per_Trip, colour = year_fac, group = year_fac)) + 
  geom_point() + 
  geom_path()
