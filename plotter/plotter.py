import os
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


SRC_DIR = '../outcomes_summaries/magiczne_karty/'
SRC_LAST_DIR = '../outcomes_summaries/magiczne_karty/i_RANDOM_2019-04-04-001720_summary/'
DST_DIR = '../plots/'

def plot_num_wins():
    src_file_path = os.path.join(SRC_LAST_DIR, "outcomes.csv")
    data = pd.read_csv(src_file_path)
    data = data.rename(index=str, columns={"mcts_time": "czas [warunek petli]",
                                    "Player2_wins": "wygrane MCTS",
                                    "Player1_strategy": "przeciwnik"})
    dst_data_path = os.path.join(DST_DIR, "wygrane.csv")
    data.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="czas [warunek petli]", y="wygrane MCTS", hue="przeciwnik", data = data)
    ax.set_title('Liczba wygranych MCTS od czasu')
    path_pdf = os.path.join(DST_DIR, "wygrane.pdf")
    path_png = os.path.join(DST_DIR, "wygrane.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


def _get_basic_data_from_outcomes():
    src_file_path = os.path.join(SRC_LAST_DIR, "outcomes.csv")
    data = pd.read_csv(src_file_path)
    data = data.rename(index=str, columns={"mcts_time": "czas [warunek petli]",
                                    "Player2_wins": "wygrane MCTS",
                                    "Player1_strategy": "przeciwnik"})
    return data[["przeciwnik", "czas [warunek petli]"]]


def _get_mean_stat_per_game_from_all_dirs(stat_name: str, file_name: str):
    dirs = os.listdir(SRC_DIR)
    dirs.sort()
    column_data = list()
    for dir in dirs:
        file_path = os.path.join(SRC_DIR, dir)
        file_path = os.path.join(file_path, file_name)
        data = pd.read_csv(file_path)
        aval_games = data["game"].unique()
        means = list()
        for game in aval_games:
            game_data = data[data["game"] == game]
            means.append(np.mean(game_data[stat_name].values))
        column_data.append(np.mean(means))
    return np.asarray(column_data)


def plot_playouts():
    data = _get_basic_data_from_outcomes()
    playouts = _get_mean_stat_per_game_from_all_dirs("num_playouts", "playouts.csv")
    data["srednia liczba playoutow"] = playouts.transpose()
    dst_data_path = os.path.join(DST_DIR, "playouty.csv")
    data.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="czas [warunek petli]", y="srednia liczba playoutow", hue="przeciwnik", data=data)
    ax.set_title('Srednia liczba playoutow od czasu')
    path_pdf = os.path.join(DST_DIR, "playouty.pdf")
    path_png = os.path.join(DST_DIR, "playouty.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


def plot_mean_depths():
    data = _get_basic_data_from_outcomes()
    playouts = _get_mean_stat_per_game_from_all_dirs("mean", "leaves.csv")
    data["srednia glebokosc liscia"] = playouts.transpose()
    dst_data_path = os.path.join(DST_DIR, "srednia_glebokosc_liscia.csv")
    data.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="czas [warunek petli]", y="srednia glebokosc liscia", hue="przeciwnik", data=data)
    ax.set_title('Srednia glebokosc liscia od czasu')
    path_pdf = os.path.join(DST_DIR, "srednia_glebokosc_liscia.pdf")
    path_png = os.path.join(DST_DIR, "srednia_glebokosc_liscia.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


def plot_median_depths():
    data = _get_basic_data_from_outcomes()
    playouts = _get_mean_stat_per_game_from_all_dirs("median", "leaves.csv")
    data["mediana glebokosci liscia"] = playouts.transpose()
    dst_data_path = os.path.join(DST_DIR, "mediana_glebokosci_liscia.csv")
    data.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="czas [warunek petli]", y="mediana glebokosci liscia", hue="przeciwnik", data=data)
    ax.set_title('Mediania glebokosci liscia od czasu')
    path_pdf = os.path.join(DST_DIR, "mediana_glebokosci_liscia.pdf")
    path_png = os.path.join(DST_DIR, "mediana_glebokosci_liscia.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


def plot_max_depths():
    data = _get_basic_data_from_outcomes()
    playouts = _get_mean_stat_per_game_from_all_dirs("max", "leaves.csv")
    data["maksymalna glebokosc liscia"] = playouts.transpose()
    dst_data_path = os.path.join(DST_DIR, "max_glebokosc_liscia.csv")
    data.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="czas [warunek petli]", y="maksymalna glebokosc liscia", hue="przeciwnik", data=data)
    ax.set_title('Maksymalna glebokosc liscia od czasu')
    path_pdf = os.path.join(DST_DIR, "max_glebokosc_liscia.pdf")
    path_png = os.path.join(DST_DIR, "max_glebokosc_liscia.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


def plot_max_depths():
    data = _get_basic_data_from_outcomes()
    playouts = _get_mean_stat_per_game_from_all_dirs("expl_rate", "nodes_exploration.csv")
    data["srednia czesc eksploracji"] = playouts.transpose()
    dst_data_path = os.path.join(DST_DIR, "sr_procent_eksplorowanych.csv")
    data.to_csv(dst_data_path, index=False)

    fig, ax = plt.subplots()
    ax = sns.scatterplot(x="czas [warunek petli]", y="srednia czesc eksploracji", hue="przeciwnik", data=data)
    ax.set_title('Srednia procent(czesc) eksplorowanych dzieci wezlow')
    path_pdf = os.path.join(DST_DIR, "sr_procent_eksplorowanych.pdf")
    path_png = os.path.join(DST_DIR, "sr_procent_eksplorowanych.png")
    fig.savefig(path_pdf, bbox_inches='tight')
    fig.savefig(path_png, bbox_inches='tight')


if __name__ == '__main__':
    plot_num_wins()
    plot_playouts()
    plot_mean_depths()
    plot_median_depths()
    plot_max_depths()
    plot_max_depths()