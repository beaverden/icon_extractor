rmdir /S /Q build
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=%1 .. 
cmake --build . --target install --config Release
::call "C:\Program Files (x86)\Microsoft Visual Studio\2019\Community\VC\Auxiliary\Build\vcvars64.bat"
::msbuild LockYourShit.sln /p:Configuration=%1