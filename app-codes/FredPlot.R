#!/usr/bin/Rscript --vanilla
require(ggplot2)
require(plyr)
pdf(NULL)

args = commandArgs(trailingOnly=TRUE)

df <- read.csv(args[1])
df$WaitTime = as.numeric(as.POSIXlt(df$Start,format="%Y-%m-%dT%H:%M:%S") -
               as.POSIXlt(df$Submit,format="%Y-%m-%dT%H:%M:%S"))/60
df$State = factor(df$State)
df$exp = paste0("E",df$exp)

df2=ddply(df, .(exp), summarize, JobIDRaw = JobIDRaw, 
          JobIDRel = seq(length(exp)))

df$JobIDRel = df2$JobIDRel

p = ggplot(df, aes(JobIDRel, WaitTime, color=State)) +
    geom_point(size=.5) + 
    facet_wrap(~exp, ncol=3, scales="free") + 
    theme_bw()+
    xlab("Job ID (per experiment)") +
    ylab("Wait Time (in minutes)") +
    guides(color = guide_legend(override.aes = list(size = 5))) +
    theme(legend.position="top") 

ggsave(file.path("./FredPlot.pdf"), p,
       device = cairo_pdf, width = 24, height = 18, units = "cm")
       