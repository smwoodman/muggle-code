load("DemeRelate_Wcoast4.Rdata")
library(tidyverse)

# gdata1b <- data4 %>% 
#   mutate(across(starts_with("Loc"), str_replace_all, "G","1"), 
#          across(starts_with("Loc"), str_replace_all, "A","2"), 
#          across(starts_with("Loc"), str_replace_all, "T","3"), 
#          across(starts_with("Loc"), str_replace_all, "C","4"), 
#          across(starts_with("Loc"), as.numeric))


locus.names <- unique(sapply(str_split(names(data4[, 3:ncol(data4)]), "[.]"), function(i) i[1]))

allele.count <- sapply(locus.names, function(i) {
  x <- data4 %>% select(starts_with(paste0(i, ".")))
  if (ncol(x) != 2) stop("More than two columns selected for ", i)
  length(sort(unique(unlist(x))))
})
table(allele.count, useNA = "always")


gdata1.fac.list <- lapply(locus.names, function(i) {
  x <- data4 %>% select(starts_with(paste0(i, ".")))
  if (ncol(x) != 2) stop("More than two columns selected for ", i)
  x.uniq <- sort(unique(unlist(x)))
  if (length(x.uniq) > 9) warning("More than nine alleles for ", i)
  
  data.frame(lapply(x, factor, levels = x.uniq))
})

gdata1.fac <- bind_cols(gdata1.fac.list)
gdata1.num <- data.frame(lapply(gdata1.fac, as.integer))
