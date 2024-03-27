# Code to calculate the area of the each grid cell that falls entirely or partially 
#   in the polygon defined by the points in eez_Guatemala.dat.
# The centers of the grid cells are spaced 0.25 deg apart, i.e. at (-92,12), (-92.25,12), etc.
# By Sam Woodman for Paul Fiedler, May 2019

#------------------------------------------------------------------------------
# Install packages (will only need to run once)
install.packages(c("maps", "sf"))

# Load packages
library(sf)

# Reference map for plotting
map.base <- st_geometry(st_as_sf(maps::map('world', plot = FALSE, fill = TRUE)))


#------------------------------------------------------------------------------
# Read in study area polygon; crs = 4326 refers to WGS 84 coordinate reference system
x <- read.csv("eez_Guatemala.dat", header = FALSE)
x.poly <- st_sfc(st_polygon(list(matrix(c(x[, 1], x[, 2]), ncol = 2))), crs = 4326)

# Create grid; first make polygon to define grid extent
y.poly <- st_sfc(st_polygon(list(matrix(
  c(-95, -90, -90, -95, -95, 10, 10, 15, 15, 10), ncol = 2)
)), crs = 4326)

y.grid <- st_sf(
  idx = 1:441,
  geometry = st_make_grid(y.poly, cellsize = 0.25, offset = c(-95.125, 9.875)), 
  crs = 4326, agr = "identity"
)

# Get centroids of the grid to ensure they are correct; ignore warning message
y.cent <- st_centroid(st_geometry(y.grid))
y.cent.df <- data.frame(idx = y.grid$idx, do.call(rbind, y.cent))
head(y.cent.df)

# Get intersection of grid and study area polygon
yx.int <- st_intersection(y.grid, x.poly)


#------------------------------------------------------------------------------
# Visualize
plot(st_geometry(y.grid), axes = TRUE)
plot(x.poly, add = TRUE, border = "red")
plot(y.cent, add = TRUE, col = "orange", pch = 19, cex = 0.3)
plot(map.base, add = TRUE, col = "tan", border = NA)

plot(st_geometry(yx.int), axes = TRUE, border = "green")
plot(map.base, add = TRUE, col = "tan", border = NA)


#------------------------------------------------------------------------------
# Calculate areas of grid cells that are within study area polygon
yx.int.area.m2 <- as.numeric(st_area(yx.int))
yx.int.area.km2 <- yx.int.area.m2 / 1e+06
yx.int.area.km2

yx.int.area.df <- data.frame(idx = yx.int$idx, yx.int.area.m2, yx.int.area.km2)

# Create data frame with grid centroids and area
df.out <- merge(y.cent.df, yx.int.area.df, by = "idx")
names(df.out) <- c("idx", "lon", "lat", "area_m2", "area_km2")
write.csv(df.out, row.names = FALSE, file = "eez_Guatemala_area_forPaul.csv")


# Visualize - sanity check
temp <- st_sf(yx.int.area.km2, geometry = st_geometry(yx.int))
plot(temp, axes = TRUE, key.length = 1, main = "eez Guatemala area (km2)")
#------------------------------------------------------------------------------
