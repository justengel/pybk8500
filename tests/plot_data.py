from pybk8500.plot_csv import main, plot_csv_file, plot_csv_files

if __name__ == '__main__':
    plot_csv_files('./CC_1.csv', './CC_2.csv', split=False)
