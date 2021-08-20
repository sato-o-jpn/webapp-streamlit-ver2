import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

st.title("上限電圧、下限電圧 プロットApp -Ver2")
st.write("※ Ver2ではCSVのセルの空欄、#VALUE!、#DIV/0! を欠損値として認識し、自動で対象のセルを0埋めします。")
st.write('<span style="color:red;background:pink">"インポートするCSVの注意点"</span>', unsafe_allow_html=True)

img = Image.open("image2.png")
st.image(img, caption="CSVに関する注意事項", use_column_width=True)

uploaded_file = st.file_uploader("CSVファイルのアップロード", type={"csv", "txt"})
if uploaded_file is not None:
    # VALUE や #DIV/0! があれば欠損値として認識させる
    uploaded_df = pd.read_csv(uploaded_file, na_values=["VALUE!", "#DIV/0!"])
#st.write(uploaded_df)

if uploaded_file:

    # メインとなるCSV
    dat1 = uploaded_df
    # 編集用のCSV
    dat2 = uploaded_df
    st.write("アップロードしたCSVファイル")

    if True in dat2.isnull().all(axis=1): 
        st.write("欠損値が見つかりました。欠損値を0で穴埋めします。")
        dat1 = dat1.fillna(0)
        dat2 = dat2.fillna(0)
    else:
        st.write("データは正常です。")

    # アップロードしたCSVファイルを表示
    dat1

    # テキスト入力
    target = st.text_input('特徴量選択（例：ci）')
    
    # テキストを入力したら実行開始
    if target:

        st.write("目的の特徴量を軸に降順にCSVを変換")

        # 特徴量Ciを軸に昇順に変換
        df = dat2.sort_values(target, ascending=False)
        # 選択した特徴量を軸に昇順に変換したCSVを表示
        df
        
        # 変数に格納
        vu = dat1["vu"]
        vl = dat1["vl"]
        time = dat1["time"]

        # 軸となる行数リスト
        column_lis = list(df.iloc[0:20,0])
        #column_lis

        st.write("上限電圧と下限電圧をプロットした画像の表示")

        # 上限電圧と下限電圧の上位20をプロットで表示 
        for i in range(20):
            plt.rcParams['figure.figsize'] = (40, 20)
            fig = plt.figure()
            # プロットは合計13個（最大値がセンター）
            x = column_lis[i] - 6 # 前半6個プロット
            y = column_lis[i] + 7 # 後半6個プロット
            # 上限電圧の折れ線グラフ
            plt.plot(time[x:y], vu[x:y],  'o-', color="red", label="Upper limit voltage")
            # 下限電圧の折れ線グラフ
            plt.plot(time[x:y], vl[x:y], 'o-', color="blue", label="Lower limit voltage")
            # x軸に目盛線を設定
            plt.grid(which = "major", axis = "x", color = "blue", alpha = 0.4, linestyle = "--", linewidth = 1)
            # y軸に目盛線を設定
            plt.grid(which = "major", axis = "y", color = "green", alpha = 0.4, linestyle = "--", linewidth = 1)
            # グラフタイトルの表示とサイズ
            plt.title("feature" + " " + "%02.f"%(i+1) + " " + "rank", fontsize=32)
            # y軸小数点以下2桁表示
            plt.gca().xaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))
            # y軸の値のサイズ
            plt.yticks(fontsize=28)
            # x軸の値のサイズ
            plt.xticks(fontsize=28)
            plt.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0, fontsize=32)
            st.pyplot(fig)