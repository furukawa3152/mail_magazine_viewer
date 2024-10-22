import os
import json
import re
import gspread
import requests
from openai import OpenAI
from google.oauth2.service_account import Credentials
from datetime import datetime
chat_GPT_API_key = os.environ["API_KEY"]
def make_notes(columnA,columnB):
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
    credentials = Credentials.from_service_account_file("my-project-20230927-1db60d7e8989.json", scopes=scope)

    gc = gspread.authorize(credentials)

    #スプレッドシートIDを変数に格納する。
    SPREADSHEET_KEY = '1wjS_kDyKMi65DHWCaHNWeLLFyslr5DL8NEyLRTEhPXI'
    # スプレッドシート（ブック）を開く
    workbook = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = workbook.worksheet("シート1")
    # 追記したいデータ（A列のデータ、B列のデータ）
    new_data_a = columnA
    new_data_b = columnB
    today_str = datetime.now().strftime('%Y-%m-%d')
    # A列B列に同時にデータを追加する
    worksheet.append_row([new_data_a, new_data_b,today_str])

def read_textdata():
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
    credentials = Credentials.from_service_account_file("my-project-20230927-1db60d7e8989.json", scopes=scope)

    gc = gspread.authorize(credentials)

    #スプレッドシートIDを変数に格納する。
    SPREADSHEET_KEY = '1wjS_kDyKMi65DHWCaHNWeLLFyslr5DL8NEyLRTEhPXI'
    # スプレッドシート（ブック）を開く
    workbook = gc.open_by_key(SPREADSHEET_KEY)
    worksheet = workbook.worksheet("data")
    a1_value = worksheet.acell('A1').value
    return a1_value
def chat_gpt_return(input_data):
    client = OpenAI(api_key=chat_GPT_API_key)
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system",
                   "content": "以下に与えるメールマガジンの文章を、内容ごとに分割して出力して下さい。分割した文章には日本語で内容を要約した簡潔な見出しをつけ、見出しをkeyに、内容をvalueに持つjson形式にしてください。valueの部分は絶対に要約せず、原文のままで出力すること。質問、回答形式になっている部分については、質問と回答をセットにして一つの内容として扱ってください。その際のkeyは質問内容の要約にしてください。質問内容、回答は要約せず原文のままで書き出すこと。回答は必ずjsonのみを出力すること。"},
                  {"role": "user", "content": input_data}]
    )
    return (chat_completion.choices[0].message.content,chat_completion.usage)


if __name__ == '__main__':
    data = (read_textdata())
    # json_data = '''
    # {
    #     "key1": "value1",
    #     "key2": "value2",
    #     "key3": "value3"
    # }
    # '''

    # return_text,usage = chat_gpt_return(data)
    # print(return_text,usage)
    return_text = '''
    {
  "英語版Podcast": "先週から開始した英語版Podcast「Life is Artificial」ですが、かなり自動化も進んだので、1日一つ以上のペースで配信が可能になりました。\n\n配信のプロセスは、以下の通りです。\n\n\"ChatGPT 4o with canvas\"を使って脚本の作成（ただし、JSONとして出力）\nそのJSONファイルをTypeScriptで作ったアプリで音声ファイルの変換\nSpotify for Podcasterを使って、PodcastとしてSpotifyとAppleに配信\n実際の時間は、１にどのくらい時間をかけるかによりますが、１エピソードあたり、１０分程度で配信が可能です。作ったものが気に入らない場合の変更プロセスに少し問題があるので（全部の音声を生成し直さなければならない）、それを改善する方法を模索しています。\n\n最終的には、私自身が情報を得る際に使いたいと考えているので、どこまで自動化できるかがとても重要ですが、一本あたりを５分程度に抑えてあるので、英語の勉強も兼ねて聞くのも悪くないと思います。余裕があれば、日本語の字幕付きのビデオポットキャストにしても良いと考えています。\n\nこのメルマガの「私の目に止まった記事」欄で紹介した記事をベースにエピソードを作成する時もあるので、その際にはリンクを貼るようにします。",
  "SpaceX": "10月18日の朝に、SpaceXによるStarshipの５回目の打ち上げ実験が行われました。シアトル時間の早朝でしたが、たまたま早起きが出来たので、生で実況中継を見ることが出来ました。\n\n今回は、Starshipの打ち上げに使ったブースターロケット「Super Heavy」を、打ち上げ台に設置した「チョップスティック（「お箸」のこと）」と呼ばれるアームで回収するという、技術的に非常に難しいことにチャレンジしましたが、見事に成功しました。\n\nElon Muskは、これまで何度も不可能と言われることを成し遂げて来ましたが、今回はその経歴にさらに輝かしいページを加えることになりました。\n\nSuper Heavyは、直径９メートル、高さ７１メートルと２５回建てのビルぐらいの高さがあり、重さは200トンほどあります。\n\nそれほどの重さの物体をアームで持つだけでも大変なエンジニアリングですが、ロケットの打ち上げ後に音速の半分ほどの速度で自由落下してくるSuper Heavyを、逆噴射でスピードを落とし、位置と角度を精密にコントロールしながらアームでキャッチするのは、本当に至難の業です。\n\nNASAのエンジニアは、Elon Muskが「再利用可能なロケット」を作ると宣言した時に、それは見果てぬ夢でしかなく、「いつかは夢から覚めるだろう」とコメントしていましたが、その「見果てぬ夢」が実現してしまったのです。\n\nSpaceXが宇宙産業にもたらしたインパクトを良く表すグラフを見つけたので（参照）、下に貼り付けておきます。SpaceXが参入して以来、キログラムあたりの打ち上げコストが激減していることが良くわかります。\n\nちなみに、先日のTeslaの\"We Robot\"のプレゼンに関しても、機関投資家たちは「ロボタクシーも人間型ロボットも実現には程遠い」と判断してTesla株の売りに転じて株価が下がりましたが、こんな不可能を可能にし続けたElon Muskだからこそ、私のような個人投資家は、Tesla株を持ち続けるのです。\n\nSpaceX: Catching the Super Heavy booster\nMusk details Space X's Mechazilla's precise method for Super Heavy booster retrieval.",
  "Elon Muskのスピーチ": "巷では、AnthropicのCEO、Dario Amodeiが書いた「Machines of Loving Grace」というエッセイが評判を読んでいるようですが、私には、元OpenAIのエンジニアで、Superalignment チームにいたLeopold Aschenbrennerが書いた、SITUATIONAL AWARENESS: The Decade Aheadというエッセイの方が、もっと直接的に訴えかけて来るものがあったので、あえてそちらを紹介します。\n\n特に素晴らしいのは、その第一章「I. From GPT-4 to AGI: Counting the OOMs」で、\n\nなぜAIがこれほどの勢いで進化しているのか？\nなぜ、莫大なお金がGPUクラスターの構築に費やされているのか？\nAGIと呼べるほどのAIはいつ頃誕生するのか？\nの三つの質問に対して、とても分かりやすい回答を提示している点は、評価に値します。\n\nその根底にあるのは、このメルマガでも何度も指摘している「学習データ量とパラメータ数を増やせば増やすほど、AIは賢くなる」という「規模の効果」が効いています。\n\n１つめのAIの進化のスピードに関して、筆者は、以下の三つの効果が重なることにより、単純なムーアの法則による「2年ごとに2倍の進化」をはるかに上回るスピードで遂げるようになったと指摘します。\n\nCompute (ハードウェア能力の向上)\nAlgorithmic efficiencies（アルゴリズムの進化）\nUnhobbling（能力を阻害する障害の除去）\n特に興味深いのは、ハードウェア能力の向上で、ムーアの法則による「2年ごとに2倍の進化」に加えて、GPUクラスターへの投資額が急激に増えている点で、その結果、（2019年のGPT-2から、2024年のGPT-4の）過去5年間で、AIの学習に費やされる計算量が3千～1万倍に、10の乗数で表して、3.5～4 OOMs (Order of Magnitudes)増えたと指摘しています。\n\nそれにアルゴリズムの進化（＝より少ない計算量で優秀なAIを育てる技術）による効果が 1～2 OOMs、Unhobblingによる効果が 2 OOMsほどあり、トータルで 6 OOMs (100万倍)以上のスケールでAIが進化した結果、高校を優秀な成績で卒業した程度の能力を持つAIが誕生したと指摘しています。\n\n筆者は、この傾向は今後も続き、2027年までに、ハード+ソフトウェアだけで 5 OOMs (10万倍)のスケール増が期待出来、AIが博士号を取得した人並みの能力(=AGIと呼ばれるほどの能力)を獲得するだろうと予測しています。\n\nMicrosoft、Googleに代表されるハイパースケーラーと呼ばれる会社が、莫大な資金を投入して巨大なGPUクラスターを構築しているのは、この開発競争に乗り遅れまいとする結果で、それが結果として、2027年という早い段階でAGIと呼べるほどのAIを誕生させることになってしまうのです。\n\nこの業界で働いていない人たちにとっては、なかなか実感が湧かない話だと思いますが、博士号を持つ人並みの知能を人工知能を持つということは、単に、普通のAIが人から職を奪うだけでなく、科学の進歩そのものがAIによって行われる時代が来ようとしていることを意味します。\n\nそんな時代に、人々はどこに「生きがい」を見出せば良いのか、そんな時代に向けて子供たちは何を勉強すれば良いのか、色々と考えさせられる、意味深いエッセイです。",
  "Cerebras": "先週予告した通り、(上場準備中の)Cerebrasのホワイトペーパー（資料１）をじっくりと時間をかけて読んでみました。いくつか不明だった点もあるのですが、その疑問は、Cerebrasの技術者による解説ビデオ（資料２）でほぼ解決しました。\n\nニューラルネットには、ニューラルネットのパラメータ数が多いほど性能が向上するというスケールメリットがあります。そのため、時代の最先端を走るモデル（フロンティア・モデル）は莫大なパラメータ数を持たざるを得ないことになります。MetaのLlama3.2の場合だと、最大で405B(billion)のパラメータを持っています。\n\nニューラルネットの学習や推論のプロセスにおいては、GPUやNPUなどの「AIアクセラレータ」を使って、高速に、かつ並列に計算を行う必要がありますが、そこでボトルネックになるのが、（莫大なパラメータがしまってある）メモリへのアクセスです。\n\nGPUの場合、GPUが内部に持てるメモリ（高速アクセスが可能なSRAM）の量は限られているため（MBのオーダー）、それはキャッシュとして使い、パラメータは大容量のDRAM（GBのオーダー）に置いてアクセスすることになります。\n\nしかし、通常のDRAMではメモリの転送スピードが遅すぎるため、最新のNvidiaのGPUの場合、HBM(High Bandwidth Memory)と呼ばれる特殊なメモリが形成されたダイ（シリコンの上に電子回路を形成して切り出したもの）をGPUのダイに隣接し、その間を CoWoS(Chip-on-Wafer-on-Substrate)と呼ばれる特殊な技術で繋ぐことにより、GPUからアクセスしやすくする工夫がされています。\n\nCoWoSは非常に高度で繊細な技術であるため、温度変化に弱い、歩留まりが悪い、製造ラインの数が限られている、などの欠点があり、コスト高、品不足の原因になっています。また、HBMとは言え、チップ上のSRAMにはアクセススピードで大きく劣る上に、電力も大量に消費する原因にもなっています。\n\nCerebrasのWSE-3（Wafer Scale Engine）は、これらの問題を解決するために、演算処理を行うロジックとSRAMを隣接した小さなコアを90万個シリコンウェアハー上に形成した上でそれらをウェアハー上で直結することにより、CoWoSのような不安定で高価な技術を使わずに、桁外れに高速なスピードでのメモリへのアクセスを可能にしています。全体としては、１チップに44GBの高速アクセスが可能なSRAMが搭載された形になります。\n\n通常、チップを大きくすると、それだけ不良品の数も増えるため、通常は歩留まりが下がりますが、WSEの場合は、不良なコアがあっても、それをソフトウェアで見えなくするため、その問題はありません。\n\nCoWoSのような弱い接続部がないため熱にも強く、かつ、演算回路とメモリが一枚のウェアハーに同一のプロセスで形成されているため、（異なるプロセスで生成されたGPUとHBMが混在するNvidiaチップと比べて）放熱版との設置も用意です。\n\nCerebrasのチップは、こんな特殊な形状をしているため、通常のパソコンにPCIeカードとして装着することなどが不可能であるため、Cerebras自身が設計した水冷機能付きの専用のAIサーバー、CS-3をサーバーラックに設置することになります。\n\nまだ実績の少ないベンチャー企業でもあるため、すぐにNvidiaからシェアを奪うとは考えにくいですが、Llama3.1-70Bを550tokens/sec超で実際に処理出来ることは、Webサイトのデモでも確認できます。これからgrok、SanbaNovaと並んで、有望なAIベンチャーの一つとして、活躍することが期待出来ます。",
  "商品企画：代理母マリア": "妻と散歩をしながら、AIやロボットがもたらす未来について話していたところ、面白い商品の企画が出来たので、ChatGPTを使って書いたプレスリリースの形で紹介します。\n\n革新的な家族支援ロボット「マリア」登場 ― 日本の未来を支える新しい家族の形を提案―\n\n202X年10月5日、株式会社アーク・ロボティックスは、少子高齢化という社会的課題に挑む画期的な家族支援ロボット「マリア」を発表しました。「マリア」は、革新的な人工子宮技術を搭載しており、受精卵を用いた妊娠から出産・育児までのプロセスを完全にサポートすることができます。これにより、カップルやシングルの方々が自然に近い形で家族を持つことを実現します。\n\n「マリア」は、家族を持つ夢を支えるために設計され、不妊症に悩むカップル、共働き世帯、LGBTQ+カップル、結婚はしたくないけど子供が欲しい方など幅広い層を対象に、革新的な家族支援を提供します。\n\nオプションとして、精子バンクサービスから、アスリート、学者、実業家、俳優などの優秀な遺伝子を選択することが可能であり、将来の子どもの成長に対して大きな可能性を提供します。\n\nマリアは出産後も育児ロボットとして子どもの成長をサポートし、個別化された家庭教師機能による教育も提供します。これにより、親たちは子育てにかかる時間と労力の負担を大幅に軽減し、キャリアとの両立や家庭の幸福度向上を実現することが可能です。\n\nテスト期間中に「マリア」のサービスを受けたカップルからも、多くのポジティブな声が寄せられています。\n\n「私たちは何年も不妊治療を続けてきましたが、ようやく夢だった家族を持つことができました。『マリア』は私たちの人生を変えてくれました。」― 不妊カップルAさん\n\n「共働きの私たちにとって、『マリア』は子育ての頼れるパートナーです。赤ちゃんの成長を見守りながら、私たちのキャリアも諦めずに続けることができるなんて、本当にありがたいです。」― 共働きカップルBさん\n\n「同性カップルである私たちが家族を持つことに前向きになれたのは、『マリア』のおかげです。誰にでも家族を持つ権利があると感じさせてくれました。」― LGBTQ+カップルCさん\n\nまた、政府関係者からも「マリア」に対する大きな期待が寄せられています。\n\n「少子高齢化が進む日本において、『マリア』のような革新的な技術は非常に重要です。政府としても『マリア』を全面的にサポートするための予算を閣議決定しました。この技術が多くの家庭を支え、国全体の出生率向上に寄与することを強く期待しています。」― 内閣総理大臣\n株式会社アーク・ロボティックスは、「マリア」が日本社会における家族の新しい形を創造し、少子化問題の解決に寄与することを目指しています。「マリア」は単にロボットではなく、家族を支え、未来を育むパートナーとして、すべての人々に新たな希望を提供します。株式会社アーク・ロボティックスの名前は、人類を少子化という「洪水」から救うという願いを込めて名付けられました（アークは「箱舟」）。",
  "私の目に止まった記事": "Volkswagen’s state-of-the-art EV plant is on the brink of collapse\n\nVolkswagen傘下のAudiブランドで、電気自動車e-tronを生産しているブリュッセル工場が閉鎖の危機に瀕しているという報道です。\n\nブリュッセル工場は、年間12万台のe-tronを製造するキャパシティを持った工場ですが、実際に売れた数は、\n\n2022年 47,900台 2023年 37,400台 2024年 23,900台（現時点で）\n\nしかなく、このままでは閉鎖するしかないと経営陣は判断し、労働組合はそれに猛反対をしているそうです。\n\ne-tronは、高級電気自動車という位置付けで8万ユーロ(約1,300万円)という値付けで売られていますが、それが戦略的に失敗だったと、この記事は指摘しています。\n\nTeslaも同様に、最初は高級車(Roadstar、Model S、Model Y)から入りましたが、既に今は普及社（Model 3、Model Y）にシフトしており、さらに最近は中国メーカーがさらに安い電気自動車を提供しており、それがe-tronの販売不振に繋がっています。\n\nちなみに、私の妻は、Audiのe-tronに乗っていますが、とても満足しています。e-tronは、外見も操作感も従来型のAudi車とほぼ同じで、そこが彼女は気に入っているようです。\n\nTariffs Aren't Going To Stop China's EVs From Marching On Europe\n\nEUが中国製の電気自動車に関税をかけることを決めましたが、BYDはそれに先んじて安価な電気自動車をEU向けに、特に自動車産業が盛んなドイツ向けに提供することにより、（関税が導入される前に）中国製の電気自動車の価値を消費者に知ってもらうという戦略に出ているそうです。\n\nさらに、BYDはヨーロッパにも工場を作り始めており、それにより「中国製の電気自動車」にかかる関税を回避する戦略に出ているそうです。\n\n一つ上の記事でも紹介したように、Volkswagenは電気自動車で利益を上げることが出来ていません。同様の記事をポルシェに関しても読みました。この状況が続けば、関税を導入したところで一時凌ぎでしかなく、最終的には中国の自動車メーカーが世界を席巻する時代が来るように私には思えます。\n\nApple has terminated its self-driving vehicle testing permit in California\n\nAppleがカルフォルニア州で取得していた自動運転車の運行許可を取り下げたことを報じるX経由の報道です。Appleが自動運転車の開発から撤退したことは、すでにリーク情報として流れていましたが、それを追認するものとなりました。\n\nAppleの自動運転プロジェクトは、内部ではTitan（タイタン）と呼ばれ、年間に$1billion（約1,500億円）を費やして開発が進められていましたが、開発が思うように進まず、キャンセルになったと報じられていました。\n\nNew nuclear clean energy agreement with Kairos Power\n\nGoogleが、Kairos Powerにより開発されたSMR（small modular reactors、小型のモジュラー原発）を複数購入する契約を結んだことを発表する、ブログ記事です。\n\nこの記事で、Googleは、原発を「二酸化炭素を排出しないグリーンなエネグリー」と呼んでいます。Googleは、Fervo Energyが提供する新しいスタイルの地熱発電にも投資をしておりA first-of-its-kind geothermal project is now operational、会社としての脱炭素戦略の一環だと宣言しています。\n\nKairos PowerのSMRは、まだ開発中のものですが、その第一号を2030年にGoogleが導入することにより、SMRの開発を加速しようという意図もあると述べています。\n\nスリーマイルアイランドの原発が、Microsoftのデータセンター向けに再稼働をすることを伝えましたが、人類よりも優れたAIの開発競争が激化する中、データセンター向けの電力需要が急速に伸びており、それに応えることが出来るのは、原発だけだという認識が共有されつつあるように感じます。\n\nちなみに、Kairos Powerが作るSMRは、溶けた塩を冷却材として使用するスタイルの原発で、核燃料は小石状とのことです。似たような技術の別の原発ベンチャーを以前にこのメルマガで紹介した記憶があります。\n\nSam Altman-backed Oklo reacts to Google's nuclear energy deal\n\nSam AltmanがChairmanとして設立に関わったOkloの株価が、ハイパー・スケーラーたち（AIデータセンターに莫大な投資をしている、Microsoft、Google、Amazonなどの巨大IT企業のこと）による原発への投資の影響を受けて急騰した、という報道です。\n\n福島第一での過酷事故以来、米国での原発への投資は一気に冷え込んでいましたが、ここに来て、AIデータセンター向けの電力需要の急増を受けて、比較的早いスピードで運用を開始できる小型の原発（SMR：Small Moular Reactor）に注目が集まっています。\n\nSMRを開発している企業は複数ありますが、Okloはその中でも小型の高速増殖炉を開発している点で非常にユニークです。\n\n日本では、もんじゅの破綻で高速増殖炉のイメージが悪くなってしまいましたが、高速増殖炉は（資源に限りがある）放射性鉱物の利用効率の面で有利であり、もし実用化が可能になれば、これまでゴミ扱いだった使用済み核燃料を燃料として有効に使えるようになります。\n\n日本では、高速増殖炉は「核のリサイクル」プロジェクトの中核をなす存在で、それゆえ、日本の電力会社は、使用済み核燃料を（破棄にコストがかかる）負債ではなく、（さらに価値を生み出す）資産として計上してきたという経緯があります。\n\n経産省が意地でも「核のリサイクル計画は失敗だった」と認めることが出来ない理由の一つが、この資産計上で、失敗を認めると、債務超過になってしまう可能性があります。\n\nChanging OpenAI’s nonprofit structure could have big consequences\n\nOpenAIが、設立時の非営利団体から、完全な営利団体に変わろうとしていることが報じられていますが、そこには大きな障害があると指摘する記事です。\n\n非営利団体は、株式会社のように株主を持たないため、非営利団体が持つ資産を、たとえ取締役であっても、勝手に使うことは出来ません。\n\nその意味では、非営利団体であったOpenAIが開発したChatGPTは、営利団体であるOpenAI Globalが勝手に使うことは許されず、相当の対価を支払うべきだ、というのが筆者の主張です。\n\nこの件に関しては、OpenAIの設立の際に巨額の寄付をしたElon Muskも文句を言っていますが、Sam AltmanがMicrosoftから資金を調達した際に、営利団体であるOpenAI Globalを設立し、そこに知的財産を動かした経緯には、公にはなっていません。\n\n営利団体の株式を対価として非営利団体に渡せば良いようにも思えますが（当時、Microsoftが49%の株式を持つことになると報じられました）、これが許されるのであれば、かなり好き勝手なことが出来るようになってしまいます。\n\nMeta Bulls Are Overvaluing Zuckerberg’s Vision\n\nMetaの株価が今年に入って70％以上上昇していることに関して、警告を鳴らす記事です。\n\nMetaは、MicrosoftとGoogle並んでAIに莫大な投資をしていますが、まだその効果は、売り上げや利益に反映されておらず、投資家たちは、CEOのMark Zackerbergの掲げるビジョンに投資をしているだけだと筆者は指摘しています。\n\nMetaは、（ゲーム端末の一種である）VRグラスだけでなく、ARグラスにも力を入れており、Ray-Banと共同開発したスマートグラスは、70万個が売れたとされていますが、それは、同時期に2,600万個出荷されたApple Watchと比べたら微々たるものだと筆者は指摘しています。先日発表した、Orionは画期的なデバイスですが、まだ発売までには何年かかかります。\n\nさらに、Metaの本業であるソーシャル・メディアも、独禁法上の懸念や、子供達をソーシャル・メディアから守ろうという運動などもあり、必ずしも順風満帆とは言えません。\n\nそんな中で、2024年だけで$40 billion、2025年はさらに上回る投資をAIにして、本当に回収できるのかに関して、疑問を呈する人も少なくありません。\n\nちなみに、私は、Facebookは上場間もなく株を購入しましたが、Zackerbergが「Metaverse」を戦略と掲げた時に、一度すべて売却しました。しかし、Llamaをオープンソースとして公開し、Smart Glassを発表したあたりから再び株を購入し始め、今では再びポートフォリオのトップ１０に入っています。\n\n私は、ARグラスに限らず、AIを活用したウェアラブルデバイスに大きなポテンシャルを感じており、その意味でも、最近のMetaの動きが気に入っているのです。",
  "Boston Dynamics & Toyota Research Institute Announce Partnership to Advance Robotics Research": "Boston DynamicsとTRI(Toyota Research Institute)が、ロボットの共同開発をすることで合意した、というアナウンスです。\n\nBoston Bynamicsは、Atlasという非常に可動性の高い（＝運動神経の良い）ロボットの開発で長年注目されてきた会社ですが、会社としては、2013年にGoogle傘下に、2017年にソフトバンク傘下に、2020年にHyundai Motor傘下にと変遷を繰り返してきた会社です。独立した会社として運営するのは厳しいものの、大きな会社の傘下に入ったところで、親会社の業績に貢献できるわけではないところが難しかったのだと思います。\n\n大きな課題だったのは、Boston Dynamicsに使われているソフトウェアです。ニューラルネットがこれほどの性能を発揮することが分かる前から開発されていたため、すべての動作を人間が作ったアルゴリズムでこなすソフトウェアであり、Teslaが採用している「Software 2.0」的なフルスタック・ニューラルネットとは程遠い設計なのです。\n\nヒューマノイドロボット市場に、Tesla、Figure AI、1X、Unitree Roboticsなどが最新のAI技術を活用して参入する中で、このままでは戦えないと見て、(AI技術者を多数抱える)TRIと技術提携をすることにしたのです。\n\n一方のTRIは、トヨタ自動車の「AI戦略」の一環として研究者を集めて設立されたものの、トヨタ本体の「ものづくりカルチャー」とは大きな隔たりがある組織であり、トヨタ自動車としてもどう活用して良いか分からない状況になっていたのだと思います（私は、トヨタ自動車がTRIを設立したばかりの頃に、トヨタ自動車とビジネスをしていたので、その辺りの事情は、肌感覚で知っています）。\n\n今後、自動運転技術が自動車業界にとって最も重要な技術になろうとしている今、トヨタ自動車がTRIという資産を生かすことはとても重要です。\n\nしかし、トヨタ自動車は、長年、ソフトウェア作りを外部に委託して来たため、たとえどんなに良い技術をTRIが作ったとしても、その技術を製品に反映させるためには、数多くの障害を乗り越えなければならないし、時間もかかるのです。\n\nそれを理解した上で、今回の提携の報道を見ると、また、少し違う景色が見えてきます。\n\nNvidia's Ian Buck shares his vision of the GPU data center": "Nvidiaで \"VP of accelerated computing\"を務めるIan Buck氏のインタビューの紹介です。\n\nBuck氏は、Nvidiaが既にGPUを単体で売る会社から、GPUを含めた\"AI Factory\"を販売する会社に変わりつつあることを、分かりやすく説明してくれています。\n\n高性能なGPUを使いこなすには、CPUや外部メモリとの通信スピードがとても大切で、これまでのように、汎用的なパソコンに「GPUカード」を搭載する時代ではなくなっています。\n\nGPUが出す熱の排熱もとても重要で、Nvidiaの最新のチップになると、空冷では最大のパフォーマンスを出すことが出来ず、水冷にせざるを得ないそうです。\n\nそこまで含めて考えると、Nvidiaから単にGPUを購入するのではなく、高速なデータ転送を可能にする仕組みや、水冷システムを最初から全て備えたシステムをNvidiaから購入することが理にかなっており、そこにNvidiaは注力しているとBuck氏は主張しています。",
  "Chinese cyber association calls for review of Intel products sold in China": "中国の業界団体「サイバーセキュリティー協会」が、Intelのチップを安全保障上のリスクがある商品の一つとして指定した、という報道です。\n\n米国政府は、既に中国製の交換機やネットに繋がる自動車に対して同様の扱いをして輸入を禁止していますが、これはそれに対する中国側の報復と解釈することも可能です。",
  "質問: 2024/10/11のTSLAのロボタクシーイベントの後、株価が7～8%下がりました。わたしは好印象だったのですが株主の反応は逆でした。何が原因だと考えられますか？": "一番の原因は、Model2と呼ばれている$25,000程度の安価なモデルの発表がなかったことにあります。株価を大きく左右する機関投資家は、高々６ヶ月先ぐらいの業績を見て投資先を決めているため、今回のような、実際に消費者が購入出来る製品の発表を含まないイベントは、マイナスでしかないのです。\n\nElon Muskは、前回の決算発表で、安価なモデルの開発はロボタクシーと並行して進めていることは明言していたので、来年の前半には正式発表があると私は期待しています。多くの機関投資家たちは、それが今回のイベントで発表されると期待したのだと思います。",
  "質問: 近年、AIの画像認識などが発達し、製造業などでもその導入が検討されているかと思います。大手のゼネコンなどではITやAI部門などを設けているようですが、思うように現場への導入が進んでいないようです。この導入はなぜ難しいのでしょうか。また、製造業に携わる従業員の負担軽減のためのAI活用法について中島様の見解を教えていただきたいです。": "単に時間がかかっているだけだと思います。LLMに代表される最新のニューラルネットワーク・モデルは、これまで不可能だったことを可能にする画期的なソフトウェアですが、あくまで「部品」に過ぎないので、それをビジネスに活用するには、誰かが業務に役にたつアプリケーションの形に仕上げる必要があります。\n\nまだ未熟な業界ではありますが、この市場を狙った開発ツールを作っているベンチャー企業も多数あるし、そこでAIコンサルタント的なビジネスで大きな売り上げを上げている会社もあります（Accentureが良い例です）。\n\n一番手っ取り早いのは、製造業を営む会社が優秀なソフトウェア技術者を雇って、自ら必要なアプリケーションを開発ことですが、それはそれで、人事上難しかったりもするので（終身雇用を嫌う日本企業は専門職を雇いたがらない、優秀な技術者の給料はやたらと高い）、時間がかかっているのだと思います。",
  "質問: 海外からVPNサービスを使うことを検討しています。具体的にはマレーシアからAmazon Prime等へのアクセスです。VPNを提供するサービスはいくつかありますが「セキュリティの観点からどのサービスを選べば良いか？」の判断がつきません。中島さんが実際に利用されている（たことのある）またはお勧めのVPNサービスはありますでしょうか？": "難しい質問ですね。私も一時期はVPNサービスを使っていましたが、そもそもその会社を信用して良いのかが、不安で、今は使っていません。ちなみに、サービスを使っていた会社の名前はsurfsharkで、サービスそのものはとてもしっかりとしていました。",
  "質問: 生成AIの醍醐味は、RAGとFINE TUNINGにあると考えております。しかし一般の方がその機能を使うのは難しいと考えております。そこで何か誰でも簡単にRAGやFINE TUNINGできるサービスや手法があれば教えていただけますでしょうか。": "OpenAIのGPTsを使えば、知識がなくても与えたドキュメントを使ったRAGが実行できるので、まずはその辺りから試すのが良いと思います。他にも、RAGやTune Tuningをサービスとして提供しているベンチャー企業が複数あることは知っていますが、実際に私自身が試してもいないので、特におすすめのサービスはありません。\n\nちなみに、Fine Tuningは大きな手間がかかりますが、RAGはとても手軽に出来るので、OpenAIから提供されているサンプル（Question answering using embeddings-based search）などをベースに自分で開発するのもそれほど難しくはありません。",
  "質問: フロントエンドはGo、バックエンドはGinを使用して、DeepL APIを使って日本語から英語に翻訳するアプリを作ったのですが上手く動作しませんでした。Stack Overflowで質問するとき英語が必要だと思うので、ChatGPTを使って日本語を英語に翻訳して質問しても問題なく解決できますか？": "ここに質問するよりも、実際にStack Overflowで質問するのが一番良いと思います。最近は、ChatGPTやCoPilotの誕生で使う人が減ってはいると思いますが。私も最近は、ほとんどアクセスしていませんが、以前は、質問者として大いに活用していました。",
  "質問: Celsius Holdingsは健康志向やフィットネスの焦点を当てており、エナジードリンク市場で急速に成長しています。将来的にMonster Beverageに匹敵する企業になる可能性はありますか？": "エナジードリンク市場のことは詳しくないし、Celsiusの商品を見かけたこともないので(知り合いが飲んでいるとか、Costcoで大量に売っているのを見かけたりしたことがない、という意味です)、なんとも評価のしようがありません。\n\nInstagramのフォロワーが74万人いる（参照）のはとても頼もしいと思います。",
  "質問: 中島さんが使われているイスを教えていただけないでしょうか。イスに座っている時間が長いので、腰痛や背中が痛くなることが多く困っています。": "中島さんはどのようなイスを使い、またはサポート器具を使い、腰痛対策などされていますでしょうか。": "Stokkeというノルウェーの会社のバランスチェアという椅子です。類似品も試しましたが、この会社のものが最高でした。私は、以前、腰痛に悩まされていましたが、この椅子に変えてから、腰痛そのものがなくなってしまいました。背筋を伸ばして座らないといけないので、慣れないうちは少し疲れますが、それが良いようです。\n\n調べたところ、今はStokkeはバランスチェアは売っておらず、同じデザイナーによる製品を、同じくノルウェーのVarierという会社が売っています。Variable Balanceという製品名です。",
  "質問: ふと疑問に思った事を質問させて頂きます。昔から、「お金に色は無い」と言いますが、ブロックチェーン技術でコインに色は付けられないものでしょうか？戦争や犯罪に使われた黒いお金を受け取る側も選べるように出来たら、社会が少し良くなる気もしたのですが、出来ないものなのでしょうか？またコインの色によって金利が変わったら、それも面白いなと妄想しています。変な事だとは思い恥ずかしさも感じますが、自分の中で聞いてみたい！と思い質問をさせて頂きました。": "技術的には可能です。Ethereum上であれば、スマートコントラクトという仕組みを使って、自分独自の通貨を発行することも可能なので、その際に「世界初の色付きの通貨」としてローンチするのも面白いと思います。\n\nちなみに、BitcoinやEtherium上の通常の通貨の場合、トランザクションのすべて（どのウォレットからどのウォレットにいくら転送されたか）がブロックチェーン上に刻まれるとは言え、一度ウォレットに入ってしまえば「総数」でしか管理しないため、そこで「色が混ざって」しまいます。\n\nこの問題を解決するためには、すべての通貨に、明示的に色を付けるだけでなく、自分のウォレットから通貨を取り出す際にも、「どの色の通貨を使うのか」を明確に指定する必要が生じ、その分、使い勝手（UX）も悪くなるし、ブロックチェーンに書き込むデータも増えて、結果的に「ガス代（書き込むデータ量に応じて支払う手数料）」が増えてしまいます。\n\n上手に設計しないと、これらの問題（特にガス代）のために、うまく機能しない可能性も十分にあるので、注意が必要です。",
  "質問: 就活生です。面接でよく聞かれる質問の一つに、「あなたの強みと弱みは？」というのがありますが、自分の強み弱みがわからないです。強み弱みは自分のこれまでの経験とエピソードと紐付ける必要があるかと思うのですが、なかなかこれというものがないのが本音です。中島様が考える「自分の強み、弱み」の見つけ方についてご教示いただけますでしょうか。": "「自分の強み弱みがわからない」という状況は私にとっては理解し難いです。私は、子供の頃から好き嫌いがはっきりしていたので、自然と、好きなこと（数学、科学）が強みに、嫌いなこと（古典、漢文、歴史）が弱みになりました。\n\n自分が何が好きなのか、何をしていると夢中になれるのか、もう一度考えてみてください。",
  "質問: 政府が次世代半導体の量産を目指すラピダスに出資を協議しています。国策の半導体支援は、エルピーダ等今までなかなかうまくいっていません。米中対立でアメリカの支援は期待できると思いますが、競合は、TSMCやサムスンになると思います。中島様は、率直にラピダスの今後についてどう思いますか。お聞かせください。": "半導体作りに挑戦すること自体は悪くないと思うのですが、「国策として税金を使って行う」ことに伴うマイナス面が数多くあるので、うなく行かない可能性が高いと感じています。\n\n国策に伴うマイナス面とは、\n\n困ったら国がお金をくれるという甘えが生じる\nハングリー精神を持った人が来ない\n政府や企業の天下り先になってしまう可能性がある\n株を大量に持った創業者がいない\n不要な人を解雇出来ない\n甘い汁を吸おうとする人や会社が集まってくる\nなどです。",
  "質問: 中島様が日々生活している中で強く興味関心を惹かれ取り組もうと思う分野は既知の分野が多いですか？私は情報工学の博士号を持ち現在ソフトウェアエンジニアとして働いていますが、Light Sports Aircraftと呼ばれるカテゴリの軽飛行機を作りたく空いた時間に専門書を読み、既存航空機の設計図を手本に自作機の設計をしています。ただ、同じ工学とはいえ内容がかなり異なり実機製作まで漕ぎ着けるか疑問に思うこともしばしばあります。このような状況をどう思われますか（ざっくりでスミマセン…）。": "「作りたい」という思いはエンジニアにとっては、何よりも貴重な「宝」なので、思い切って突っ走ってみるのが良いと思います。何事もやってみなければ分からないことが多いので、失敗を恐れてスタートしないのは、とても勿体無いと思います。\n\n先週、SpaceXが見せてくれた（２００トンのブースターロケットをキャッチするという）超絶技巧は、多くの人が無理だと思っていたし、Elon Muskからやれと言われたエンジニア自身も簡単ではないことは十分に認識していたと思います。\n\nチャレンジしなければ、失敗する可能性もゼロですが、成功する可能性もゼロです。そんな人生はつまらないと私は思います。",
  "質問: 中島様は経営者やマネージャーの立場として，部下から「もっと長い時間に働きたい」のような要望があった場合に，どのように対応しますか？": "「働きたい理由」次第です。残業手当が目当てであるならとんでもない話ですが、関わっているプロジェクトが楽しくて仕方なく、寝るまも惜しんで働きたいのであれば、応援します。そんな人には、裁量労働制で働いてもらう方が、マッチしているように思います。\n\n裁量労働制：「働いた時間の長さ」ではなく「働いたことへの成果」に対して報酬が支払われる制度です。労働者が自分の裁量で、仕事の進め方や労働時間を決められるため、うまく運用できれば働き方改革や生産性向上が期待できます。裁量労働制は「業務の性質上、業務遂行の手段や方法、時間配分等を大幅に労働者の裁量にゆだねる必要がある業務に適しています。",
  "質問: 2025年のNvidiaの今後の成長率について、中島様の見解をお聞かせください。": "2026年1月決算のNvidiaの当期純利益の前年比成長率は+40％予想です。 Appleの同年度の成長率は+9%予想ですから、Nvidiaが時価総額世界1位になる可能性が高いと思います。\n\n更に、時価総額4兆ドル、5兆ドル、6兆ドルに達する可能性も見えてくるわけですが、そこまで手が届くのかと思う一方で、私の周囲を見渡すとバックオフィスの人員が1/10と減少し、AIに代替されています。\n\n私自身、私の分身を作り、私の分身とリアルタイムAPIでアイデアの壁打ちMTGを行っていますし、 クライアントの経営陣や優秀なマネージャーの発言を教師データにAIマネージャーを産み出し、 基礎となるマネジメントをAIに担当させるプロジェクトも動いております。\n\n更に、ポジショントークが多分に含まれていますが、AMDのLisa Su CEOは2023年→2027年までのCAGRを70％と予想しています。 https://thinglabs.io/amd-ceo-forecasts-custom-chips-surpassing-gpus-due-to-ai-demand\n\nNvidiaの時価総額4兆ドル、5兆ドル、6兆ドルは荒唐無稽だと思う一方で、夢物語ではないようにも感じます。",
  "質問: 私もNvidiaの株を持っているので、ポジショントークになってしまいますが、これからさらに伸びる可能性は十分にあると思います。": "繰り返しになりますが、AIに関しては、「多くのパラメータを持つモデルを大量の学習データを与えると、より賢いAIができる」という効果が働くことが明らかになったため、「どこよりも大きなAIデータセンター、どこよりも優秀なAIを作る」競争が（Microsoft、Meta、Googleなどの）ハイパースケーラーたちの間で始まっています。\n\nその戦いが続く限り、「AIアクセラレータ」の市場は伸び続けるし、少なくも現時点では、Nvidiaがそのメリットを最も享受出来る立ち位置にいます。",
  "質問: 早速ご質問なのですが、ChatGPTを活用してプログラミングをすることは、初心者に対しておすすめできますでしょうか？": "私の体験談なのですが、音楽ファイルを指定の時間で細かく分けたい事情があり、ふとChatGPTを使ってPythonでコードを書かせてみようと思い立ちました。（私はPythonを使ったプログラミングは初心者です）\n\nある程度の指定をしてあげると、ちゃんとコードを書いてくれ、実行してエラーがあれば、その解決法も教えてくれました。\n\nそして何度かやり取りをし、実践したところ、遂にPythonで音楽ファイルを分割するコードを書くことができました。\n\nこのように、何かやりたいことがあった場合にChatGPTを使ってプログラミングすることを繰り返していれば、プログラミングスキルが上達しますでしょうか？それとも、Chat GPTに頼らず自分で検索等して調べながらコードを書いた方が、長期的な視点ではプログラミングスキルが上達しますでしょうか？\n\n以上、中島様のご意見をお聞かせいただけますと幸いです。",
  "質問: 1.『ionq』という、量子コンピュータを開発？する企業があり、そこの株を買おうか迷っています、ご参考に中島聡の量子コンピュータへのお考えをお聞きしたいです。2.将来の為にAIを使いこなせた方が良いなどの話しがあるかと思いますが、AIを使いこなすとは一体どこまで出来ることを指すのでしょうか？": "例えばchatgptへの質疑応答は使えば誰でも出来るかと思います。生成aiもプロンプト入力すれば誰でも画像や動画が生成出来ます。 AIを使いこなすとはそこから発展して何か別の用途に応用出来るまでを指すのでしょうか。 AIを使いこなしたいたいとは思うものの具体的に何を目指して何を訓練的にやっといた方が良いのかが分かりません。\n\n中島聡さんのご意見が聞きたいです。",
  "回答: その場合、少し前にもここで答えた覚えがありますが、私にとっては、量子コンピュータは、核融合と同じく、「実用化されれば、大きなインパクトを与えるとは思うけど、普段は考える必要がないテクノロジー」の一つです。その分野で魅力的な企業に出会えば、少しだけ株を購入するかも知れませんが、（Tesla、Apple、Nvidiaのように）毎日のように気にかけるべき存在にはなり得ません。",
  "回答: 一言でいえば、「AIを使うことにより、生産性を爆上げすること」です。プログラミングでも良いし、動画などのコンテンツの作成でも良いですが、これまで一週間かかっていた仕事が、AIを使うと３時間で出来るようになる、それこそが、「AIを使いこなしている」証です。"
}
    '''
    start_index = return_text.find('{')
    end_index = return_text.rfind('}') + 1
    json_text = return_text[start_index:end_index]
    # テキスト内の制御文字を正規表現で削除する
    json_text = re.sub(r'[\x00-\x1F\x7F]', '', json_text)
    # JSON文字列をPythonの辞書に変換
    try:
        json_data = json.loads(json_text)
        print("JSON部分のデータ:")
        print(json_data)
    except json.JSONDecodeError as e:
        print(f"JSONデータの解析に失敗しました: {e}")
    dict_data = json.loads(json_text)
    for key,value in dict_data.items():
        make_notes(key,value)

