from matplotlib import pyplot as plt

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Meiryo"]

fname = "楽曲一覧_20220312_ANSI.csv"
data = []
csv_key_data = ["No", "default index", "type", "name", "unit", "E", "N", "H", "EX", "M", "EX notes", "M notes", "time", "BPM", "MV", "MV personnel", "release date"]
## data形式
## [0 ,1  ,2  ,3  ,4   ,5,6,7,8 ,9,10      ,11,     ,12 ,13 ,14,15 ,16  ] 
## [No,デフォ,種別,曲名,ユニット,E,N,H,EX,M,EX Combo,M Coombo,時間,BPM,MV,人数,配信日]

with open(fname, "r") as f:
    data_temp = f.readlines()
    
    for i, line in enumerate(data_temp):
        temp_dic = dict(zip(csv_key_data, line.rstrip("\n").split(",")))
        
        if len(temp_dic) != len(csv_key_data):
            print("###ERROR!###", temp_dic)
            
        data.append(temp_dic)

## song difficulty key list 22-34
## for master, 26-34
key_data = [str(i) for i in range(26, 34 + 1)]

Exp_data = {}
Mas_data = {}
All_data = {}

def get_data(key_list, keyword):
    global data
    Res_data = {}
    for key in key_data:
        Res_data[key] = 0
    
    for i in range(len(data)):
        dif_temp = data[i][keyword]
        Res_data[dif_temp] += 1

    Res_data = dict(sorted(Res_data.items()))
    
    return Res_data

Mas_data = get_data(key_data, "M")
date_text = data[0]["release date"]
print(date_text)

# print(sum([Mas_data[s] for s in key_data]))

mad_skillz_dist = [[0 for k in key_data] for j in range(10 + 1)]
Mas_tot_num = sum([Mas_data[s] for s in key_data])

## テーブル用データ
mad_skillz_stats = []

## 今の場所を指すポインタ　[難易度、曲数]
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
            ## ポインタを次の難易度レベルに向けて初期化
            temp_diff_pos = [temp_diff_pos[0]+1, 0]
    
    if i != 10:
        ## 数え終わり時の処理
        ## 前の難易度からの繰り越しがある場合
        if sum(mad_skillz_dist[i][:temp_diff_pos[0]]) > 0:
            # print(i, temp_diff_pos)
            mad_skillz_dist[i][temp_diff_pos[0]] = temp_diff_pos[1]
        ## 繰り越しがない場合
        else:
            mad_skillz_dist[i][temp_diff_pos[0]] = diff_song_num
        ## その皆伝レベルのデータを格納
        mad_skillz_stats.append([key_data[temp_diff_pos[0]], temp_diff_pos[1]])

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
    p[1] = axes[1].bar(key_data, mad_skillz_dist[i], bottom=y_offset, width=0.5, color=ms_cm.colors[i], label="Mad Skill")
    y_offset = [y_offset[j] + mad_skillz_dist[i][j] for j in range(len(key_data))]


for i in range(2):
    axes[i].set_yticks(range(0, max(Mas_data.values()), 10))
    axes[i].set_ylim(0, max(Mas_data.values())+10)
    axes[i].grid(True, axis='y', linestyle='-')
    axes[i].set_ylabel("number of\nsongs")
    axes[i].bar_label(p[i])
    axes[i].text(len(key_data)-0.5, axes[i].get_ylim()[1]-10, axes[i].get_legend_handles_labels()[1][0]\
        , color="white", backgroundcolor=bar_color[i], ha="right", va="top")
    box = axes[i].get_position()
    axes[i].set_position([box.x0, box.y0, box.width, box.height * 1.5])
#    axes[i].autoscale()

ms_table = plt.table(cellText=list(zip(*mad_skillz_stats)),
                      colLabels=range(1, 11),
                      colColours=ms_cm.colors[1:],
                      rowLabels=["difficulty level", "no. of songs"],
                      bbox = [0, -1.3, 1, 0.7],
                      label="mad skill level")

plt.subplots_adjust(left=0.2, bottom=0.35)
plt.title("皆伝称号に必要な難易度レベルと曲数", y=-0.5)
# plt.title("mad skill required song number and levels", y=-0.5)

plt.gcf().text(0.05, 0.9, date_text)


# fig.tight_layout()
plt.show()


