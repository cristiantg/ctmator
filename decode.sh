#!/bin/sh


# Decodes a bunch of audio files and obtain the n-best output
################
# Please change all lines: # CHANGE-1, # CHANGE-2, # CHANGE-3 and
# CHANGE-4 with the correct path value
# PD: BTW, I tried to set a variable but when combining Kaldi + 
# pipes + variabels it does not work.
################


KALDIdir=/vol/tensusers3/ctejedor/lacristianmachine/opt/kaldi_nl
# CHANGE-1
HCLGdir=/vol/tensusers3/ctejedor/cgn_light/out_cgn
#######HCLGdir=$KALDIdir/out_cgn
HCLG=$HCLGdir/HCLG.fst
wordlist=$HCLGdir/words.txt
model=$KALDIdir/models/NL/UTwente/HMI/AM/CGN_all/nnet3_online/tdnn/v1.0
latbindir=/vol/customopt/lamachine2/opt/kaldi/src/latbin
utilsdir=utils
# CHANGE-2
# Change the same value of indir and outdir in the next command
# Change the same value of indir and outdir in the next command
#indir=/vol/tensusers3/ctejedor/lacristianmachine/opt/kaldi_nl/homed_21_cgn/decoded
indir=/vol/tensusers3/ctejedor/cgn_light/decoded
outdir=$indir
rm -r $outdir
mkdir -p $outdir


/vol/customopt/lamachine2/opt/kaldi/src/online2bin/online2-wav-nnet3-latgen-faster \
--do-endpointing=false \
--frames-per-chunk=20 \
--extra-left-context-initial=0 \
--online=false \
--frame-subsampling-factor=3 \
--config=${model}/conf/online.conf \
--min-active=200 \
--max-active=7000 \
--beam=15 \
--lattice-beam=6.0 \
--acoustic-scale=1.2 \
--word-symbol-table=$wordlist \
${model}/final.mdl \
$HCLG \
ark:/vol/tensusers3/ctejedor/cgn_light/homed_kaldi/spk2utt 'ark,s,cs:/vol/customopt/lamachine2/opt/kaldi/src/featbin/extract-segments scp,p:/vol/tensusers3/ctejedor/cgn_light/homed_kaldi/wavscp.scp /vol/tensusers3/ctejedor/cgn_light/homed_kaldi/segments ark:- |' 'ark:|/vol/customopt/lamachine2/opt/kaldi/src/latbin/lattice-scale \
--acoustic-scale=10.0 ark:- ark:- | gzip -c > /vol/tensusers3/ctejedor/cgn_light/decoded/mylat.test1.gz'
# CHANGE-3 and CHANGE-4 (PREV. 2 LINES)
gunzip -c $outdir/mylat.test1.gz | $latbindir/lattice-to-ctm-conf --frame-shift=0.03 --inv-acoustic-scale=10  ark:- $outdir/out.ctm
cat $outdir/out.ctm | $utilsdir/int2sym.pl -f 5 $wordlist > $outdir/out.ctm_w
