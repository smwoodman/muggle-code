library(magick)
library(lubridate)

path.reconyx <- "C:/Users/sam.woodman/Downloads/Reconyx/"
list.files(path.reconyx)

# Each have some number of reconyx folders
path.build <- list.files(file.path(path.reconyx, "Build"), full.names = TRUE)
path.demo <- list.files(file.path(path.reconyx, "Demo"), full.names = TRUE)

length(list.files(path.build))
length(list.files(path.demo))

reconyx_animate <- function(path_imgs, file_out, fps = 20) {
  # https://www.nagraj.net/notes/gifs-in-r/
  imgs <- list.files(path_imgs, full.names = TRUE)
  print(paste("reading", as.character(lubridate::now())))
  img_list <- lapply(imgs, image_read)
  
    # Error: Image pointer is dead. You cannot save or cache image objects between R sessions.
  # print(paste("saving reading", as.character(lubridate::now())))
  # saveRDS(img_list, 
  #         file = file.path(path.reconyx, paste0(file_out, "img_read_list.rds")))
  
  ## join the images together
  print(paste("joining", as.character(lubridate::now())))
  img_joined <- image_join(img_list)
  
  ## animate at 'fps' frames per second
  print(paste("animating", as.character(lubridate::now())))
  img_animated <- image_animate(
    img_joined, fps = fps, loop = 0, optimize  = TRUE
  )
  
  ## view animated image
  # x <- img_animated
  
  print(paste("writing", as.character(lubridate::now())))
  image_write(image = img_animated, path = file.path(path.reconyx, file_out))
}

# img.build <- unlist(lapply(path.build, list.files, full.names = TRUE))
# img.build.list <- lapply(img.build, image_read)
# img.build.joined <- image_join(img.build.list)
# img.build.animated <- image_animate(img.build.joined, fps = 2)
# img.build.animated

reconyx_animate(path.build, "CS-202324-build.gif")
reconyx_animate(path.demo, "CS-202324-demo.gif")

# reconyx_animate(path.demo[2], "CS-202324-demo2.gif")
