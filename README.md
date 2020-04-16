# rasam

Rasa Improvements

<table>
    <tr>
        <td>License</td>
        <td><img src='https://img.shields.io/pypi/l/rasam.svg' alt="License"></td>
        <td>Version</td>
        <td><img src='https://img.shields.io/pypi/v/rasam.svg' alt="Version"></td>
    </tr>
    <tr>
        <td>Travis CI</td>
        <td><img src='https://travis-ci.org/roniemartinez/rasam.svg?branch=master' alt="Travis CI"></td>
        <td>Coverage</td>
        <td><img src='https://codecov.io/gh/roniemartinez/rasam/branch/master/graph/badge.svg' alt="CodeCov"></td>
    </tr>
    <tr>
        <td>AppVeyor</td>
        <td><img src='https://ci.appveyor.com/api/projects/status/9jd435vy2csjjkvo/branch/master?svg=true' alt="AppVeyor"></td>
        <td>Supported versions</td>
        <td><img src='https://img.shields.io/pypi/pyversions/rasam.svg' alt="Python Versions"></td>
    </tr>
    <tr>
        <td>Wheel</td>
        <td><img src='https://img.shields.io/pypi/wheel/rasam.svg' alt="Wheel"></td>
        <td>Implementation</td>
        <td><img src='https://img.shields.io/pypi/implementation/rasam.svg' alt="Implementation"></td>
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
pipeline:
  - name: rasam.RegexEntityExtractor
  - name: rasam.URLEntityExtractor
```

## Author
[Ronie Martinez](ronmarti18@gmail.com) 
