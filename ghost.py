import traceback  # エラー表示のためにインポート
import configparser
import os

from discord.ext import commands  # Bot Commands Frameworkをインポート

# 読み込むコグの名前を格納しておく。
INITIAL_EXTENSIONS = [
    'cog.bot_cog',
    "cog.idol_cog"
]

# クラスの定義。ClientのサブクラスであるBotクラスを継承。
class MyBot(commands.Bot):

    # MyBotのコンストラクタ。
    def __init__(self, command_prefix):
        # スーパークラスのコンストラクタに値を渡して実行。
        super().__init__(command_prefix)

        # INITIAL_COGSに格納されている名前から、コグを読み込む。
        # エラーが発生した場合は、エラー内容を表示。
        for cog in INITIAL_EXTENSIONS:
            try:
                self.load_extension(cog)
            except Exception:
                traceback.print_exc()

    # Botの準備完了時に呼び出されるイベント
    async def on_ready(self):
        print('-----')
        print(self.user.name)
        print(self.user.id)
        print('-----')


def main():
    #configの読み込み
    base = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.normpath(os.path.join(base))
    conf = configparser.ConfigParser()
    conf.read(conf_path+'/config/config.ini', encoding='utf-8')

    bot = MyBot(command_prefix='$')
    bot.run(conf['DEFAULT']['BOT_TOKEN'])

# MyBotのインスタンス化及び起動処理。
if __name__ == '__main__':
    main()
