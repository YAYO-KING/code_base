Selenium-Server-Standalone搭建  离线的远程selenium
相比于各种浏览器Driver，RemoteWebDriver提供了控制远程浏览器能力，通过搭配Selenium-Server-standalone的服务，彻底将浏览器和测试代码分离。核心思想是：客户端代码通过RemoteWebDriver，发送浏览器操作至远程机器上的server服务，间接的操作浏览器。

使用：
https://blog.csdn.net/GAMEloft9/article/details/81017262

下载地址：
https://selenium-release.storage.googleapis.com/index.html

java -jar selenium-server-standalone-2.x.x.jar


google驱动下载：
http://chromedriver.storage.googleapis.com/index.html
https://googlechromelabs.github.io/chrome-for-testing/#stable


使用selenium的remote WebDriver
https://www.w3cschool.cn/selenium2/selenium2-mons3g7w.html
