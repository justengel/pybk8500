from pybk8500 import plot_csv_file, plot_csv_files

if __name__ == '__main__':
    plot_csv_files('./CC_1.csv', './CC_2.csv', inc_time=True, split=False)
