library(reshape2)
library(ggplot2)
library(ggthemes)
library(ggExtra)
library(ggplot2)


x <- c("LeNet")
for (val in x) {

fname=paste("cum_",val,".csv",sep="")
print (fname)
df <- read.csv(fname, header=T)

ggplot(data=df,aes(x=Total_Cost, y=Volume, color=Method))+geom_step(direction="vh")+
    #geom_errorbar(aes(ymin=Volume-SD, ymax=Volume+SD),width=0.4)+
    facet_wrap(~Architecture)+xlab("Cumulative Cost ")+
    ylab("Hypervolume")+ ylim(0.35, 0.85)+ 
    theme_bw()+theme(legend.position = "top")+
    theme(axis.text.x = element_text(hjust=1,family="serif",size=12), axis.title.x =   element_text(hjust=0.5,family="serif",size=16))+
    theme(axis.text.y = element_text(hjust = 1, family="serif",size=16),axis.title.y = element_text(hjust = 0.5, family="serif",size=16))+
    theme(strip.text.x=element_text(size=16,color="black",family="serif"))+
    theme(panel.background=element_rect(fill=NA,color="black"))+
    theme(strip.background=element_blank())+
    theme(plot.background=element_rect(fill=NA))+ 
    theme(panel.spacing.x=unit(0.1, "lines"),panel.spacing.y=unit(0.3, "lines"))+
    theme(legend.text = element_text(colour="black", size = 12, family="serif"),legend.title = element_text(colour="black", size = 12, family="serif"))
pdf_file <- paste(val,"_hvc.pdf",sep="")

ggsave(
  pdf_file,
  device = cairo_pdf,
  width = 5.5,
  height = 5.6
)

knitr::plot_crop(pdf_file)
}
