#!/usr/bin/env Rscript
library(ggplot2)
d <- read.csv("./in.csv", head=FALSE)
pdf(file="fits.pdf")
print(
    ggplot(data=d) + 
    geom_point(aes(V1, V2, color=V5)) + 
    geom_line(aes(V1, V4, color=V5)) + 
    facet_wrap(~V5, ncol=1, scales="free")
)
dev.off()
