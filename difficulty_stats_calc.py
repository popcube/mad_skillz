#################################
## parameter format YYYY/MM/DD ##
#################################

import datetime
import os, sys
from matplotlib import pyplot as plt

def get_data(idx, keyword):
    global data
    global key_data

    Res_data = {}
    for key in key_data:
        Res_data[key] = 0
    
    for i in range(len(data[idx:])):
        dif_temp = data[idx:][i][keyword]
        Res_data[dif_temp] += 1

    Res_data = dict(sorted(Res_data.items()))
    
    return Res_data

def read_time(s):
    return datetime.datetime.strptime(s, "%Y/%m/%d")

# plt.rcParams["font.family"] = "sans-serif"
# plt.rcParams["font.sans-serif"] = ["Meiryo"]

fname = "20220514_data.csv"
figfoler = "./docs/figs/latest"
data = []
csv_key_data = ["No", "default index", "type", "name", "unit", "E", "N", "H", "EX", "M", "EX notes", "M notes", "time", "BPM", "MV", "MV personnel", "release date"]

with open(fname, "r", encoding='utf-8') as f:
    data_temp = f.readlines()
    
    for i, line in enumerate(data_temp):
        temp_dic = dict(zip(csv_key_data, line.rstrip("\n").split(",")))
        
        if len(temp_dic) != len(csv_key_data):
            print("###ERROR!###", temp_dic)
            
        data.append(temp_dic)

key_data_max = max([line["M"] for line in data])
print("key_data_max", key_data_max)

## song difficulty key list 21-34
## for master, 26-34
key_data = [str(i) for i in range(26, 36 + 1)]

## sort data from newest to oldest
data.sort(key=lambda x: read_time(x["release date"]), reverse=True)

## アップデート v1.12.0時は2021/12/24
## 最初から読みたい場合はずっと昔の日時を指定する
if len(sys.argv) == 2:
  oldest_time = read_time(sys.argv[1])
else:
  print("only one parameter (YYYY/mm/dd) must be provided")
  sys.exit(1)

time_str_list = [d["release date"] for d in data]

## get the dating-back timetable list value at zero index or oldest_time
oldest_time = next((read_time(s) for s in time_str_list if read_time(s) < oldest_time), oldest_time)
print("oldest time: " + oldest_time.strftime("%Y%m%d"))

data_offset_idx = 0

# グラフの縦軸の最大値は使いまわす
ytick_max = max(get_data(0, "M").values())

os.makedirs(figfoler, exist_ok=True)

while read_time(data[data_offset_idx]["release date"]) >= oldest_time and data_offset_idx < len(data):
    # kill while loop: remove to make while loop function
    if read_time(data[data_offset_idx + 1]["release date"]) >= oldest_time and data_offset_idx + 1 < len(data):
        data_offset_idx += 1
        continue

    Exp_data = {}
    Mas_data = {}
    All_data = {}

    Mas_data = get_data(data_offset_idx, "M")
    date_text = data[data_offset_idx]["release date"]
    song_text = data[data_offset_idx]["name"]
    if song_text == "Hello world!": song_text="Hello,World!"
    print()
    print(date_text, song_text)
    
    # data_offset_idx += 1
    # if data_offset_idx >= len(data): break
    # continue

    # print(sum([Mas_data[s] for s in key_data]))

    mad_skillz_dist = [[0 for k in key_data] for j in range(10 + 1)]
    Mas_tot_num = sum([Mas_data[s] for s in key_data])

    ## テーブル用データ
    mad_skillz_stats = [["", ""] for i in range(10)]

    ## 今の場所を指すポインタ　[楽曲レベル、曲数]
    temp_diff_pos = [0, 0]
    for i in range(11):
        diff_song_num = 10
        if i==0: diff_song_num *= 3
        if i==10: diff_song_num = Mas_tot_num + 1
        
        ## numbering variable
        song_num = diff_song_num
        
        while song_num > 0 and temp_diff_pos[0] < len(key_data):
            if Mas_data[key_data[temp_diff_pos[0]]] != temp_diff_pos[1]:
                temp_diff_pos[1] += 1
                song_num -= 1
            else:
                ## 前の難易度からの繰り越しがある場合
                if sum(mad_skillz_dist[i][:temp_diff_pos[0]]) > 0:
                    mad_skillz_dist[i][temp_diff_pos[0]] = Mas_data[key_data[temp_diff_pos[0]]]
                ## 繰り越しがない場合
                else:
                    mad_skillz_dist[i][temp_diff_pos[0]] = diff_song_num - song_num
                ## 楽曲レベﾙポインタを次の楽曲レベルに向けて初期化
                temp_diff_pos = [temp_diff_pos[0]+1, 0]
        
        ## 楽曲レベルポインタがカンストしていないとき
        if temp_diff_pos[0] < len(key_data):
            ## 数え終わり時の処理
            ## 前の難易度からの繰り越しがある場合
            if sum(mad_skillz_dist[i][:temp_diff_pos[0]]) > 0:
                # print(i, temp_diff_pos)
                mad_skillz_dist[i][temp_diff_pos[0]] = temp_diff_pos[1]
            ## 繰り越しがない場合
            else:
                mad_skillz_dist[i][temp_diff_pos[0]] = diff_song_num
            ## その皆伝レベルのデータを格納
            mad_skillz_stats[i] = [key_data[temp_diff_pos[0]], temp_diff_pos[1]]

    print(*mad_skillz_dist)
    print(*mad_skillz_stats)

    # exit(0)
    p=[0, 0, 0]
    bar_color = ["#BB33EE", "k"]

    fig, axes = plt.subplots(2, 1,figsize = (10, 5), sharex=True)        

    p[0] = axes[0].bar(key_data, Mas_data.values(), width=0.5, color = bar_color[0], label="MASTER")

    y_offset = [0 for k in key_data]
    ms_cm = plt.cm.get_cmap("Set3", 12)
    for i in range(11):
        p[1] = axes[1].bar(key_data, mad_skillz_dist[i],
            bottom=y_offset, width=0.5,
            color=ms_cm.colors[i], label="Mad Skill")
        y_offset = [y_offset[j] + mad_skillz_dist[i][j] for j in range(len(key_data))]


    for i in range(2):
        axes[i].set_yticks(range(0, ytick_max, 10))
        axes[i].set_ylim(0, ytick_max+10)
        axes[i].grid(True, axis='y', linestyle='-')
        axes[i].set_ylabel("no. of songs")
        axes[i].bar_label(p[i])
        axes[i].text(len(key_data)-0.5, axes[i].get_ylim()[1]-10,
            axes[i].get_legend_handles_labels()[1][0],
            color="white",
            backgroundcolor=bar_color[i],
            ha="right", va="top")
        box = axes[i].get_position()
        axes[i].set_position([box.x0, box.y0, box.width, box.height * 1.5])
    #    axes[i].autoscale()

    ms_table = plt.table(cellText=list(zip(*mad_skillz_stats)),
                          colLabels=range(1, 11),
                          colColours=ms_cm.colors[1:],
                          rowLabels=["song level", "no. of songs"],
                          bbox = [0, -1.3, 1, 0.7],
                          label="mad skill level")

    plt.subplots_adjust(left=0.2, bottom=0.35)
    plt.title("皆伝称号に必要な楽曲レベルと曲数", y=-0.5, fontname="IPAexGothic")
    # plt.title("mad skill required song number and levels", y=-0.5)

    plt.gcf().text(0.05, 0.9,
        f"{date_text}\n{len(data)-data_offset_idx} songs",
        backgroundcolor="#FFFF66")
    
    plt.gcf().text(0.95, 0.95,
        f"latest song\n{song_text}",
        fontname="IPAexGothic",
        backgroundcolor="#FFFF66",
        ha="right", va="top")

    figpath = figfoler + "/" + date_text.replace("/","_") + ".png"
    if os.path.exists(figpath):
        os.remove(figpath)
    
    plt.savefig(figpath)
    plt.close()
    
    ## 次の日付へ　必ずループ内最後に行うこと
    data_offset_idx += 1
    if data_offset_idx >= len(data): break


# fig.tight_layout()
# plt.show()


