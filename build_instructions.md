## Build
sphinx-build -b html docs/source/ docs/build/html

## Test whether your translation works
sphinx-build -b html -D language=zh_CN docs/source  docs/build/html/zh_CN

## Update the .pot source file
sphinx-build -b gettext docs/source docs/pot

## Transifex action
### Push your source
tx push -s
### Pull your source
tx pull -a