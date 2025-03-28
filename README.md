# onnxruntime-qnn

## install CMake 3.28.0
```
apt update
apt install -y build-essential libssl-dev libcurl4-openssl-dev libexpat1-dev
cd /tmp
wget https://github.com/Kitware/CMake/releases/download/v3.28.0/cmake-3.28.0.tar.gz
tar -zxvf cmake-3.28.0.tar.gz
cd cmake-3.28.0
mkdir build
cd build
../configure
cmake ..
make -j$(nproc)
make install
cmake --version
```

## install g++ 11
```
apt update
apt install -y build-essential wget m4 autoconf automake libgmp-dev libmpfr-dev libmpc-dev zlib1g-dev flex bison
cd /tmp
wget http://ftp.gnu.org/gnu/gcc/gcc-11.1.0/gcc-11.1.0.tar.gz
tar -xvzf gcc-11.1.0.tar.gz
cd gcc-11.1.0
./contrib/download_prerequisites
mkdir ../gcc-build
cd ../gcc-build
../gcc-11.1.0/configure --prefix=/usr/local/gcc --enable-languages=c,c++ --disable-multilib
make -j$(nproc)
make install
echo "export PATH=/usr/local/gcc/bin:$PATH" >> ~/.bashrc
source ~/.bashrc
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-11 100
update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-11 100
gcc --version
```

## install onnxruntime-qnn
```
git clone --recursive https://github.com/Microsoft/onnxruntime.git
cd onnxruntime
./build.sh --use_qnn --qnn_home /home/aim/Documents/v2.26.0.240828/qairt/2.26.0.240828 --build_shared_lib --build_wheel --config Release --skip_tests --build_dir build/Linux --parallel 2 --allow_running_as_root
```

reference: 
* https://onnxruntime.ai/docs/build/eps.html#qnn
* https://docs.qualcomm.com/bundle/publicresource/topics/80-63442-2/dsp_runtime.html
* https://github.com/microsoft/onnxruntime/issues/21203
