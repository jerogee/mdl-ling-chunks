# mdl-ling-chunks

To estimate complexity for BNC sentences using a LZ77 estimator, currently on 10K BNC sentences:

```bash
mdl-ling-chunks/src$ python est.py ../data/bnc_10K.txt ../data/bnc_10K_lz77.txt
```

## Open tasks

- [x] Collext test data (English, BNC)
- [ ] Collect suitable parallel data
- [x] LZ77 estimator in memory
- [ ] LZW estimator in memory
- [ ] Support standard input format for sentence/word/morpheme encoding
- [x] Sentence level
- [ ] Word level
- [ ] Morpheme