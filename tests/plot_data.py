from pybk8500 import plot_csv_file, plot_csv_files
import matplotlib.pyplot as plt


if __name__ == '__main__':
    figures = plot_csv_files('./CC_1.csv', './CC_2.csv', inc_time=True, split=False, show=False)

    # Change figures
    # for fig in figures:
    #     fig.gca().grid()

    # Use plt
    plt.grid()
    plt.show()
