install.packages('ggplot2')
library(ggplot2)

# bar-graph showing average AT:GC per k-mer per list

kmer_len <- c(3,4,5,6)
rand_ratio <- c(1.0, 1.02, 1.04, 1.09)
biased_ratio <- c(1.1, 0.94, 0.8, 1.0)

# create a dataset
kmer=c(rep("3-mer" , 3) , rep("4-mer" , 3) , rep("5-mer" , 3) , rep("6-mer" , 3) )
Nucleotides=rep(c("AT-Biased Happy", "GC-Biased Sad","Random") , 4)
value = c(1.0, 0.76, 1.0, 1.02,0.53,1.02, 1.23,1.04,0.35, 1.39,0.33,1.09)

data=data.frame(kmer,nucleotides,value)
data
# Grouped
kmersplot <- ggplot(data, aes(fill=Nucleotides, y=value, x=kmer)) + 
  geom_bar(position="dodge", stat="identity")

print(kmersplot + ggtitle("AT:GC Ratio in k-mers of Varying Lengths"))
print(kmersplot + labs(y="AT:GC Ratio", x = "k-mer") + ggtitle("AT:GC Ratio in k-mers of Varying Lengths"))

#plot(x=kmer, y=value, main="AT:GC Nucleotide Ratio in k-mers of Varying Lengths",
#     xlab="k-mer", ylab="AT:GC Ratio",
#     xlim=c(3, 6), ylim=c(0, 1.5))
