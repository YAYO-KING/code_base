conda的使用：

https://www.anaconda.com/

Python 管理工具 —— conda

Anaconda：一个非常流行的 Python 发行版，用于科学计算。它包含了 Vonda、Python 和超过 150 个科学软件包及其依赖项
Miniconda：Anaconda 的轻量级版本，只包含了 Python 和 Conda，以及它们的依赖项
Conda：一个开源的包管理系统和环境管理系统，用于安装多种语言的软件包

一般安装带可视化界面的Anaconda（也最大）

-------------------------------------------------------- 1.环境管理 --------------------------------------------------------
查看conda的版本号
conda -V

查看环境
conda env list

创建虚拟环境
conda create --name 环境名称 安装库包列表

创建环境并安装Python指定版本
conda create --name 环境名称 python=3.8

启用创建的环境
conda activate  环境名称

退出当前环境
conda deactivate

删除环境
conda env remove --name 环境名称

-------------------------------------------------------- 2.包管理 --------------------------------------------------------

进入环境后安装需要的包
conda install requests

查看已经安装的包
conda list

更新包
conda update 包名

删除包
conda remove 包名

-------------------------------------------------------- 3.通道 --------------------------------------------------------
设置conda源：
直接修改在用户目录下的.condarc文件（没有的新建一个）
```
channels:
  - defaults
show_channel_urls: true
default_channels:
  - http://mirrors.aliyun.com/anaconda/pkgs/main
  - http://mirrors.aliyun.com/anaconda/pkgs/r
  - http://mirrors.aliyun.com/anaconda/pkgs/msys2
custom_channels:
  conda-forge: http://mirrors.aliyun.com/anaconda/cloud
  msys2: http://mirrors.aliyun.com/anaconda/cloud
  bioconda: http://mirrors.aliyun.com/anaconda/cloud
  menpo: http://mirrors.aliyun.com/anaconda/cloud
  pytorch: http://mirrors.aliyun.com/anaconda/cloud
  simpleitk: http://mirrors.aliyun.com/anaconda/cloud
```

查看已安装通道
conda config --show channels

更换源：栗子是清华大学的通道
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/

删除某个通道
conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/

# 恢复默认源
conda config --remove-key channels

# 显示镜像源
conda config --show-sources

# 清华源
conda config --add channels https://pypi.tuna.tsinghua.edu.cn/simple/
# 设置搜索时显示通道地址
conda config --set show_channel_urls yes

# 阿里源
conda config --add channels https://mirrors.aliyun.com/pypi/simple/

# 豆瓣源
conda config --add channels http://pypi.douban.com/simple/ 

# 中科大源
conda config --add channels https://pypi.mirrors.ustc.edu.cn/simple/

# 删除镜像源
conda config --remove channels https://pypi.mirrors.ustc.edu.cn/simple/

# 安装第三方包临时指定镜像源
pip install numpy -i channels
pip install numpy -i https://mirrors.aliyun.com/pypi/simple/

# 确认配置
conda config --set show_channel_urls yes





