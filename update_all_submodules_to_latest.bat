git submodule foreach --recursive git clean -dfx
git submodule foreach --recursive git reset --hard
git submodule foreach --recursive git fetch
git submodule foreach --recursive './update_as_submodule.bat || :'
pause