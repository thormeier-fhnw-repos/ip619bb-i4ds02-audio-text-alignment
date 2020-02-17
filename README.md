# Audio-Text-Alignment for Swiss german speech recognition

Library for automated forced alignment of given Swiss german audio and German transcript.

## Requirements

* **Python version:** 3.6
* **And the following libraries:**
    * prettytable==0.7.2
    * pydub==0.23.1
    * numpy==1.13.1+mkl
    * nltk==3.4.5
    * Bio==0.1.0
    * PyYAML==5.2
    * google==2.0.3

See ./requirements.txt for a list generated by [pireqs](https://github.com/bndr/pipreqs).

## Getting started

 1. Clone this repository
 2. Install dependencies (see  Requirements )
 3. Download the output of a given Google STT execution (**must be JSON**) and place it in the same folder as your audio and transcript files.
 4. Make sure all file groups follow this naming convention and all mentioned files are present:
    ```shell script
    [source_file_name].txt                  # The transcript
    [source_file_name].wav                  # Mono-channel WAV file
    [source_file_name].flac                 # OPTIONAL: Mono-channel FLAC file, only needed for generating the google output.
    [source_file_name]_google_output.json   # Output generated by google
    [source_file_name]_audacity_hand.txt    # OPTIONAL: Hand alignment
    ```
    For instance:
    ```shell script
    gemeinde_stadthausen_123.txt
    gemeinde_stadthausen_123.wav
    gemeinde_stadthausen_123_google_output.json
    ```
 5. Copy and alter `./config.example.yml` to your needs (See  Configuration )
 6. Generate alignments as needed using the CLI commands (See  CLI commands )

## Configuration

```yaml
aligner_type: [  basic | random | google_biopython | google_global_character | google_global_word | google_semiglobal_character | google_semiglobal_word | google_local_character | google_local_word ]

algorithm:
  match_reward: int
  mismatch_penalty: int
  gap_penalty: int

no_appearance:
  type: [ character | time ]
  interval_length: float

score_weights:
  gaps_google: float
  gaps_transcript: float
  alignment_score: float
  google_confidence: float

filtering:
  threshold: float
  method: [ mark | delete ]
```

## CLI commands

The following CLI commands are available and should be executed as `python ./bin/{scriptName}` from project root:

```
Create alignment
----------


Creates an alignment based on configuration. See README.md for setting up a correct configuration.

Usage:
    python create_alignment.py --path=<path> --config=<path> [-v|-vv|-vvv]

Args:
    --path:      Path to read raw data from and write alignments to
    --config:    Path to configuration
    -v|-vv|-vvv: Verbosity level of the output
    -h:          Prints this help
```

```
Compare alignments
----------


Compares two kinds of alignments

Usage:
    python compare_alignment.py --path=<path> --type1=basic,hand,random,google --type2=basic,hand,random,google [-v|-vv|-vvv] [--with-list] [--get-low-means] [--training-only]

Args:
    --path:          Path to read alignment data
    --type1:         First type to compare, one of basic, hand, random or google
    --type2:         Second type to compare, one of basic, hand, random or google
    -v|-vv|-vvv:     Verbosity level of the output
    --with-list:     Include a list with all calculated IOUs for copy/paste (to use in an EXCEL sheet, for example)
    --get-low-means: Includes a list of wav files with a mean IOU < 0.3, for debugging purposes
    --training-only: Only ever compares sentences marked with [TRAINING] in the first type of the alignment
    -h:              Prints this help
```

```
Get Google recognition
----------


Gets the Speech Recognition result of Google Cloud API and stores it in a caching folder.

Usage:
    python get_google_recognition_raw.py --path=<path> --authpath=<path> --bucket=<bucket name> --outpath=<path> [-v|-vv|-vvv]

Args:
    --path:      Path to read transcript files from (needed to filter which files to actually transcript)
    --authpath:  Path containing the authentication files necessary to connect to Google Cloud API services
    --bucket:    Name of the bucket containing all FLAC files
    --outpath:   Path to write the raw JSON output to
    -v|-vv|-vvv: Verbosity level of the output
    -h:          Prints this help
```

```
Fix hand alignments
----------


Fix hand alignments: Reshuffle training data and/or assign `-` to nonexisting sentences.

Usage:
    python fix_hand_alignments.py --path=<path> [-v|-vv|-vvv] [--fix-nonexisting] [--reshuffle-training]

Args:
    --path:               Path to read alignment data
    -v|-vv|-vvv:          Verbosity level of the output
    --fix-nonexisting:    If non-existing sentences should be marked with `-` for interval start and end points
    --reshuffle-training: Select a new 70% of all sentences as training data
    -h:                   Prints this help
```

```
Optimize alignments
----------


Tries to find the best alignment parameters based on Bayesian optimization.

Usage:
    python optimize_parameters.py --path=<path> --config=<path> [-v|-vv|-vvv]

Args:
    --path:                  Path to read alignment data from
    --config:                Path to configuration
    --convergence-plot-file: Filename for the plot of the convergence
    --acquisition-plot-file: Filename for the plot of the acquisition (if possible to create)
    -v|-vv|-vvv:             Verbosity level of the output
    -h:                      Prints this help
```

```
Optimize score
----------


Tries to find the best parameters for overall score based on Bayesian optimization.

Usage:
    python optimize_score.py --path=<path> --config=<path> [-v|-vv|-vvv]

Args:
    --path:                  Path to read alignment data from
    --config:                Path to configuration
    --convergence-plot-file: Filename for the plot of the convergence
    --acquisition-plot-file: Filename for the plot of the acquisition (if possible to create)
    -v|-vv|-vvv:             Verbosity level of the output
    -h:                      Prints this help
```

## Bechnmarking

### Memory usage

For detailed memory usage, the package [memory_profiler](https://pypi.org/project/memory-profiler/) is used. The code contains several annotations to measure memory usage.  

To measure, execute an arbitrary CLI command with the memory_profiler module:

```
python -m memory_profiler ./bin/{command and args}
```

### Execution time per sentence while aligning



## License

MIT, see LICENSE.md
