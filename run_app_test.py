import streamlit as st
import pandas as pd
import os
from data_obtain import CP_grapher
import matplotlib.pyplot as plt

# タイトル
st.title('複数データを管理するアプリ')
fig, ax = plt.subplots()
st.session_state['general_plot_settings'] = {}

# データフォルダのリストの初期化
if 'data_folders' not in st.session_state:
    st.session_state['data_folders'] = []
    st.session_state['plot_settings'] = []
    st.session_state['line'] = []
    st.session_state['data'] = []
    st.session_state['linewidth'] = []
    st.session_state['legend'] = []
    st.session_state['x_min_lim'] = 0
    st.session_state['x_max_lim'] = 1
    st.session_state['y_min_lim'] = 0
    st.session_state['y_max_lim'] = 0

# サイドバーにCVかCPの選択メニューを追加
plot_type = st.sidebar.selectbox('プロットタイプを選択', ['CP', 'CV'])

# サイドバーにフォルダ選択ウィジェットを追加
folder = st.sidebar.text_input('データフォルダのパスを入力', '')

# フォルダ追加ボタン
if st.sidebar.button('フォルダを追加'):
    if os.path.isdir(folder):
        st.session_state['data_folders'].append(folder)
        st.session_state['plot_settings'].append({
            'color': 'Black',  # デフォルトの色
        })
        st.session_state['line'].append({
            'line_type': '-',
        })
        st.session_state['linewidth'].append({
            'line_width': 3,
        })
        st.session_state['legend'].append('')  # デフォルトのレジェンド
    else:
        st.sidebar.error('無効なフォルダパスです。')

# アップロードされたフォルダの一覧を表示
st.sidebar.write('追加されたフォルダ:')
for i, folder in enumerate(st.session_state['data_folders']):
    # folderの最後のディレクトリ名を取得
    folder_name = os.path.basename(folder)
    st.sidebar.write(folder_name)
    
    # プロット設定（色）をサイドバーで選択
    preset_colors = ['black', 'blue', 'orange', 'green', 'red', 'violet', 'brown']
    color_choice = st.sidebar.radio(f'フォルダ {i+1} の色を選択', preset_colors, index=0, key=f'color_choice_{i}', horizontal=True)
    preset_types = ["-", "--", "-.", ":"]
    line_choice = st.sidebar.radio(f'フォルダ {i+1} のラインタイプを選択', preset_types, index=0, key=f'line_choice_{i}', horizontal=True)
    # linewidthをテキストボックスで選択
    st.session_state['linewidth'][i]['line_width'] = st.sidebar.number_input('ライン幅を選択', min_value=1, max_value=10, value=3, key=f'line_width_{i}')

    # レジェンドをテキストボックスで入力
    st.session_state['legend'][i] = st.sidebar.text_input(f'フォルダ {i+1} のレジェンドを入力', value=folder_name, key=f'legend_{i}')

    st.session_state['plot_settings'][i]['color'] = color_choice
    st.session_state['line'][i]['line_type'] = line_choice

    data = CP_grapher(folder)
    st.session_state['data'].append(data)
    
    # データ範囲を更新
    st.session_state['x_min_lim'] = min(st.session_state['x_min_lim'], data["time/s"].min())
    st.session_state['x_max_lim'] = max(st.session_state['x_max_lim'], data["time/s"].max())
    st.session_state['y_min_lim'] = min(st.session_state['y_min_lim'], data["Ewe/V"].min())
    st.session_state['y_max_lim'] = max(st.session_state['y_max_lim'], data["Ewe/V"].max())

    st.sidebar.divider()

if plot_type == 'CP':
    # 軸ラベルと範囲の設定
    xlabel = st.text_input('x軸のラベルを入力', r'time/s^{1/2}')
    ylabel = st.text_input('y軸のラベルを入力', r'E_{we}/V')
    x_min = st.number_input('x軸の最小値を入力', value=st.session_state['x_min_lim'])
    x_max = st.number_input('x軸の最大値を入力', value=st.session_state['x_max_lim'])
    y_min = st.number_input('y軸の最小値を入力', value=st.session_state['y_min_lim'])
    y_max = st.number_input('y軸の最大値を入力', value=st.session_state['y_max_lim'])

    # st.session_state['data']にデータがある場合、データをプロット
    for i, data in enumerate(st.session_state['data_folders']):
        ax.plot(
            st.session_state['data'][i]["time/s"], 
            st.session_state['data'][i]["Ewe/V"], 
            color=st.session_state['plot_settings'][i]['color'], 
            linestyle=st.session_state['line'][i]['line_type'], 
            linewidth=st.session_state['linewidth'][i]['line_width'], 
            label=st.session_state['legend'][i]
        )

    # グラフの設定を適用
    ax.set_xlabel(f'${xlabel}$')
    ax.set_ylabel(f'${ylabel}$')
    ax.set_xlim([x_min, x_max])
    ax.set_ylim([y_min, y_max])
    ax.invert_yaxis()
    ax.legend()  # レジェンドを表示
    st.pyplot(fig)

    if not st.session_state['data_folders']:
        st.write('データを追加してください。')

elif plot_type == 'CV':
    st.write('CVプロット')
