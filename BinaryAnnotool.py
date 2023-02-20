import sys
import os
import argparse
import cv2
import glob

parser=argparse.ArgumentParser()
parser.add_argument('-mp4_path')
parser.add_argument('-save')
parser.add_argument('-game_name')
parser.add_argument('-rate')

def mp4_2_jpg(target_path,rate:int=20):
    video_path=target_path
    save_jpg_path='./Data/images/'+game_name
    if not os.path.exists(save_jpg_path):
        os.mkdir(save_jpg_path)
    cap = cv2.VideoCapture(video_path)


    width=cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    num_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    fps=cap.get(cv2.CAP_PROP_FPS)

    count=0
    while True:
        ret,frame=cap.read() #フレームがあるならret=True,ないとFalse
        if ret==True:
            #指定フレームごとに画像を生成
            if count%rate==0:
                path=os.path.join(save_jpg_path,'frame_{:06d}.jpg'.format(count+1))
                cv2.imwrite(path,frame)
            count+=1
        else:
            break
    return save_jpg_path


## マウス処理 
def onMouse(event,x,y,flag,params):
    """
    左クリック : ポイントを追加
    右クリック : ポイント削除
    Enter     : 次の画像へ
    """
    
    
    
    raw_img=params["img"]
    wname=params["wname"]
    point_list=params["point_list"]
    now_img=params["now_img"]
    total_imgs=params["total_img"]
    ##クリックイベント
    ##左クリックでポイント追加
    if event == cv2.EVENT_LBUTTONDOWN:
        point_list.append([x,y])
    ##右クリックでポイント削除
    if event==cv2.EVENT_RBUTTONDOWN:
        point_list.pop(-1)
    
    #レーダーの作成、描画
    img=raw_img.copy()
    h,w=img.shape[0],img.shape[1]
    cv2.line(img,(x,0),(x,h),(255,0,0),1)
    cv2.line(img,(0,y),(w,y),(255,0,0),1)
    
    ##点、線の描画
    for i in range(len(point_list)):
        #各ポイントリストの座標を取得
        cv2.circle(img,(point_list[i][0],point_list[i][1]),3,(0,0,255),3)
        if 0<i:
            cv2.line(img, (point_list[i][0], point_list[i][1]),
                     (point_list[i-1][0], point_list[i-1][1]), (0, 255, 0), 2)
    if 0<len(point_list):
        cv2.line(img, (x, y),
                     (point_list[len(point_list)-1][0], point_list[len(point_list)-1][1]), (0, 255, 0), 2)
    
    #座標情報をテキストで出力
    cv2.putText(img,"({0},{1})".format(x,y),(0,20),cv2.FONT_HERSHEY_PLAIN,1,(255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(img,"{}/{} Imgs".format(now_img+1,total_imgs),(0,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 200), 2, cv2.LINE_AA)
    cv2.imshow(wname, img)

    
    
 
##取得した座標情報を保存
def save_point_list(path,point_list):
    f=open(path,"w")
    for p in point_list:
        f.write(str(p[0])+","+str(p[1])+"\n")
    f.close()

def main(save_jpg_path,save_anno_path,game_name,rate:int=20):
    PATH=save_jpg_path+'/*'
    PATH=sorted(glob.glob(PATH))
    
    for i,path in enumerate(PATH):
        #画像の読み込み
        print(path)
        img=cv2.imread(path)
        #諸々設定
        wname="MouseEvent"
        point_list=[]
        frame=i*rate+1
        total_img=len(PATH)
        params={"img":img,
                "wname":wname,
                "point_list": point_list,
                "now_img":i,
            "total_img":total_img
            }
                
        #main
        cv2.namedWindow(wname,cv2.WINDOW_NORMAL)
        cv2.setMouseCallback(wname,onMouse,params)
        cv2.imshow(wname,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        ## 取得したポイントをcsvに保存
        ## game_nameのfolderないなら作成。
        SAVE_ANNO_PATH=save_anno_path+'/'+game_name
        if not os.path.exists(SAVE_ANNO_PATH):
            os.mkdir(SAVE_ANNO_PATH)
        csv_path=os.path.join(SAVE_ANNO_PATH,'frame_{:06d}.csv'.format(frame))
        if len(point_list) !=0:
            save_point_list(csv_path, point_list)
            print("Save csv file:", csv_path)
        


if __name__=="__main__":
    args=parser.parse_args()
    target_path=args.mp4_path
    save_anno_path=args.save
    game_name=args.game_name
    rate=int(args.rate)

    save_jpg_path=mp4_2_jpg(target_path,rate)
    main(save_jpg_path,save_anno_path,game_name,rate)