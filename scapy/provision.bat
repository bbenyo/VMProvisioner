SET sdir=c:/Dev/scapy
SET py=python

powershell Expand-Archive master.zip -DestinationPath %sdir% -Force

cd %sdir%/scapy-master
python setup.py install

%py% -m pip install ipython
%py% -m pip install matplotlib
%py% -m pip install pyx
%py% -m pip install cryptography
%py% -m pip install sphinx
%py% -m pip install sphinx_rtd_theme
%py% -m pip install tox

cd doc/scapy
make html

xcopy /S /I /Y files %sdir%



