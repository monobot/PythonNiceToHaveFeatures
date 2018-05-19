# SublimeText3 PythonNiceToHaveFeatures
**_PythonNiceToHaveFeatures_** are a set of features usually included in IDEs that are not present in SublimeText.

## Refactor Commands
They are available in the context menu of the opened file and affect only to that file (we can not do that refactor in the whole project because SublimeText doesn't know the whole context of the project and its better to be safe than sorry)
These commands affect to each and all the selected regions.

- Refactor to _ClassCase_
- Refactor to _under\_score\_case_
- Refactor to _camelCase_
- Refactor to _Capfirst_

## File Commands
These commands are available both in the sidebar menu and the file context menu.

- Copy relative path to clipboard
- Copy relative path in package mode to clipboard
- Copy reference in package mode to clipboard
    + Will copy the reference of the selection or word
- Copy filename to clipboard
- Create Package (and __init__.py file) (only side bar menu)
