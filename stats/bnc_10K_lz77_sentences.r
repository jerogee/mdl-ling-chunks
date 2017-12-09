library(ggplot2)

# Input data & output figure
fn_i <- '../data/bnc_10K_lz77_sentences.txt'
fn_o <- 'bnc_10K_lz77_sentences.pdf'

# Plot
pdf(fn_o, height=6, width=8)
p <- ggplot(data=read.table(header=T, file=fn_i), aes(x=length, y=ratio))
p <- p + geom_line() + geom_point()
p <- p + xlab("Sequence length (characters)") 
p <- p + ylab("Compression Ratio (original / compressed)")
p <- p + theme_bw()
p
dev.off()