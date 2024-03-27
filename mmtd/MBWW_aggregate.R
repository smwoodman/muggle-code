library(dplyr)
library(ggplot2)
library(lubridate)

x <- read.csv("MBWW_Humpback Whale_per_halfday_trip.csv", stringsAsFactors = FALSE) %>% 
  mutate(Date = as.Date(Date), 
         year = year(Date), 
         month = month(Date), 
         day = day(Date), 
         day_interval = ifelse(day <= 15, 1, 2))


x.summ <- x %>% 
  group_by(year, month, day_interval) %>% 
  summarise(count = n(), 
            Whales_sum = sum(Whales, na.rm = TRUE), 
            Trips_sum = sum(Trips, na.rm = TRUE), 
            Whales_per_Trip = Whales_sum / Trips_sum) %>% 
  ungroup() %>% 
  mutate(month_day = paste(sprintf("%02d", month), day_interval, sep = "_"), 
         year_fac = factor(year))


# Facets
ggplot(x.summ, aes(x = month_day, y = Whales_per_Trip)) + 
  geom_point() + 
  facet_wrap(vars(year), nrow = 3)

# Line
ggplot(x.summ, aes(x = month_day, y = Whales_per_Trip, colour = year_fac, group = year_fac)) + 
  geom_point() + 
  geom_path()
  

