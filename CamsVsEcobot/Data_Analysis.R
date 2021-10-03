ALL <- read.table("12am_2.csv", header=TRUE)
# data description:
# 1. date
# 2. device_id - id of land station (single 30th is used)
# 3. land_pm25 - land value of pm25 pollutant (12:00, 30th station)
# 4. cams_id - satellite id of area for 30th station
# 5. cams_pm25 - satellite value of pm25 (same) pollutant (12:00, 30th station)
# 6. land_pm10 - land value of pm10 (another) pollutant (12:00, 30th station)
# 7. land_temperature - land value of temperature (12:00, 30th station)
# 8. land_humidity - land value of humidity (12:00, 30th station)

head(ALL)
SAT <- ALL$cams_pm25

### NORMALITY

summary(SAT)
hist(SAT, breaks=seq(0, 48, by=1))
shapiro.test(SAT) # rejected
ks.test(SAT, "pnorm", mean=mean(SAT), sd=sd(SAT)) # also rejected

ALL <- ALL[1:100,] # let's try a small chunk
SAT_1 <- ALL$cams_pm25
summary(SAT_1)
hist(SAT_1, breaks=seq(0, 37, by=0.5))
shapiro.test(SAT_1) # rejected
ks.test(SAT_1, "pnorm", mean=mean(SAT_1), sd=sd(SAT_1)) # accepted

### OUTLIERS

boxplot(SAT_1) # for some reason it's rendered at the end of pdf

outliers <- boxplot.stats(SAT_1)$out # 3 outliers
outliers
length(SAT_1)
ALL <- subset(ALL, !(SAT_1 %in% outliers)) # remove them
SAT_1 <- ALL$cams_pm25 
length(SAT_1) # 3 items removed

lower_bound = median(SAT_1) - 3 * mad(SAT_1, constant=1) # Hampel test
upper_bound = median(SAT_1) + 3 * mad(SAT_1, constant=1)
length(SAT_1)
ALL <- subset(ALL, (SAT_1 >= lower_bound & SAT_1 <= upper_bound))
SAT_1 <- ALL$cams_pm25  
length(SAT_1) # 4 more items removed

lower_bound = quantile(SAT_1, 0.25) - 1.5 * IQR(SAT_1) # IQR test
upper_bound = quantile(SAT_1, 0.75) + 1.5 * IQR(SAT_1)
length(SAT_1)
ALL <- subset(ALL, (SAT_1 >= lower_bound & SAT_1 <= upper_bound))
SAT_1 <- ALL$cams_pm25  
length(SAT_1) # no more items deleted

### EQUALITY OF MEANS

t.test(ALL$land_pm25, ALL$cams_pm25) # rejected

### CORRELATION

ks.test(ALL$land_pm25, ALL$cams_pm25, alternative = "two.sided") # rejected

wilcox.test(ALL$land_pm25, ALL$cams_pm25) # rejected

cor.test(ALL$land_pm25, ALL$cams_pm25, method="spearman") # rejected

### REGRESSION

Y <- ALL$cams_pm25 # satelite pollutant value (pm25)
X1 <- ALL$land_pm25 # land pollutant value (same, pm25)

summary(lm(Y ~ X1)) # both coefficients are zero, it's strange

X2 <- ALL$land_pm10 # another land pollutant value
X3 <- ALL$land_temperature # land temperature
X4 <- ALL$land_humidity # just for fun 
summary(lm(Y ~ X1 + X2 + X3 + X4))
# coefficient near land main pollutant is zero, super strange

### PCA

ALLm <- cbind(ALL$cams_pm25, ALL$land_pm25, ALL$land_pm10, ALL$land_temperature, ALL$land_humidity)
cor(ALLm) # range is [0.12, 0.91]
cov(ALLm) # range is [2.34, 218.42], it's wider, let's use S
summary(prcomp(ALLm, scale = FALSE))
# single component accounts 81.4% of variance,
# 94.1% for 2 components, let's use 2 components for better accuracy

### FACTOR

library(psych)
principal(ALLm, nfactors = 2)$loadings 
# satelite (1) and land (2, 3) pollutants are combined into factor RC1
# temperature (4) and humidity (5) are combined into factor RC2
# that makes sense and doesn't disagree with correlation matrix
