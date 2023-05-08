# hyperbuild
an attempt at a build system that is agnostic of language and platform with simple and intuitive build results that are consistent and reproducible


## Dependencies

python 3.x

## Developement Mode


python -m venv .venv

<!-- [] -->
#### Activate your environemt with:

##### source .venv/bin/activate` on Unix/macOS
      
##### .venv\Scripts\activate` on Windows

`pip install --editable .`

then just run

`hyperbuild`

to build or

`hyperbuild -r True`

to build and run
