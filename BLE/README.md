# explanation
## Overview
`relay01_dev`，`relay02_dev`，`senser_dev`それぞれをESP32で実行することでBLEマルチホップ通信が可能です.  
また，`demo_server`を自身のコードエディタの環境内で実行することでFlaskサーバを立ててデータを受け取り，  
そのデータをhtmlに埋め込むことで確認することが出来ます．
### [relay01_dev](https://github.com/Fel615/IoTDojo_fri2nd/tree/main/BLE/relay01_dev)
中継器として`senser_dev`から受信したデータを`relay01_dev`へ送信したり，経路データから経路表を作成します．
### [relay02_dev](https://github.com/Fel615/IoTDojo_fri2nd/tree/main/BLE/relay02_dev)
中継器として`relay01_dev`から受信したデータをサーバへ送信します．
### [senser_dev](https://github.com/Fel615/IoTDojo_fri2nd/tree/main/BLE/senser_dev)
送信機としてセンサーでデータを取得したり，取得データを`relay01_dev`へ送信したりします．  
また，経路データから経路表の作成をします．
### [demo_server](https://github.com/Fel615/IoTDojo_fri2nd/tree/main/BLE/demo_server)
Flaskサーバを立ち上げ，`relay02_dev`からデータを受け取ります．  
また，データをテンプレートのhtml`view.html`に埋め込むことでwebページとして閲覧が可能になります．
## MindMap
<img src="pic/mindmap.png" width="700">
