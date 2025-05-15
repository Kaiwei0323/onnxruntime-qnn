# 🧠 Build ONNX Runtime with Qualcomm QNN Execution Provider on Ubuntu
This guide walks you through building ONNX Runtime with support for Qualcomm's QNN Execution Provider (QNN EP) on Ubuntu. It includes steps to install GCC 11.2.0, Python 3.11, and CMake 3.28.0, and details how to configure and build ONNX Runtime with the QNN SDK.

---

## ✅ Prerequisites
* QCS6490
* Ubuntu 20.04
* Qualcomm QNN SDK (e.g., v2.26.0.240828)

---

## Step 1: Install Python 3.11
```
add-apt-repository ppa:deadsnakes/ppa
apt update
apt install python3.11
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
update-alternatives --config python3
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.11 get-pip.py
```

---

## Step 2: Install CMake 3.28.0
```
apt update
apt install -y build-essential libssl-dev
cd /home/aim
wget https://github.com/Kitware/CMake/releases/download/v3.28.0/cmake-3.28.0.tar.gz
tar -zxvf cmake-3.28.0.tar.gz
cd cmake-3.28.0
echo 'export LD_LIBRARY_PATH=/usr/local/gcc/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
source ~/.bashrc
strings /usr/local/gcc/lib64/libstdc++.so.6 | grep GLIBCXX_3.4.29
./bootstrap
make -j$(nproc)
make install
```

---

## Step 3: Install GCC 11.1.0
```
apt update
apt install -y build-essential wget m4 autoconf automake libgmp-dev libmpfr-dev libmpc-dev zlib1g-dev flex bison
cd /home/aim
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
gcc --version
```

---

## Step 4: Clone and Configure ONNX Runtime
```
cd /home/aim
git clone --recursive https://github.com/Microsoft/onnxruntime.git
cd onnxruntime
```
### 🔧 Modify CMake ABI for QNN
Edit onnxruntime/cmake/CMakeLists.txt and around line 1001, set the QNN ABI as follows:
```
set(QNN_ARCH_ABI aarch64-ubuntu-gcc9.4)
else()
set(QNN_ARCH_ABI aarch64-ubuntu-gcc9.4)
```

---

## Step 5: Build ONNX Runtime with QNN EP
```
apt install protobuf-compiler -y
python3.11 -m pip install numpy
python3.11 -m pip install packaging
python3.11 -m pip install onnx
./build.sh --use_qnn --qnn_home /home/aim/Documents/v2.26.0.240828/qairt/2.26.0.240828 --build_shared_lib --build_wheel --config Release --skip_tests --build_dir build/Linux --parallel 2 --allow_running_as_root
```

reference: 
* https://onnxruntime.ai/docs/build/eps.html#qnn
* https://docs.qualcomm.com/bundle/publicresource/topics/80-63442-2/dsp_runtime.html
* https://github.com/microsoft/onnxruntime/issues/21203
