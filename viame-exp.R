library(tidyverse)

viame.colnames <- c(
  "Detection or Track-id", 
  "Video or Image Identifier", 
  "Unique Frame Identifier", 
  "TL_x", "TL_y", "BR_x", "BR_y", 
  "Detection or Length Confidence", 
  "Target Length (0 or -1 if invalid)",
  paste(rep(c("class", "confidence"), 10), 
        str_pad(rep(1:10, each = 2) , 2, pad = "0"), 
        sep = "_")
)

x.orig <- read_csv("C:/Users/sam.woodman/Downloads/clone-of-dir0001.csv", 
              skip = 2, col_names = viame.colnames, 
              col_types = "iciiiiidi????????????????????")

x <- x.orig %>% 
  filter(`Detection or Length Confidence` > 0.51) %>% 
  select(`Detection or Track-id`:`confidence_01`)


y.orig <- read_csv("C:/Users/sam.woodman/Downloads/clone-of-dir0002-samtest.csv", 
                   skip = 2, col_names = viame.colnames, 
                   col_types = "iciiiiidi????????????????????")
y.conf.custom <- data.frame(
  class_01     = "coppapssc", 
  threshold_01 = 0.48
)

y <- y.orig %>% 
  select(`Detection or Track-id`:`confidence_01`) %>% 
  left_join(y.conf.custom, by = join_by(class_01)) %>% 
  mutate(conf = replace_na(threshold_01, 0.29)) %>% 
  filter(`Detection or Length Confidence` > conf)
