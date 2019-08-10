# LiveEarth!

## Introduction
- 实时动态更新地球壁纸！
- 地球照片抓自日本[himawari-8](http://himawari8.nict.go.jp/)气象卫星官网
- 默认每一小时抓取一次
- 不到50行的python代码
- 感谢 [bitdust](https://github.com/bitdust) 提供的idea

## Screenshots
<img src='http://files.cnblogs.com/files/mrpod2g/earth1.gif' width='500' />
<img src='http://files.cnblogs.com/files/mrpod2g/earth2.gif' width='500' />
<img src='http://files.cnblogs.com/files/mrpod2g/earth3.gif' width='500' />

## 更新
- 1.将LiveEarth.py更名为LiveEarth(wqpod2g版).py
- 2.添加了win版本下的托盘 并将通过拼接实现下载一张1100*1100的图片(原代码图片分辨率为550*550)

##说明
- live_earth.pyw为获取最新卫星图像版本
- live_earth2.pyw为获取东8区对应卫星图片达卫星图片与东8区时间吻合的效果(中午12点全亮,半夜十二点全黑),会比最新的卫星图片时间早约一个半小时
