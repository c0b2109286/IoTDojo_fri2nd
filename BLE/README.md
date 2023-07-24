# explanation
## Overview
`relay01_dev`，`relay02_dev`，`senser_dev`それぞれをESP32で実行することでBLEマルチホップ通信が可能です．

### relay01_dev
中継器として`senser_dev`から受信したデータを`relay01_dev`へ送信したり，経路データから経路表を作成します．
### relay02_dev
中継器として`relay01_dev`から受信したデータをサーバへ送信します．
### senser_dev
送信機としてセンサーでデータを取得したり，取得データを`relay01_dev`へ送信したりします．また，経路データから経路表の作成をします．
## MindMap
<img src="pic/mindmap.png" width="700">
