

from matplotlib import pyplot as plt
from matplotlib import transforms as tr

fname = "楽曲一覧_20220312_ANSI.csv"
data = []
key_data = ["No", "default index", "type", "name", "unit", "E", "N", "H", "EX", "M", "EX notes", "M notes", "time", "BPM", "MV", "MV personnel", "release date"]
## data形式
## [0 ,1  ,2  ,3  ,4   ,5,6,7,8 ,9,10      ,11,     ,12 ,13 ,14,15 ,16  ] 
## [No,デフォ,種別,曲名,ユニット,E,N,H,EX,M,EX Combo,M Coombo,時間,BPM,MV,人数,配信日]

with open(fname, "r") as f:
    data_temp = f.readlines()
    
    for i, line in enumerate(data_temp):
        temp_dic = dict(zip(key_data, line.rstrip("\n").split(",")))
        
        if len(temp_dic) != len(key_data):
            print("###ERROR!###", temp_dic)
            
        data.append(temp_dic)

key_data = [str(i) for i in range(22, 34 + 1)]
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

Exp_data = get_data(key_data, "EX")
Mas_data = get_data(key_data, "M")
for key in key_data:
    All_data[key] = Exp_data[key] + Mas_data[key]
All_accum_data = [sum(list(All_data.values())[:i+1])/sum(list(All_data.values())) for i in range(len(All_data))]

print(All_accum_data)
print(sum([int(Exp_data[s]) for s in key_data]))
print(sum([int(Mas_data[s]) for s in key_data]))
print(sum([int(All_data[s]) for s in key_data]))

fig, axes = plt.subplots(4, 1,figsize = (10, 7), sharex=True)
p=[0, 0, 0]

bar_color = ["#EE4466", "#BB33EE", "k"]
p[0] = axes[0].bar(key_data, Exp_data.values(), width=0.5, color = bar_color[0], label="EXPERT")
p[1] = axes[1].bar(key_data, Mas_data.values(), width=0.5, color = bar_color[1], label="MASTER")
p[2] = axes[2].bar(key_data, All_data.values(), width=0.5, color = bar_color[2], label="ALL")

for i in range(3):
    axes[i].set_yticks(range(0, max(All_data.values()), 10))
    axes[i].set_ylim(0, max(All_data.values())+10)
    axes[i].grid(True, axis='y', linestyle='-')
    axes[i].set_ylabel("number of\nsongs")
    axes[i].bar_label(p[i])
    axes[i].text(len(key_data)-0.5, axes[i].get_ylim()[1]-10, axes[i].get_legend_handles_labels()[1][0]\
        , color="white", backgroundcolor=bar_color[i], ha="right", va="top")

axes[3].plot(key_data, All_accum_data, color="k", label="All cumulative", linewidth=0.5, marker="o")
axes[3].grid(True, axis='y', linestyle='-')
axes[3].set_ylim(0, 1.3)
axes[3].set_yticks([i*0.25 for i in range(5)])
axes[3].set_yticklabels([str(i*25) for i in range(5)])
axes[3].set_ylabel("cumulative %")
for i in range(len(key_data)):
    axes[3].text(i, All_accum_data[i], f'{All_accum_data[i]*100:.1f}', size=12, ha="center", va="bottom")

axes[3].set_xlabel("difficulty level")
axes[3].text(len(key_data)-0.5, axes[3].get_ylim()[1]-0.5, axes[3].get_legend_handles_labels()[1][0]\
    , bbox=dict(edgecolor="k", facecolor="white"), ha="right", va="top")

print(All_accum_data[len(All_accum_data)-1])
for i in range(len(key_data)):
    if i==0: continue
    if All_accum_data[i] - All_accum_data[i-1] != list(All_data.values())[i]/340.0:
        print(All_accum_data[i] - All_accum_data[i-1])
        print(list(All_data.values())[i]/340.0)
        
#print(list(axes[0].set_xticks(key_data)[0]))
#axes[3].set_xticks(key_data)
fig.tight_layout()
plt.show()


