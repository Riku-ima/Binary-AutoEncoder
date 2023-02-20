# Binary-AutoEncoder

<参考論文>
[Classification of Basketball Actions through Deep Learning Techniques](https://www.researchgate.net/publication/330534530_Classificazione_di_Azioni_Cestistiche_mediante_Tecniche_di_Deep_Learning)

コート領域の検出を行う。

BinaryAnnotool.py 
-> コートの矩形を選択し、座標を保存するためのアノテーションツール
makemask.ipynb
-> csvから画像を白黒にマスク
MyAutoEncoder.ipynb
-> モデルの作成、学習

**BinaryAnnotool.py の実行画面**
![https___qiita-image-store s3 ap-northeast-1 amazonaws com_0_2778523_2f403618-5594-533d-251a-ca160cc75bbd](https://user-images.githubusercontent.com/61176769/220056513-d0623091-3f4b-4061-b7e1-88c4a73d1c0b.jpg)

右クリックで点追加、左クリックで削除。enterで次の画像へ



**モデル実行結果**
![https___qiita-image-store s3 ap-northeast-1 amazonaws com_0_2778523_e73a16ff-3be6-92da-d75e-f6023d0bc033](https://user-images.githubusercontent.com/61176769/220056639-d45d7b06-634d-484d-84f2-24e235c9aaaa.jpg)
