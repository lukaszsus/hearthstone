import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from plotter.through_all import _get_basic_data_from_outcomes

SRC_DIR = '../outcomes_summaries/session_20190402_dodatkowy_backpropagate/'
#SRC_LAST_DIR = '../outcomes_summaries/session_20190402_dodatkowy_backpropagate/i_RANDOM_2019-04-04-001720_summary/'
DST_DIR = '../plots/'


def _get_mean_stat_per_move_from_all_dirs(stat_name: str, file_name: str):
    dirs = os.listdir(SRC_DIR)
    dirs.sort()
    column_data = list()
    for dir in dirs:
        file_path = os.path.join(SRC_DIR, dir)
        file_path = os.path.join(file_path, file_name)
        data = pd.read_csv(file_path)
        moves = data["move"].values

        for i in range(len(moves)):
            if moves[i] % 2 == 0:
                moves[i] += 1

        data["move"] = np.asarray(moves).transpose()

        aval_moves = data["move"].unique()
        means = list()
        for move in aval_moves:
            move_data = data[data["move"] == move]
            means.append(np.mean(move_data[stat_name].values))
        column_data.append(np.asarray(means))
    return column_data


def plot_mean_depths():
    data = _get_basic_data_from_outcomes()
    stats = _get_mean_stat_per_move_from_all_dirs("mean", "leaves.csv")
    filtered = data[data['czas [warunek petli]'] == 1000]
    indices = filtered.index[filtered['przeciwnik'] == 'CONTROLLING'].tolist()
    stats = stats[int(indices[0])]

    to_plot = pd.DataFrame(columns=["ruch", "srednia glebokosc liscia"])
    to_plot["ruch"] = np.asarray(range(len(stats))).transpose()
    to_plot["srednia glebokosc liscia"] = np.asarray(stats).transpose()
    dst_data_path = os.path.join(DST_DIR, "srednia.csv")
    to_plot.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="ruch", y="srednia glebokosc liscia", data=to_plot)
    ax.set_title('Srednia glebokosc liscia od ruchu')
    path_pdf = os.path.join(DST_DIR, "srednia_glebokosc_liscia.pdf")
    path_png = os.path.join(DST_DIR, "srednia_glebokosc_liscia.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


def plot_median_depths():
    data = _get_basic_data_from_outcomes()
    stats = _get_mean_stat_per_move_from_all_dirs("median", "leaves.csv")
    filtered = data[data['czas [warunek petli]'] == 1000]
    indices = filtered.index[filtered['przeciwnik'] == 'CONTROLLING'].tolist()
    stats = stats[int(indices[0])]

    to_plot = pd.DataFrame(columns=["ruch", "mediana glebokosci liscia"])
    to_plot["ruch"] = np.asarray(range(len(stats))).transpose()
    to_plot["mediana glebokosci liscia"] = np.asarray(stats).transpose()
    dst_data_path = os.path.join(DST_DIR, "mediana.csv")
    to_plot.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="ruch", y="mediana glebokosci liscia", data=to_plot)
    ax.set_title('Mediana glebokosci liscia od ruchu')
    path_pdf = os.path.join(DST_DIR, "mediana_glebokosci_liscia.pdf")
    path_png = os.path.join(DST_DIR, "mediana_glebokosci_liscia.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


def plot_max_depths():
    data = _get_basic_data_from_outcomes()
    stats = _get_mean_stat_per_move_from_all_dirs("max", "leaves.csv")
    filtered = data[data['czas [warunek petli]'] == 1000]
    indices = filtered.index[filtered['przeciwnik'] == 'CONTROLLING'].tolist()
    stats = stats[int(indices[0])]

    to_plot = pd.DataFrame(columns=["ruch", "srednia glebokosc liscia"])
    to_plot["ruch"] = np.asarray(range(len(stats))).transpose()
    to_plot["maksymalna glebokosc liscia"] = np.asarray(stats).transpose()
    dst_data_path = os.path.join(DST_DIR, "max.csv")
    to_plot.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="ruch", y="maksymalna glebokosc liscia", data=to_plot)
    ax.set_title('Maksymalna glebokosc liscia od ruchu')
    path_pdf = os.path.join(DST_DIR, "max_glebokosc_liscia.pdf")
    path_png = os.path.join(DST_DIR, "max_glebokosc_liscia.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


def plot_playouts():
    data = _get_basic_data_from_outcomes()
    stats = _get_mean_stat_per_move_from_all_dirs("num_playouts", "playouts.csv")
    filtered = data[data['czas [warunek petli]'] == 1000]
    indices = filtered.index[filtered['przeciwnik'] == 'CONTROLLING'].tolist()
    stats = stats[int(indices[0])]

    to_plot = pd.DataFrame(columns=["ruch", "srednia liczba playoutow"])
    to_plot["ruch"] = np.asarray(range(len(stats))).transpose()
    to_plot["srednia liczba playoutow"] = np.asarray(stats).transpose()
    dst_data_path = os.path.join(DST_DIR, "playouts.csv")
    to_plot.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="ruch", y="srednia liczba playoutow", data=to_plot)
    ax.set_title('Srednia liczba playoutow od ruchu')
    path_pdf = os.path.join(DST_DIR, "playouts.pdf")
    path_png = os.path.join(DST_DIR, "playouts.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')



def plot_exploration_rate():
    data = _get_basic_data_from_outcomes()
    stats = _get_mean_stat_per_move_from_all_dirs("expl_rate", "nodes_exploration.csv")
    filtered = data[data['czas [warunek petli]'] == 1000]
    indices = filtered.index[filtered['przeciwnik'] == 'CONTROLLING'].tolist()
    stats = stats[int(indices[0])]

    to_plot = pd.DataFrame(columns=["ruch", "sredni stopien eksploracji"])
    to_plot["ruch"] = np.asarray(range(len(stats))).transpose()
    to_plot["sredni stopien eksploracji"] = np.asarray(stats).transpose()
    dst_data_path = os.path.join(DST_DIR, "exploration.csv")
    to_plot.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="ruch", y="sredni stopien eksploracji", data=to_plot)
    ax.set_title('Sredni stopien eksploracji wezla od ruchu')
    path_pdf = os.path.join(DST_DIR, "expl.pdf")
    path_png = os.path.join(DST_DIR, "expl.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')

if __name__ == '__main__':
    #plot_mean_depths()
    #plot_median_depths()
    #plot_max_depths()
    plot_playouts()
    #plot_exploration_rate()