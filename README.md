# MNN Demo

#### 介绍

最简单的机器学习全流程Demo

1. 训练一个线性回归的模型
2. 使用MNNConvert进行模型转换
3. 调用MNN（2.8.1）部署



线性回归模型
$$
y = w_0 * x_0 + w_1 * x_1 + b \\
w_0 = 2, w_1 = -3, b = 4 
$$



#### 安装教程

##### 编译MNN

```shell
# 拷贝build.py和builder.py到MNN根目录
python build.py --platform=Linux --benchmark --converter --demo --quantools
python build.py --clean
```

运行build.py安装程序，选项如下：

* clean：清空构建目录和安装目录
* platform
  * Linux
  * Android

* benchmark：构建benchmark
* converter：构建模型转换器
* demo：构建demo
* quantools：构建量化工具



编译完成后需要将动态库拷贝到 MNN/libs 的 linux 或 android 文件夹中

* linux
  * libMNN.so
* android
  * libMNN_CL.so
  * libMNN_Express.so
  * libMNN.so
  * libMNNConvertDeps.so



##### 编译推理demo - LinearRegression

```shell
cd ./infer
python build.py --platform=Linux
python build.py --clean
```

运行build.py安装程序，选项如下：

* clean：清空构建目录和安装目录
* platform
  * Linux
  * Android



#### 使用说明

##### 训练

```shell
cd ./train
python linear-regression.py
```



##### 模型转换

```shell
./${Path_MNNConvert}/MNNConvert -f ONNX --modelFile ./${Path_ONNX}/linear.onnx --MNNModel ./${Path_MNN}/linear.mnn --bizCode biz
```



在 android 进行模型转换需要依赖 libMNNConvertDeps.so 和 libMNN_CL.so。



##### 推理

```shell
./${Path_Demo}/LinearRegression ./${Path_MNN}/linear.mnn 2 1
```

