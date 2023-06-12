<div align="center">
<h1> Mr.BIOS </h1>

<p> A bioinformatics scripts management tool. </p>

<p>
    <a href="https://github.com/Nanguage/mrbios/actions/workflows/build_and_test.yml">
        <img src="https://github.com/Nanguage/mrbios/actions/workflows/build_and_test.yml/badge.svg" alt="Build Status">
    </a>
    <a href="https://app.codecov.io/gh/Nanguage/mrbios">
        <img src="https://codecov.io/gh/Nanguage/mrbios/branch/master/graph/badge.svg" alt="codecov">
    </a>
    <a href="https://mrbios.readthedocs.io/en/latest/">
    	<img src="https://readthedocs.org/projects/mrbios/badge/?version=latest" alt="Documentation">
    </a>
  <a href="https://pypi.org/project/mrbios/">
    <img src="https://img.shields.io/pypi/v/mrbios.svg" alt="Install with PyPI" />
  </a>
  <a href="https://github.com/Nanguage/mrbios/blob/master/LICENSE">
    <img src="https://img.shields.io/github/license/Nanguage/mrbios" alt="MIT license" />
  </a>
</p>
</div>


**Work In Progress**


## Features

+ Project scaffolding
  * Create project
  * CURD for:
    + environment
    + file type
    + file format
    + task
    + script
+ Environment build
  * Conda env build
    + Create env and install conda dependents.
    + Support fast env build using [`mamba`](https://github.com/mamba-org/mamba)
    + Support pip install.
    + Support install R package with `install.packages`.
    + Support install R package with `Bioconductor`.
    + Support install R package with `devtools`.
  * Conda env update, delete.
  * Run command under the conda env.
+ Global state setting
  * set global project path
+ Script run
  * with CLI
  * with [oneFace](https://github.com/Nanguage/oneFace) GUI/WebUI.
+ Integrate with [executor-http](https://github.com/Nanguage/executor-http).


## TODO List

+ UI for project management.
+ Support notebook.
+ Build docker image for whole project.
+ Support build compiled languages.
  * C/C++
  * Rust
+ Verbose mode for list DirObjs.
+ Documentation.
+ Pipeline module design.

## Credits

This package was created with Cookiecutter and the `Nanguage/cookiecuter-pypackage` project template.

+ Cookiecutter: https://github.com/audreyr/cookiecutter
+ `Nanguage/cookiecutter-pypackage`: https://github.com/Nanguage/cookiecutter-pypackage
