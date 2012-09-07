#!/usr/bin/env Rscript
library(ggplot2)
library(stringr)
library(gridExtra)
library(reshape2)
args <- commandArgs(trailingOnly = TRUE)
Y = read.delim(file=args[1], sep=",", header=TRUE)
summary(Y)
Ym = melt(Y, id.vars=c("date", "ts"))
png(filename = paste(sep="", args[1],"_grid.png"), width = 1000, height = 900, units = 'px')
  print(
    ggplot(data=Ym) +
	geom_line(aes(ts,value) , color="orange") + 
    facet_wrap( ~ variable, scale="free" ) +
    opts(legend.position = 'none',
       panel.background = theme_rect(fill = "#545454"),
       panel.grid.major = theme_line(colour = "#757575"),
       panel.grid.minor = theme_line(colour = "#757575"),
       title = args[2])
  )
dev.off()
png(filename = paste(sep="",args[1],".png"), width = 1000, height = 900, units = 'px')
  print(
    ggplot(data=Ym) +
	geom_line(aes(ts,value,color=variable)) + 
    opts(panel.background = theme_rect(fill = "#545454"),
       panel.grid.major = theme_line(colour = "#757575"),
       panel.grid.minor = theme_line(colour = "#757575"),
       title = args[2])
  )
dev.off()
