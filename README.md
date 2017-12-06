# mdl-ling-chunks

To estimate complexity for BNC sentences using a LZ77 estimator, currently on 10K BNC sentences:

```bash
mdl-ling-chunks/src$ python est.py ../data/bnc_10K.txt ../data/bnc_10K_lz77_sentences.txt
```

## TODO

- [x] Build sentence-by-sentence strings
- [x] ... with length by compression ratio data points
- [ ] Build word-by-word strings
- [ ] ... with length by compression ratio data points
- [ ] Build morpheme-by-morpheme strings
- [ ] ... with length by compression ratio data points
- [ ] Create length of sequence (X-axis) by compression ratio (Y-axis) vizualisations
- [ ] Test for patterns, inflection points, etc.
- [ ] Build random reference strings (for comparisons)

- [ ] Update working notes (tex)

- [x] Collect test data (English, BNC)
- [ ] Collect suitable parallel data
- [x] LZ77 estimator in memory
- [ ] LZW estimator in memory
- [ ] Support standard input format for sentence/word/morpheme encoding