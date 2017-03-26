from collections.abc import Sequence

class Directory(Sequence):
    def __init__(self, current=None):
        self._current   = current   # 親ディレクトリ
        self._files     = []        # 親ディレクトリが持つファイル一覧
        self._dirs      = {}        # 親ディレクトリがもつディレクトリ一覧

    def __bool__(self):
        return bool(self._current)

    def __len__(self):
        pass

    def __call__(self):
        pass

    def __iter__(self):
        pass

    def __getitem__(self, key):
        pass

    @staticmethod
    def diff(self, d1, d2):
        pass

    @staticmethod
    def dive_tree(node, path):
        """
        pathのディレクトリをかえす
        """
        if path:
            try:
                return Directory.dive_tree(node._dirs[path[0]], path[1:])
            except KeyError:
                # path途中のディレクトリが存在しなくてもエラー
                return Directory()
            except IndexError:
                # 入らないとは思う
                print("IndexError")
        else:
            return node

    def add_directory(self, path, dir):
        """
        ノードにディレクトリを追加する
        """
        # pathを必ずリストにする
        p = path
        if type(p) == str:
            p = p.strip("/\n").split("/")

        # pathがrootのみの場合うまく処理させる方法を思い浮かばなかったため別途処理
        # len(p)が0のときは下のIndexErrorでFalseを返す
        # TODO : pathの長さがなんでも大丈夫にする
        if len(p) == 1:
            if self._current == p[0] and dir not in self._dirs:
                self._dirs[dir] = Directory(dir)
                return True

        # 新規ディレクトリを追加するディレクトリのインスタンスを取得する
        try:
            node = Directory.dive_tree(self._dirs[p[1]], p[2:])
        except IndexError:
            return False

        if node:
            if dir not in node._dirs:
                # ディレクトリを追加
                node._dirs[dir] = Directory(dir)
                return True
        return False

    def add_files(self, path, files):
        """
        pathにあるディレクトリにファイル一覧を追加
        """
        # pathを必ずリストにする
        p = path
        if type(p) == str:
            p = p.strip("/\n").split("/")

        # pathがrootのみの場合うまく処理させる方法を思い浮かばなかったため別途処理
        # len(p)が0のときは下のIndexErrorでFalseを返す
        # TODO : pathの長さがなんでも大丈夫にする
        if len(p) == 1:
            if self._current == p[0]:
                for f in files:
                    if f not in self._files:
                        self._files.append(f)
                return True

        # 新規ファイルリストを追加するディレクトリのインスタンスを取得する
        try:
            node = Directory.dive_tree(self._dirs[p[1]], p[2:])
        except IndexError:
            return False

        success = False
        if node:
            for f in files:
                if f not in node._files:
                    node._files.append(f)
                    success = True
        return success

    def is_exist(self, path):
        """
        pathが存在するか
        """
        # pathを必ずリストにする
        p = path
        if type(p) == str:
            p = p.strip("/\n").split("/")

        # pathがrootのみの場合うまく処理させる方法を思い浮かばなかったため別途処理
        # len(p)が0のときは下のIndexErrorでFalseを返す
        # TODO : pathの長さがなんでも大丈夫にする
        if len(p) == 1:
            if self._current == p[0]:
                return True

        # 新規ディレクトリを追加するディレクトリのインスタンスを取得する
        try:
            node = Directory.dive_tree(self._dirs[p[1]], p[2:])
        except KeyError:
            return False
        except IndexError:
            return False

        return bool(node)

    def __contains__(self, value):
        return value in self._files

    def get_top(self):
        """
        このディレクトリ構造のrootを返す
        """
        return self._current

    def get_files(self, path):
        """
        pathにあるファイル一覧を取得する
        pathがなければ例外(runtimeerror的なものがあれば)
        """
        # pathを必ずリストにする
        p = path
        if type(p) == str:
            p = p.strip("/\n").split("/")

        # pathがrootのみの場合うまく処理させる方法を思い浮かばなかったため別途処理
        # len(p)が0のときは下のIndexErrorでFalseを返す
        # TODO : pathの長さがなんでも大丈夫にする
        if len(p) == 1:
            if self._current == p[0]:
                return self._files[:]
            else:
                return None

        # 新規ディレクトリを追加するディレクトリのインスタンスを取得する
        try:
            node = Directory.dive_tree(self._dirs[p[1]], p[2:])
        except IndexError:
            return None

        if node:
            return node._files[:]
        else:
            return None
