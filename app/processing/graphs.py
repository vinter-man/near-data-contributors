import logging
import sys
import matplotlib.pyplot as plt


########################################################################################################################
logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format='[%(asctime)s]:[%(levelname)s]:[%(filename)s]:[%(lineno)d]: %(message)s',
    )


########################################################################################################################
def build_graph(graph_name: str, x, y):
    logger.info(f'Start build graph with: \n\n{x}\n{y}\n')

    picture = plt.figure(
        figsize=(6.4, 4.8),
        dpi=100,
        facecolor='#1e262c',
        edgecolor='#1e262c'
    )
    graph = picture.add_subplot(1, 1, 1)

    graph.grid(
        visible=True,
        which='major',
        axis='both',
        alpha=0.1,
        antialiased=True,
        dash_capstyle='butt'
    )

    graph.set_facecolor('#1e262c')

    graph.tick_params(
        axis='both',
        color='#1e262c',
        labelcolor='#c4c9cd'
    )
    graph.spines['bottom'].set_color('#1e262c')
    graph.spines['top'].set_color('#1e262c')
    graph.spines['right'].set_color('#1e262c')
    graph.spines['left'].set_color('#1e262c')

    graph.fill_between(
        x, y,
        color='#43c4e3',
        alpha=0.10
    )
    graph.plot(
        x, y,
        color='#43c4e3',
        solid_capstyle='round',
        linestyle='solid',
        marker='.',
        markerfacecolor='white',
        markersize=4,
        linewidth=1.5)

    pic_name = f'graphs/{graph_name}.png'
    picture.savefig(pic_name)
    logger.info(f'Graph successfully saved to {pic_name}')
    return pic_name


def build_bar(graph_name: str, width: int, x, y):
    logger.info(f'Start build graph with: \n\n{x}\n{y}\n')

    picture = plt.figure(
        figsize=(6.4, 4.8),
        dpi=100,
        facecolor='#1e262c',
        edgecolor='#1e262c'
    )
    graph = picture.add_subplot(1, 1, 1)

    graph.grid(
        visible=True,
        which='major',
        axis='both',
        alpha=0.1,
        antialiased=True,
        dash_capstyle='butt'
    )

    graph.set_facecolor('#1e262c')

    graph.tick_params(
        axis='both',
        color='#1e262c',
        labelcolor='#c4c9cd'
    )
    graph.spines['bottom'].set_color('#1e262c')
    graph.spines['top'].set_color('#1e262c')
    graph.spines['right'].set_color('#1e262c')
    graph.spines['left'].set_color('#1e262c')

    graph.bar(
        x, y,
        color='#43c4e3',
        alpha=0.10
    )
    bar_another = plt.bar(x, y, width=width, color='#43c4e3', alpha=0.10)

    pic_name = f'graphs/{graph_name}_bar.png'
    picture.savefig(pic_name)
    logger.info(f'Graph successfully saved to {pic_name}')
    return pic_name
