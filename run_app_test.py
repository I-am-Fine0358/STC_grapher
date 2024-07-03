import streamlit as st
import pandas as pd
import os
from data_obtain import CP_grapher
import plotly.graph_objects as go

# タイトル
st.title('複数データを管理するシンプルなアプリ')

# セッションステートの初期化
if 'data_folders' not in st.session_state:
    st.session_state['data_folders'] = []
if 'data' not in st.session_state:
    st.session_state['data'] = []
if 'plot_colors' not in st.session_state:
    st.session_state['plot_colors'] = []
if 'legends' not in st.session_state:
    st.session_state['legends'] = []
if 'line_types' not in st.session_state:
    st.session_state['line_types'] = []
if 'x_min' not in st.session_state:
    st.session_state['x_min'] = 0.0
if 'x_max' not in st.session_state:
    st.session_state['x_max'] = 10.0
if 'y_min' not in st.session_state:
    st.session_state['y_min'] = 0.0
if 'y_max' not in st.session_state:
    st.session_state['y_max'] = 10.0

# サイドバーにCV / CPの選択欄を追加
plot_type = st.sidebar.selectbox('プロットタイプを選択', ['CP', 'CV'])

# サイドバーにフォルダ選択ウィジェットを追加
folder = st.sidebar.text_input('データフォルダのパスを入力', '')

# フォルダ追加ボタン
if st.sidebar.button('フォルダを追加'):
    if os.path.isdir(folder):
        st.session_state['data_folders'].append(folder)
        data = CP_grapher(folder)
        st.session_state['data'].append(data)
        st.session_state['plot_colors'].append('white')  # デフォルトの色を白に設定
        st.session_state['legends'].append(os.path.basename(folder))  # デフォルトの凡例をフォルダ名に設定
        st.session_state['line_types'].append('solid')  # デフォルトの線の種類を設定
        # 各軸の最小値と最大値を計算
        st.session_state['x_min'] = min(st.session_state['x_min'], data["time/s"].min())
        st.session_state['x_max'] = max(st.session_state['x_max'], data["time/s"].max())
        st.session_state['y_min'] = min(st.session_state['y_min'], data["Ewe/V"].min())
        st.session_state['y_max'] = max(st.session_state['y_max'], data["Ewe/V"].max())
    else:
        st.sidebar.error('無効なフォルダパスです。')

# アップロードされたフォルダの一覧を表示
st.sidebar.write('追加されたフォルダ:')
preset_colors = ['white', 'blue', 'orange', 'green', 'red', 'violet', 'brown']
preset_types = {
    "solid": 'solid',
    "dash": 'dash',
    "dashdot": 'dashdot',
    "dot": 'dot'
}

for i, folder in enumerate(st.session_state['data_folders']):
    st.sidebar.write(f'フォルダ {i+1}: {os.path.basename(folder)}')

    # 色をサイドバーで選択
    color_choice = st.sidebar.selectbox(f'フォルダ {i+1} の色を選択', preset_colors, index=0, key=f'color_choice_{i}')
    st.session_state['plot_colors'][i] = color_choice

    # ラインタイプをサイドバーで選択
    line_choice = st.sidebar.selectbox(f'フォルダ {i+1} のラインタイプを選択', list(preset_types.keys()), index=0, key=f'line_choice_{i}')
    st.session_state['line_types'][i] = preset_types[line_choice]

    # 凡例をサイドバーで入力
    legend_text = st.sidebar.text_input(f'フォルダ {i+1} の凡例を入力', value=st.session_state['legends'][i], key=f'legend_{i}')
    st.session_state['legends'][i] = legend_text

# プロットタイプがCPの場合のみプロットを表示
if plot_type == 'CP':
    # 軸ラベルと範囲の設定
    xlabel = st.text_input('x軸のラベルを入力', 'time/s')
    ylabel = st.text_input('y軸のラベルを入力', 'Ewe/V')
    x_min = st.number_input('x軸の最小値を入力', value=st.session_state['x_min'])
    x_max = st.number_input('x軸の最大値を入力', value=st.session_state['x_max'])
    y_min = st.number_input('y軸の最小値を入力', value=st.session_state['y_min'])
    y_max = st.number_input('y軸の最大値を入力', value=st.session_state['y_max'])

    # グラフのプロット
    fig = go.Figure()

    # st.session_state['data']にデータがある場合、データをプロット
    for i, data in enumerate(st.session_state['data']):
        fig.add_trace(go.Scatter(
            x=data["time/s"], 
            y=data["Ewe/V"],
            mode='lines',
            line=dict(color=st.session_state['plot_colors'][i], dash=st.session_state['line_types'][i]),
            name=st.session_state['legends'][i]
        ))

    # グラフの設定を適用
    fig.update_layout(
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        xaxis=dict(range=[x_min, x_max]),
        yaxis=dict(range=[y_min, y_max]),
        yaxis_autorange='reversed',  # y軸を反転
        plot_bgcolor='black',  # 背景色を黒に設定
        paper_bgcolor='black'  # 背景色を黒に設定
    )

    st.plotly_chart(fig)

if not st.session_state['data_folders']:
    st.write('データを追加してください。')
