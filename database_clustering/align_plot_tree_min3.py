"""
Build and plot neighbour-joining trees from multiple-sequence alignments.

For each alignment file in the input directory that contains at least a minimum
number of sequences (default 3, hence the "min3" in the name), compute a
distance matrix, build a neighbour-joining tree, and render it to one page of a
multi-page PDF (titled with the gene name taken from the file name).

This is a pure-Python reimplementation of the original rpy2/R (ape) script and
depends only on Biopython and matplotlib -- no R or rpy2. Alignments must be
generated beforehand (e.g. with muscle or mafft) and supplied as alignment
files in a format Biopython's AlignIO understands (FASTA by default).
"""

import glob
import os
from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(
        description="Plot neighbour-joining trees from sequence alignments."
    )
    parser.add_argument(
        "--input_dir",
        default=".",
        help="Directory containing alignment files (default: current directory)",
    )
    parser.add_argument(
        "--pattern",
        default="*.aln",
        help="Glob pattern for alignment files within --input_dir (default: *.aln)",
    )
    parser.add_argument(
        "--output",
        default="trees.pdf",
        help="Output PDF file (default: trees.pdf)",
    )
    parser.add_argument(
        "--min_seqs",
        type=int,
        default=3,
        help="Minimum number of sequences an alignment must contain to be plotted (default: 3)",
    )
    parser.add_argument(
        "--informat",
        default="fasta",
        help="Alignment format, as understood by Biopython AlignIO (default: fasta)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Imported here so that `--help` works without matplotlib/Biopython present,
    # and so the non-interactive backend is selected before pyplot is imported.
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    from Bio import AlignIO, Phylo
    from Bio.Phylo.TreeConstruction import (
        DistanceCalculator,
        DistanceTreeConstructor,
    )

    alignment_files = sorted(glob.glob(os.path.join(args.input_dir, args.pattern)))
    print("Number of input alignments found:", len(alignment_files))

    calculator = DistanceCalculator("identity")
    constructor = DistanceTreeConstructor()

    plotted = 0
    with PdfPages(args.output) as pdf:
        for filename in alignment_files:
            try:
                alignment = AlignIO.read(filename, args.informat)
            except Exception as e:
                print("Skipping {} (could not read alignment: {})".format(filename, e))
                continue

            if len(alignment) < args.min_seqs:
                continue

            distance_matrix = calculator.get_distance(alignment)
            tree = constructor.nj(distance_matrix)

            # Gene name = first dot-delimited part of the file's base name,
            # matching the original script's naming (e.g. geneA.fsa.aln -> geneA).
            gene_name = os.path.basename(filename).split(".")[0]

            fig = plt.figure(figsize=(9, 12))
            ax = fig.add_subplot(1, 1, 1)
            # Only label the tips (hide the internal "Inner<N>" node labels),
            # to match the look of the original ape plot.
            Phylo.draw(
                tree,
                axes=ax,
                do_show=False,
                label_func=lambda clade: clade.name if clade.is_terminal() else "",
            )
            ax.set_title("Gene: " + gene_name)
            pdf.savefig(fig)
            plt.close(fig)
            plotted += 1

    print("Plotted {} tree(s) to {}".format(plotted, args.output))


if __name__ == "__main__":
    main()
