ALL <- read.table("./correlation/post_30_at_12:00.csv", header=TRUE)

head(ALL)
SAT <- ALL$cams_pm25
LAND <- ALL$value

### CORRELATION

ks.test(ALL$value, ALL$cams_pm25, alternative = "two.sided") # rejected

# wilcox.test(ALL$value, ALL$cams_pm25) # rejected UNPAIRED

cor.test(ALL$value, ALL$cams_pm25, method="spearman") # rejected

cor(ALL$value, ALL$cams_pm25, method="pearson")
