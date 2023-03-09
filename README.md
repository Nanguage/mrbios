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


## TODO List

+ Project scaffolding
  * Create project (done)
  * CURD for: (done)
    + environment
    + file type
    + file format
    + task
    + script
  * verbose mode for list DirObjs.
+ Environment build
  * conda env build
    + create env and install conda dependents (done)
    + Run command under the conda env. (done)
    + support pip install (done)
    + support install R package with `install.packages` (done)
    + support install R package with `Bioconductor` (done)
    + support install R package with `devtools` (done)
    + support build compiled languages
      * C/C++
      * Rust
  * Build docker image for whole project
+ Global state setting (done)
  * set global project path
+ Script run
  * with CLI
  * with [oneFace](https://github.com/Nanguage/oneFace) GUI/WebUI


## Credits

This package was created with Cookiecutter and the `Nanguage/cookiecuter-pypackage` project template.

+ Cookiecutter: https://github.com/audreyr/cookiecutter
+ `Nanguage/cookiecutter-pypackage`: https://github.com/Nanguage/cookiecutter-pypackage
