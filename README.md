# rasam
Rasa Improvements

## Usage

### Installation

```shell script
pip install rasam
```

### Rasa `config.yml`

```yaml
pipeline:
  - name: rasam.RegexEntityExtractor
  - name: rasam.URLEntityExtractor
```

## Author
[Ronie Martinez](ronmarti18@gmail.com)
