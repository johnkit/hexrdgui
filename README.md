# Develop

Requires Python 3.6+

```bash
git clone git@github.com:/HEXRD/hexrd.git
git clone git@github.com:/HEXRD/hexrdgui.git
```

## pip

```bash
pip install numpy
# For now we need to explicitly install hexrd, until we push it to PyPI
pip install -e hexrd
pip install -e hexrdgui
```

## conda

```bash
# Install deps using conda package
conda install -c cjh1 -c conda-forge hexrdgui
# Now using pip to link repo's into environment for development
pip install --no-deps -U -e hexrd
CONDA_BUILD=1 pip install --no-deps -U -e hexrdgui
```

# Run

```bash
hexrd
```
