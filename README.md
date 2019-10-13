# Audio-Text-Alignment for Swiss german speech recognition

Requires Python 3.6

## CLI Commands

There's several CLI commands that can be executed:
 - Create a basic alignment
 - Create a random alignment
 - Compare two arbitrary alignments via IOU

### Create basic alignment

To create a basic alignment for all transcripts and wave files within a given directory, execute

```
python ./bin/create_basic_alignment.py --path=../your/data/path
```

**Keep in mind that the WAV-file and its transcript need to be named the same in order to be aligned.**

### Create random alignment

To create a random alignment for all transcripts and wave files within a given directory, execute

```
python ./bin/create_random_alignment.py --path=../your/data/path
```

**Keep in mind that the WAV-file and its transcript need to be named the same in order to be aligned.**

### Compare alignments

To compare two kinds of alignments, execute

```
python ./bin/compare-alignments.py --path=../your/data/path --type1=hand --type2=basic
```

Whereas the parameters `--type1` and `--type2` can be either one of `random`, `basic` or `hand`.
