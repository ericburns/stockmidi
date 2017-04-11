from song import Song
from stockutil import load_csv


def main():
    data = load_csv('../data/stock-top50-last90-2017-04-10.csv')
    song = Song('test', data)
    song.generate()
    song.write('../out/test.mid')


if __name__ == '__main__':
    main()
