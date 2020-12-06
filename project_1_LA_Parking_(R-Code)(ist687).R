#LA Tickets for 2018 - Applied Data Science Final Project
library(gdata,warn.conflicts = FALSE, quietly = TRUE)
library(ellipse, warn.conflicts = FALSE, quietly = TRUE)
library(RColorBrewer,warn.conflicts = FALSE, quietly = TRUE)
library(sqldf, warn.conflicts = FALSE, quietly = TRUE)
library(ggplot2, warn.conflicts = FALSE, quietly = TRUE)
library(reshape2, warn.conflicts = FALSE, quietly = TRUE)
library(ggmap, warn.conflicts = FALSE, quietly = TRUE)
library(tidyr, warn.conflicts = FALSE, quietly = TRUE)

library(gdata,warn.conflicts = FALSE, quietly = TRUE)
df0 <- read.csv("C:/Users/17574/Desktop/Data/streetsweeping-citations-2018-clean.csv")

apply(apply(df0,2,is.na),2,sum)  #confirm no NAs....
# str(df0)
#colnames(df0)
# head(df0,1)
df1 <- data.frame(df0) ##594546 obs. of  27 variables:
#Notes.1 ==> violation.fine all $73; all street cleaning; meter.id=dont use all same meter
#Note.2==> when merge dataframe columns are reordered....
#DATA TRANSFORMATION - add numeric codes for scatter+melt & correlations
    # f.make.numeric.id <-function(v.name)  ##FIX - v.name
    #     # { df.unique.temp <- data.frame(unique(df1$v.name))
    #     # level.rows <- c(1:nrow(df.unique.temp))  #fill in blanks to add a group size variable
    #     # df.unique.temp <-cbind(df.unique.temp ,level.rows)
    #     # colnames(df.unique.temp) <- c("v.name",paste("v.name",".2"))
    #     # df2 <- merge(x=df1, y=df.unique.temp, by ="v.name", all.x=TRUE)
    #     # remove(df.unique.temp)  }
#NUMBERIC IDs -------------FOR correlation & scatterplots--------------------------------
c.names <- colnames(df1)
c.names.2 <- gsub("\\.","",c.names)  #remove dots for sqldf
c.names.2
colnames(df1)<-c.names.2
remove(c.names.2)
#route.ID  ==>levels=674
df.temp <- data.frame(unique(df1$routeid))
level.rows <- c(1:nrow(df.temp))  #fill in blanks
df.temp <-cbind(df.temp ,level.rows) #lookup table
colnames(df.temp) <- c("routeid",paste("routeid2"))
df1 <- merge(x=df1, y=df.temp, by ="routeid", all.x=FALSE)
#plate.state  ==> 7levels=73
df.temp <- data.frame(unique(df1$platestate))
level.rows <- c(1:nrow(df.temp))  #fill in blanks
df.temp <-cbind(df.temp ,level.rows) #lookup table
colnames(df.temp) <- c("platestate",paste("platestate2"))
df1 <- merge(x=df1, y=df.temp, by ="platestate", all.x=FALSE)
#car.make ==> levels=62
df.temp <- data.frame(unique(df1$carmake))
level.rows <- c(1:nrow(df.temp))  #fill in blanks
df.temp <-cbind(df.temp ,level.rows) #lookup table
colnames(df.temp) <- c("carmake",paste("carmake2"))
df.carid.master <-df.temp
df1 <- merge(x=df1, y=df.temp, by ="carmake", all.x=FALSE)
write.csv(df.carid.master, "df.carid.master.csv") #spped up normalization
#car.bodystyle  ==> levels=12
df.temp <- data.frame(unique(df1$carbodystyle))
level.rows <- c(1:nrow(df.temp))  #fill in blanks
df.temp <-cbind(df.temp ,level.rows) #lookup table
colnames(df.temp) <- c("carbodystyle",paste("carbodystyle2"))
df1 <- merge(x=df1, y=df.temp, by ="carbodystyle", all.x=TRUE)
#car.color  ==>levels=16
df.temp <- data.frame(unique(df1$carcolor))
level.rows <- c(1:nrow(df.temp))  #fill in blanks
df.temp <-cbind(df.temp ,level.rows) #lookup table
colnames(df.temp) <- c("carcolor",paste("carcolor2"))
df1 <- merge(x=df1, y=df.temp, by ="carcolor", all.x=TRUE)
#issue.address ==>levels=292164
df.temp <- data.frame(unique(df1$issueaddress))
level.rows <- c(1:nrow(df.temp))  #fill in blanks
df.temp <-cbind(df.temp ,level.rows) #lookup table
colnames(df.temp) <- c("issueaddress",paste("issueaddress2"))
df1 <- merge(x=df1, y=df.temp, by ="issueaddress", all.x=TRUE)
head(df1,3)
#------CORRELATION----ELLIPSIS----------------------------------
library(ellipse, warn.conflicts = FALSE, quietly = TRUE)
library(RColorBrewer,warn.conflicts = FALSE, quietly = TRUE)
my_colors <- brewer.pal(11, "Spectral")  #build color panel
my_colors = colorRampPalette(my_colors)(100)
#x <- data.frame(colnames(df1))   #use colnames to get IDs
df.cor <-data.frame(df1[,c(11,12,13,15,16,18,19,26:33)]) 
cor.df1 <- cor(df.cor)   #build corrleation of data
ord <- order(df.cor[1,])  # Order the correlation matrix
data_ord = cor.df1[ord, ord]
plotcorr(data_ord , col = my_colors[data_ord * 50 + 30] , mar = c(1, 1, 1, 1))
#write.csv(round(cor.df1,2), "project.csv"): found coordinate issues had to fix
#-----MELT HISTROGRAM-----------------------------
library(sqldf, warn.conflicts = FALSE, quietly = TRUE)
library(ggplot2, warn.conflicts = FALSE, quietly = TRUE)
library(reshape2, warn.conflicts = FALSE, quietly = TRUE)
library(ggmap, warn.conflicts = FALSE, quietly = TRUE)
us <-map_data("state")
suppressWarnings(require(RColorBrewer)) #install.packages("RColorBrewer")
ggplot(data = melt(df1[,c(11,12,13,15,16,18,19,26:33)]), mapping = aes(x = value)) + 
  geom_histogram(bins=12)+ facet_wrap(~variable, scales = "free")
#------------LA REVENUE MAP------------------------------
state <-map_data("state")
route.df1 <- sqldf('select routeid2, issueaddresslat as long,issueaddresslon as lat,
                   SUM(violationfineamt) as fine from df1 group by routeid2')
RevenueGroup <- c(1:nrow(route.df1))  #fill in blanks to add a group size variable
state <- c(1:nrow(route.df1))     #write.csv(route.df1, "Route_Fine.csv")
longnew <-c(1:nrow(route.df1))
latnew <-c(1:nrow(route.df1))
route.df1 <-cbind(route.df1,RevenueGroup)   #Gadd state full name back for mapping please
route.df1 <-cbind(route.df1,state)
route.df1 <-cbind(route.df1,longnew)
route.df1 <-cbind(route.df1,latnew)
remove(RevenueGroup,state,latnew, longnew)  #----ADD FIXING OF LAT/LON CONVERSION HERE
#str(route.df1)
# there are both bad and blank coordinates; I am just grouping for revenue diagram
#old values = -137.9131, 27.51751
#new values = -118.24532, 34.05349
n <-1 
while (n <= nrow(route.df1))
  {  route.df1[n,7]= round(route.df1[n,2],4)
     route.df1[n,8]= round(route.df1[n,3],5)
     #route.df1[n,2]= 0
     #route.df1[n,3]= 0
     n <- n+1                 #fixing some bad lat long positions - moving over from ocean
  }                               #REVENUE DOT PLOT FIXING LAT/LONG
n <- 1
while (n <= nrow(route.df1))
  { #if (route.df1[n,7]== -137.9131) { baddates <- baddates+1 }
    if (route.df1[n,7]== -137.9131)  {route.df1[n,2]= -118.24532  } 
    if (route.df1[n,8]== 27.51751)   {route.df1[n,3]= 34.05349  }
    if (route.df1[n,7]== 0)         {route.df1[n,2]= -118.24532  } 
    if (route.df1[n,8]== 0)       {route.df1[n,3]= 34.05349  }
    n <- n+1  }
    #colnames(route.df1) <- c("routeid2","long","lat","fine","grpsize","state","fix")
#head(route.df1)
route.df1$state <- "california"   #expand to get whole view on R windows
route.df1$RevenueGroup <- cut(route.df1$fine,           #make buckets for mapping
                    breaks = c(-Inf, 50000, 75000, 150000, 200000, 300000, Inf), 
  labels = c("0-50,000","50,001-75,000","75,001-150,000","150,001-200,000","200,000-300,000","300+"), 
                         right = FALSE)
mycolors <- brewer.pal(6, "Accent")   #head(df4,1)
names(mycolors) <-levels(route.df1$grpsize)  #getting the color names
ggplot(route.df1, aes(map_id=state)) + 
  expand_limits(x=route.df1$long, y=route.df1$lat) + coord_map()+
  geom_map(map = us, fill="black", color="red" ) + geom_point(data=route.df1,
                    aes(x=long,y=lat, color=RevenueGroup, size=RevenueGroup ))+
  #stat_density2d(data=route.df1,aes(x=long,y=lat), geom="density_2d")+ 
  scale_colour_manual( values=mycolors) +  #name="Color",
  ggtitle("2018 Los Angeles Sweep Fine Revenue by 674 Routes")
      #nice revenue map - had some coordinate issues fixed
#================================================================================
#-------------->>>>> HEATMAP WORK  <<<<========================
#GET A GRID OF THE CARS AS NEED TO MAKE NUMERIC THEN NORMALIZE 0-1
# 
#       head(df1$carmake)
#       hist(df1$carmake2)
#       nrow(table(df1$violation.fine.amt))
#       hist(df1$violation.fine.amt)
#       df.temp <- data.frame(tapply(df1$carmake2, df1$carmake,min))
#       unique(df1$carmake)
#       tapply(df1$carmake2, df1$carmake,min)

car.df1 <- data.frame(sqldf('select carmake,SUM(carmake2) as CarQty 
                            from df1 group by carmake') )
#explore & performing grouping/normalization in Excel
#would have done in R but running out of time on delivery to team! - doing rest in R
      #write.csv(df.carid.master, "df.carid.master.csv") #spped up normalization 
car.df2 <- read.xls("C:/Users/Brian P Hogan Jr/Desktop/IST687+Final+Project+Car+Group+Normalize.xlsx",
                perl="C:/strawberry/perl/bin/perl.exe", verbose=TRUE)
car.df2
df.temp <- data.frame(car.df2)
#head(df.temp)
              # carqty <- c(1:nrow(df1))
              # cargroupnormalize <- c(1:nrow(df1))
              # df2.heat <-cbind(df1 ,carqty,cargroup,cargroupnormalize)
              # df2.heat$carqty <- -199
              # df2.heat$cargroup <- -199
              # df2.heat$cargroupnormalize <- -199
#============================================================
#FINDING===> WAS USING 2 DIFFERENT TABLE IDS PULLED AT DIFFERETN TIME PIONTS!
#===> R resorts data on subsequent data merges
#==================================================================
#fixed the merge - was using 2 different tables w differing assignment values..
df2.heat <-merge(x=df1, y=df.temp, by=c("carmake2","carmake"), all.x = TRUE)
#head(df2.heat,10)
remove(car.df1,car.df2)
cargroupname <- c("Dom.EconY","Dom.EconN","Intl.EconY","Intl.EconN","Fancy","Trucks")
cargroup<- c(1,2,3,4,5,6)
df.car.group <- data.frame(cargroup, cargroupname)
df.car.group
df2.heat <-merge(x=df2.heat, y=df.car.group, by="cargroup", all.x = TRUE)
head(df2.heat)
#=================>>>>>remove(df.car.group)
#Heatmap
#car type grouping - 0-1 scaling was done in Excel to spped up as had issue mergeing
#issue wasn't mergeing but was 2 different data tables pulled at different time points
colnames(df2.heat)
# table(df2.heat$issuetimebin)
# hist(df2.heat$cargroupnormalize)  

#Step 4 Heatmap---using normalization approach between 0-1 as didnt' want negative scale
head(df2.heat)
df3.heat <- data.frame(df2.heat[,c(9,12,13,15,17,1,37,36)])
head(df3.heat,10)
max(df3.heat$issuetimebin)
range(df3.heat$issuetimebin)
df3.heat$timebin.z <- (df3.heat[,5]-min(df3.heat$issuetimebin))/
  (max(df3.heat$issuetimebin)-min(df3.heat$issuetimebin))
df3.heat$cargrp.z <- (df3.heat[,6]-min(df3.heat$cargroup))/
  (max(df3.heat$cargroup)-min(df3.heat$cargroup))
# head(df3.heat,1)
# length(df3.heat)

dftemp<-data.frame(df3.heat) #    <----switch to dataframe w no dots in it
str(dftemp) 
#============================================================
#hwat I really want is by car groups........       
cargrp <- sqldf('select issuemonth as month, issueweekday as day,
        cargroupname , cargroupnormalize as zscore from dftemp ')

# head(cargrp)
# str(cargrp)
# table(cargrp$cargroupname)

#Comparison to learn if need to transform data to interpret better in heatmap
ggplot(data = melt(df3.heat[,c(8:10)]), mapping = aes(x = value)) + geom_histogram(bins=20)+
  facet_wrap(~variable, scales = "free") +
  ggtitle("Checking out for heat map")
#str(df3.heat)

#install.packages("tidyr")     #CLASS SLACK HELP was INVALUABLE !
library(tidyr)
#Abundance = grouping of all air quality factor values 0-1
#Felt Square Root Transformation did help with graph read but could vary by person
df4.heat <- gather(data = cargrp, key = Class, value= Abundance,-c(1:3))
df4.heat$Sqrt.Abundance <- sqrt(df4.heat$Abundance)
head(df4.heat,4)
str(df4.heat)
                                                    #y=Class
heat.reg <-ggplot(data=df4.heat, mapping= aes(x=day,y=cargroupname,fill=Abundance))+
  geom_tile() + xlab(label="Month/Day") + ylab(label="ticket") +
  ggtitle("Super Luxury Cars e.g. Rolls Royces & Bentleys are towed Least of All Others
      but 3% of Total Cars or 21.6k/7.6M Towes in 2018") +
  theme(axis.text.x = element_text(size=8,angle = 90, hjust = 1)) +
  facet_grid(~ month, switch = "x", scales="free_x", space="free_x")
heat.reg #non transformed data

# heat.reg <-ggplot(data=df4.heat, mapping= aes(x=day,y=cargroupname,fill=Sqrt.Abundance))+
#   geom_tile() + xlab(label="Month/Day") + ylab(label="ticket") +
#   ggtitle("Super Luxury Cars e.g. Rolls Royces & Bentleys are towed Least of All Others
#           but 3% of Total Cars or 21.6k/7.6M Tows in 2018") +
#   theme(axis.text.x = element_text(size=8,angle = 90, hjust = 1)) +
#   facet_grid(~ month, switch = "x", scales="free_x", space="free_x")
# heat.reg #non transformed data

#--------------------------machine learning

#HOUSE KEEPING--------------------------------
remove(df0, df1,df.temp, cor.df1, route.income.df1, df.carid.master)  



