# rasam

Rasa Improved

<table>
    <tr>
        <td>License</td>
        <td><img src='https://img.shields.io/pypi/l/rasam.svg' alt="License"></td>
        <td>Version</td>
        <td><img src='https://img.shields.io/pypi/v/rasam.svg' alt="Version"></td>
    </tr>
    <tr>
        <td>Travis CI</td>
        <td><img src='https://travis-ci.org/roniemartinez/rasam.svg?branch=develop' alt="Travis CI"></td>
        <td>Coverage</td>
        <td><img src='https://codecov.io/gh/roniemartinez/rasam/branch/develop/graph/badge.svg' alt="CodeCov"></td>
    </tr>
    <tr>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/rasam.svg' alt="Python Versions"></td>
        <td>Wheel</td>
        <td><img src='https://img.shields.io/pypi/wheel/rasam.svg' alt="Wheel"></td>
    </tr>
    <tr>
        <td>Status</td>
        <td><img src='https://img.shields.io/pypi/status/rasam.svg' alt="Status"></td>
        <td>Downloads</td>
        <td><img src='https://img.shields.io/pypi/dm/rasam.svg' alt="Downloads"></td>
    </tr>
</table>

## Support
If you like `rasam` or if it is useful to you, show your support by buying me a coffee.

<a href="https://www.buymeacoffee.com/roniemartinez" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## Usage

### Installation

```shell script
pip install rasam
```

### Rasa `config.yml`

```yaml
importers:
  - name: rasam.PlaceholderImporter
    fake_data_count: 10  # default value is 1

pipeline:
  - name: rasam.RegexEntityExtractor
  - name: rasam.URLEntityExtractor
```

### Rasa `nlu.md`

#### PlaceholderImporter

The PlaceholderImporter removes the need to write unnecessary information (eg. name, address, numbers, etc.) and helps focus on writing test data.

#### Using `{}` placeholder

```markdown
## intent:tell_name
- My name is {name}
- I am {name} and he is {name}
```

#### Using `@` placeholder

```markdown
## intent:tell_address
- I live in @address
- I stay at @address and @address
```

#### Mixing `{}` and `@` placeholders

It is possible to mix both `{}` and `@` placeholders but it is recommended to use only one style for consistency.

#### Available placeholders

Under construction.

## Author
[Ronie Martinez](ronmarti18@gmail.com) 
