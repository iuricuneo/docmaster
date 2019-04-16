# docmaster

## Under development.

Minimal application will be capable of moving files into a specific folder and
restoring them. This will be expanded into copying files to the folder,
compressing them and allowing the user to restore them with one or two keywords.

The minimal application will be composed of 3 main modules: the interpreter, the
search engine and the file handler, responsible, respectively for interpreting
user commands, handling search requests from the interpreter, and handling
file-related requests from the file handler.

After successful implementation of the minimal application, this will be
extended into a application with diverse uses, plus unit tests.

For testing purposes, run:

```
cd docmaster
echo "test" > file.txt
python3 docmaster save file.txt
python3 docmaster save file.txt -v
python3 docmaster show file.txt -v
python3 docmaster update file.txt -v
python3 docmaster update file.txt -vf
python3 docmaster remove file.txt -v
python3 docmaster remove file.txt -vf
```

Without the implementation of a file handler, nothing will be done to the file.

Author: Iuri Cuneo Ferreira
