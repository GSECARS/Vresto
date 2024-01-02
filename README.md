# Vresto

[![License](https://img.shields.io/badge/license-GPL--3.0-orange.svg)](LICENSE) ![Python](https://img.shields.io/badge/python-v3.9--v3.10-blue.svg?logo=python)

Vresto is used to locate and perform optical corrections on the samples used in the GSECARS DAC program. The application allows access to all the basic motors for visualization and alignment procedures. Advanced users can operate without having any limitations in place and save or move to known positions.
The application allows easy conversion of sample coordinates among the 13-ID-D, 13-BM-D stations, and the offline Raman system.

------------
## Table of Contents

- [Installation](#installation)
- [License](#license)

------------
## Installation

Make sure that you install all the requirements for the project.

#### Python Requirements

- Python >= 3.9
- pyepics>=3.5.1
- numpy>=1.22.3
- pyqt5>=5.15.6
- qtpy>=2.0.1

#### Source

Download the GitHub repository and install it locally on your system.

```bash
git clone -b main https://github.com/GSECARS/Vresto.git && cd Vresto
```


```bash
pip install .
```

------------
## Contributing

All contributions to Vresto are welcome! Here are some ways you can help:
- Report a bug by opening an [issue](https://github.com/GSECARS/Vresto/issues).
- Add new features, fix bugs or improve documentation by submitting a [pull request](https://github.com/GSECARS/Vresto/pulls).

Please adhere to the [GitHub flow](https://docs.github.com/en/get-started/quickstart/github-flow) model when making your contributions! This means creating a new branch for each feature or bug fix, and submitting your changes as a pull request against the main branch. If you're not sure how to contribute, please open an issue and we'll be happy to help you out.

By contributing to Vresto, you agree that your contributions will be licensed under the GPL-3.0 license.

[back to top](#table-of-contents)

------------
## License

Vresto is distributed under the GPL-3.0 license. You should have received a [copy](LICENSE) of the GPL-3.0 License along with this program. If not, see [https://www.gnu.org/licenses/gpl-3.0.en.html/](https://www.gnu.org/licenses/gpl-3.0.en.html) for additional details.

------------
#### [Christofanis Skordas](mailto:skordasc@uchicago.edu) - Last updated: 02-Jan-2024
