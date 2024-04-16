library(rnaturalearth)
library(rnaturalearthhires)
library(ggplot2)
library(sf)

world <- ne_countries(scale = "large", returnclass = "sf")
class(world)

g <- ggplot(data = world) +
  geom_sf() + 
  coord_sf(xlim = c(-85.0, -50), ylim = c(-70, -50), 
           crs = st_crs(4326), expand = FALSE)
g

ggsave(
  "C:/Users/sam.woodman/Downloads/g.png", 
  g, width = 25, height = 20, bg = "white"
)
