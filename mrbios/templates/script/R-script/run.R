#!/usr/bin/env Rscript

library(optparse)

parser <- OptionParser()
parser <- add_option(parser, "--name", help="Name of the person")
parser <- add_option(parser, "--times", type="integer", default=1, help="Number of times to say hello")
parser <- add_option(parser, "--out", default="output.txt", help="Output file name")
args <- commandArgs(TRUE)
options <- parse_args(parser, args = args)


main <- function(name, times, output_file) {
  hello_msg <- paste0("Hello, ", name, "!")
  cat(paste(rep(hello_msg, times), collapse="\n"), file=output_file)
  cat(paste0("Result written to ", output_file, "\n"))
}


main(options$name, options$times, options$out)
