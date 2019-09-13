## Creating the Executable for Yourself!
I used the pyinstaller python package to bundle the source code along with its
dependencies to be run as an executable. If you don't currently have the package,
you can install it through [anaconda](https://anaconda.org/conda-forge/pyinstaller)

Once you have pyinstaller downloaded, simply run the pyinstaller command and
pass in your project's driver program.

```sh
pyinstaller drb_rounder.py
```

The executable can be found at `dist/drb_rounder/drb_rounder.exe`


