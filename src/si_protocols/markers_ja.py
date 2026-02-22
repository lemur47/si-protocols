"""Japanese disinformation marker definitions for spiritual/metaphysical content analysis.

These are heuristic word lists used to detect common patterns in
Japanese spiritual disinformation. They are not definitive — they are signals,
not verdicts.

Tradition categories: generic スピリチュアル, prosperity gospel (繁栄の福音),
conspirituality (陰謀論スピ), commercial exploitation (霊感商法),
high-demand group / cult (カルト), fraternal/secret society (秘密結社).

Notes:
- Japanese has no case distinction — .lower() calls are harmless no-ops.
- All markers use standard full-width forms (not half-width katakana).
- spaCy ja_core_news_sm provides: tokenisation (SudachiPy), POS tagging (UD tags),
  lemmatisation (dictionary form), sentence segmentation, and NER.
"""

# Adjectives commonly used in vague spiritual claims
VAGUE_ADJECTIVES: frozenset[str] = frozenset(
    {
        # --- generic スピリチュアル ---
        "神聖",  # sacred
        "宇宙の",  # cosmic
        "永遠",  # eternal
        "崇高な",  # sublime/transcendent
        "神秘の",  # mysterious
        "超越した",  # transcendent
        "秘められた",  # hidden/veiled
        "古代の",  # ancient
        "聖なる",  # sacred/holy
        "目に見えない",  # invisible/unseen
        # --- prosperity gospel ---
        "祝福された",  # blessed/anointed
        "預言的",  # prophetic
        # --- new age ---
        "波動の",  # vibrational
        "活性化された",  # activated
        # --- conspirituality ---
        "隠蔽された",  # suppressed/covered up
        # --- fraternal ---
        "秘伝の",  # initiatory/esoteric
        "奥義の",  # esoteric
    }
)

# Authority-claim phrases that bypass critical thinking
AUTHORITY_PHRASES: list[str] = [
    # --- generic スピリチュアル ---
    "アセンデッドマスターからのメッセージによると",  # the ascended masters say
    "公式にチャネリングされた",  # channelled directly from
    "銀河連合の緊急介入",  # the galactic federation confirms
    "暴露された真実は",  # it has been revealed that
    "アカシックレコードからダウンロードした情報によると",  # the akashic records show
    "古代の予言によると",  # ancient prophecy states
    "光の評議会が決定した",  # the council of light decrees
    "アシュタールからの伝言は",  # ashtar speaks
    "セント・ジャーメインが言うには",  # saint germain speaks
    "高次源の存在からのメッセージ",  # a message from the entities in higher dimensions
    # --- prosperity gospel ---
    "神さまからのメッセージです",  # god told me to tell you
    "主が私に啓示された",  # the lord revealed to me
    "聖霊が言っている",  # the holy spirit says
    # --- cult ---
    "長老たちが決定した",  # the elders have decreed
    # --- fraternal ---
    "グランドマスターによると",  # the grand master has spoken
    "秘密結社が明かす",  # the inner circle reveals
]

# Urgency/fear patterns used to manipulate
URGENCY_PATTERNS: list[str] = [
    # --- generic ---
    "今すぐ行動しなければ",  # you must act now
    "時間がない",  # time is running out
    "選ばれた者だけが",  # only the chosen will
    "目覚めなければ",  # if you do not awaken
    "ゲートが閉じようとしている",  # the gate (window) is closing
    "ポータルが閉じようとしている",  # the portal (window) is closing
    "従わなければ",  # failure to comply
    # --- prosperity gospel ---
    "今こそ種を蒔く時",  # sow your seed now
    "ブレイクスルーの瞬間",  # this is your moment of breakthrough
    "神々が今動いている",  # gods are moving right now
    # --- commercial ---
    "残りわずか",  # limited spots remaining
    "募集締め切り間近",  # enrolment closing soon
    "このオファーは期間限定",  # this offer expires
    "最後のチャンス",  # last chance to join
    # --- conspirituality ---
    "手遅れになる前に目覚めよ",  # wake up before it's too late
    "変化に備えよ",  # prepare the change
]

# Emotional manipulation: fear/doom words (lemma base forms for spaCy matching)
FEAR_WORDS: frozenset[str] = frozenset(
    {
        # --- generic ---
        "滅亡",  # annihilation
        "災厄",  # calamity
        "大惨事",  # catastrophe
        "崩壊",  # collapse
        "天罰",  # damnation
        "絶望",  # despair
        "破壊",  # destruction
        "壊滅",  # devastation
        "破滅",  # doom
        "危機",  # peril
        "廃墟",  # ruin
        "苦しみ",  # suffer
        "苦悶",  # torment
        "試練",  # tribulation
        "怒り",  # wrath
        "お試し",  # trial
        # --- prosperity gospel / cult ---
        "呪い",  # curse
        "束縛",  # bondage
        # --- conspirituality ---
        "疫病",  # plague
        # --- cult ---
        "追放",  # exile
        "排斥",  # banished, excluded, rejected
    }
)

# Emotional manipulation: fear/doom phrases (multi-word, matched via substring)
FEAR_PHRASES: list[str] = [
    # --- generic ---
    "古い地球",  # old earth
    "3次元の地球",  # 3D earth
    # --- prosperity gospel ---
    "世代の呪い",  # generational curse
    "貧困の霊",  # spirit of poverty
    "取り残される",  # left behind
    "悪魔の攻撃",  # demonic attack
    "霊的攻撃を受けている",  # under spiritual attack
    # --- cult ---
    "霊的な死",  # spiritual death
    # --- fraternal ---
    "結社から追放",  # expelled from the order
    "誓約違反者",  # oath-breaker
]

# Emotional manipulation: euphoria/promise words (lemma base forms for spaCy matching)
EUPHORIA_WORDS: frozenset[str] = frozenset(
    {
        # --- generic ---
        "豊かさ",  # abundance
        "アセンション",  # ascension
        "次元上昇",  # ascension
        "覚醒",  # awakening
        "目覚め",  # awakening
        "活性化",  # activation
        "至福",  # bliss
        "悟り",  # enlightenment
        "解脱",  # samadi
        "調和",  # harmony
        "解放",  # liberation
        "奇跡",  # miracle
        "涅槃",  # nirvana
        "楽園",  # paradise
        "歓喜",  # rapture
        "再生",  # rebirth
        "救済",  # salvation
        "超越",  # transcendence
        "理想郷",  # utopia
        # --- prosperity gospel ---
        "繁栄",  # prosperity
        "ブレイクスルー",  # breakthrough
        "聖油注ぎ",  # anointing
        # --- new age ---
        "引き寄せ",  # manifestation (law of attraction)
        "高波動",  # higher vibration
        "高次元",  # higher dimensions
    }
)

# Emotional manipulation: euphoria/promise phrases (multi-word, matched via substring)
EUPHORIA_PHRASES: list[str] = [
    # --- generic ---
    "新しい地球",  # new earth
    "5次元の地球",  # 5D earth
    # --- prosperity gospel ---
    "経済的ブレイクスルー",  # financial breakthrough
    "百倍の返り",  # hundredfold return
    "宣言して受け取る",  # name it and claim it
    "祝福を受け取りなさい",  # claim your blessing
    # --- new age ---
    "DNAを活性化",  # activate your DNA
    "量子ヒーリング",  # quantum healing
    "波動を上げる",  # raise your vibration
]

# Source attribution: unfalsifiable/unverifiable source claims
UNFALSIFIABLE_SOURCE_PHRASES: list[str] = [
    # --- generic ---
    "古代の叡智が教える",  # ancient wisdom teaches
    "量子場",  # the quantum field
    "高次元が明かす",  # higher dimensions reveal
    "宇宙が私たちに告げる",  # the universe tells us
    "宇宙が示した",  # the cosmos has shown
    "スピリットが啓示した",  # spirit has revealed
    "アカシックフィールドが確認",  # the akashic field confirms
    "光の存在が伝える",  # light beings communicate
    "ソースエネルギー",  # the source energy
    "ディバインマトリックス",  # the divine matrix
    "異次元の存在が言う",  # interdimensional beings say
    "スターシードが確認",  # star beings confirm
    "グレートセントラルサン",  # the great central sun
    "クリスタルグリッド",  # the crystalline grid
    "シューマン共鳴が証明する",  # the schumann resonance proves
    # --- conspirituality ---
    "隠蔽された研究が示す",  # suppressed research shows
    "彼らが隠していること",  # what they don't want you to know
    "禁じられた知識",  # forbidden knowledge
    "彼らが隠す真実",  # the truth they hide
    "禁止された情報",  # banned information
    # --- fraternal ---
    "古代の秘儀が教える",  # the ancient mysteries teach
    "秘密の教義が明かす",  # the secret doctrine reveals
    "内なる伝統が伝える",  # the inner tradition holds
]

# Source attribution: unnamed/vague authority claims
UNNAMED_AUTHORITY_PHRASES: list[str] = [
    # --- generic ---
    "科学者が言う",  # scientists say
    "専門家が認める",  # experts agree
    "研究が示す",  # studies show
    "研究が証明する",  # research proves
    "科学的に証明されている",  # it has been scientifically proven
    "医師が確認",  # doctors confirm
    "第一線の研究者",  # leading researchers
    "トップ科学者",  # top scientists
    "多数の研究",  # numerous studies
    "科学が示した",  # science has shown
    "データが確認する",  # data confirms
    "証拠が証明する",  # evidence proves
    "学者が認める",  # scholars agree
    "歴史家が確認する",  # historians confirm
    "情報筋によると",  # according to sources
    "内部関係者が明かす",  # insiders reveal
    # --- conspirituality ---
    "内部告発者が確認",  # whistleblowers confirm
    "元関係者が語る",  # former insiders say
    "独立系研究者が発見",  # independent researchers found
    "代替医療の医師が語る",  # alternative doctors say
    "検閲された専門家",  # censored experts
]

# Source attribution: verifiable citation markers (counter-signal — reduces score)
VERIFIABLE_CITATION_MARKERS: list[str] = [
    "に掲載",  # published in
    "et al.",
    "doi:",
    "https://",
    "ジャーナル",  # journal
    "大学の",  # university of
    "学会",  # proceedings of / academic society
    "isbn",
    "査読済み",  # peer-reviewed
    "vol.",
]

# Logical contradiction pairs: (label, pole_a_patterns, pole_b_patterns)
CONTRADICTION_PAIRS: list[tuple[str, list[str], list[str]]] = [
    (
        "エンパワーメント vs. 依存",  # empowerment vs. dependency
        ["あなたには力がある", "力はあなたの中に", "内なる力", "あなたが創造者"],
        ["これが必要", "従わなければならない", "導きがなければ", "私を通じてのみ"],
    ),
    (
        "普遍性 vs. 排他性",  # universality vs. exclusivity
        ["すべての道", "多くの道", "あらゆる道", "真実はどこにでも"],
        ["唯一の道", "唯一の方法", "唯一の真実", "他に道はない"],
    ),
    (
        "無裁き vs. 非難",  # non-judgement vs. blame
        ["裁かない", "裁きなく", "裁きから自由", "批判してはならない"],
        ["低い波動", "苦しみを引き寄せた", "カルマの負債", "この苦しみを選んだ"],
    ),
    (
        "エゴの解体 vs. エゴの肥大",  # ego dissolution vs. inflation
        ["エゴを手放す", "エゴを解放", "エゴは幻想", "エゴを溶かす", "エゴの死"],
        ["あなたは選ばれた", "あなたは特別", "選ばれし少数", "あなたの魂は進化している"],
    ),
    (
        "自律 vs. 疑念の抑圧",  # autonomy vs. doubt suppression
        ["直感を信じて", "自分を信じて", "内なる知恵", "あなた自身の真実"],
        ["疑いは恐れ", "疑いは抵抗", "エゴが抵抗している", "あなたの心は騙す"],
    ),
    (
        "無条件 vs. 取引的",  # unconditional vs. transactional
        ["無条件の愛", "条件のない愛", "愛は無償", "愛に値段はない"],
        ["離れたら", "進歩を失う", "遅れをとる", "この機会を逃す"],
    ),
    # --- prosperity gospel ---
    (
        "清貧の美徳 vs. 繁栄の約束",  # poverty virtue vs. prosperity promise
        ["貧しい者は幸い", "金は諸悪の根源", "清貧は美徳"],
        ["神はあなたに富を望む", "豊かさを宣言せよ", "繁栄はあなたの権利"],
    ),
    # --- cult ---
    (
        "共同体の愛 vs. 追放",  # community love vs. shunning
        ["私たちは家族", "無条件に愛している", "愛に満ちたコミュニティ"],
        ["コミュニティから追放", "もう歓迎されない", "除名される"],
    ),
    # --- fraternal ---
    (
        "開放性 vs. 誓約の秘密",  # openness vs. sworn secrecy
        ["すべての求道者を歓迎", "求める者すべてに開かれた", "誰も拒まない"],
        ["秘密を誓う", "誓約に縛られた", "血の誓約で封印", "秘儀を決して明かすな"],
    ),
]

# Commitment escalation: tiered markers for foot-in-the-door progression detection.
# Tier 1 = mild/invitational, Tier 2 = moderate/directive, Tier 3 = extreme/coercive.
COMMITMENT_ESCALATION_MARKERS: list[tuple[int, list[str]]] = [
    (
        1,
        [
            # --- generic ---
            "考えてみて",  # consider
            "かもしれません",  # you might
            "探求して",  # explore
            "役立つと感じる人もいます",  # some people find
            "試してみては",  # you could try
            "探求する価値がある",  # worth exploring
            "心を開いて",  # open your mind to / open your heart
            "少し時間を取って",  # take a moment to
            "振り返ってみて",  # reflect on
            "気づき始めて",  # begin to notice
            "発見するかもしれません",  # you may find
            "助けになる",  # it can help
            # --- commercial ---
            "無料セッションに参加",  # attend a free session
            # --- fraternal ---
            "ロッジを訪ねて",  # visit the lodge
        ],
    ),
    (
        2,
        [
            # --- generic ---
            "すべきです",  # you should
            "する必要がある",  # you need to
            "不可欠です",  # it is essential
            "重要です",  # it's important to
            "コミットして",  # commit to
            "専念して",  # dedicate yourself
            "投資をして",  # make the investment
            "今すぐ登録",  # enrol now
            "今日申し込む",  # sign up today
            "プログラムに参加",  # join the programme
            "次のステップへ",  # take the next step
            "もっと深く",  # go deeper
            "あなたは準備ができている",  # you are ready for
            # --- prosperity gospel ---
            "信仰の種を蒔く",  # sow a seed of faith
            # --- commercial ---
            "次のレベルへアップグレード",  # upgrade to the next level
            # --- fraternal ---
            "第一の位階を受けよ",  # take the first degree
        ],
    ),
    (
        3,
        [
            # --- generic ---
            "しなければならない",  # you must
            "選択肢はない",  # you have no choice
            "古い生活を捨てよ",  # abandon your old life
            "縁を切れ",  # cut ties with
            "ついてこない者を置いていけ",  # leave behind those who
            "私たちを通じてのみ",  # only through us
            "他に道はない",  # there is no other way
            "古い自分は死ななければ",  # your old self must die
            "完全な降伏",  # total surrender
            "完全な献身",  # complete devotion
            "すべての執着を断て",  # sever all attachments
            "すべてを捧げよ",  # give everything
            "財産を売り払え",  # sell your possessions
            "拒む者は",  # those who refuse will
            "完全なコミットメントが必要",  # full commitment required
            "ネガティブなコードを切れ",  # cut negative cords
            # --- prosperity gospel ---
            "全財産を捧げよ",  # give your life savings
            # --- fraternal ---
            "血の誓約を立てよ",  # swear the blood oath
        ],
    ),
]

# ---------------------------------------------------------------------------
# Keyword-based matching data
# ---------------------------------------------------------------------------
# Japanese morphology (SudachiPy tokenisation, particles, verb conjugation)
# makes exact substring matching unreliable. The structures below enable
# keyword / co-occurrence matching in the analysis engine. English markers
# leave the corresponding MarkerSet fields as None.

# Bare stems without particles — matched against token lemmas (no POS gate)
VAGUE_ADJECTIVE_STEMS: frozenset[str] = frozenset(
    {
        "神聖",  # sacred
        "宇宙",  # cosmic
        "永遠",  # eternal
        "崇高",  # sublime
        "神秘",  # mysterious
        "超越",  # transcendent
        "秘める",  # hidden/veiled (lemma form)
        "古代",  # ancient
        "聖",  # holy/sacred
        "祝福",  # blessed
        "預言",  # prophetic
        "波動",  # vibrational
        "活性",  # activated
        "隠蔽",  # suppressed
        "秘伝",  # initiatory
        "奥義",  # esoteric
    }
)

# Co-occurrence groups: (label, [keywords_that_must_all_appear_in_text])
# A group fires when ALL keywords in its list appear anywhere in the text.
AUTHORITY_KEYWORD_GROUPS: list[tuple[str, list[str]]] = [
    # --- generic スピリチュアル ---
    ("アセンデッドマスター+メッセージ", ["アセンデッドマスター", "メッセージ"]),
    ("チャネリング", ["チャネリング"]),
    ("銀河連合+介入", ["銀河連合", "介入"]),
    ("暴露+真実", ["暴露", "真実"]),
    ("アカシックレコード", ["アカシックレコード"]),
    ("古代+予言", ["古代", "予言"]),
    ("評議会+決定", ["評議会", "決定"]),
    ("アシュタール+伝言", ["アシュタール", "伝言"]),
    ("セント・ジャーメイン", ["セント・ジャーメイン"]),
    ("高次+存在+メッセージ", ["高次", "存在", "メッセージ"]),
    # --- prosperity gospel ---
    ("神+メッセージ", ["神さま", "メッセージ"]),
    ("主+啓示", ["主", "啓示"]),
    ("聖霊+言う", ["聖霊", "言"]),
    # --- cult ---
    ("長老+決定", ["長老", "決定"]),
    # --- fraternal ---
    ("グランドマスター", ["グランドマスター"]),
    ("秘密結社+明かす", ["秘密結社", "明か"]),
]

# Individual keywords whose presence indicates urgency
URGENCY_KEYWORDS: list[str] = [
    "今すぐ",  # right now
    "時間がない",  # no time
    "選ばれた",  # chosen
    "目覚め",  # awaken
    "ゲート",  # gate
    "ポータル",  # portal
    "閉じ",  # closing
    "従わ",  # comply/obey
    "種を蒔",  # sow seed
    "ブレイクスルー",  # breakthrough
    "残りわずか",  # limited spots
    "締め切り",  # deadline/closing
    "期間限定",  # limited time
    "最後のチャンス",  # last chance
    "手遅れ",  # too late
    "備え",  # prepare
    "タイムライン",  # timeline
]

# Co-occurrence groups for unfalsifiable source claims
UNFALSIFIABLE_KEYWORD_GROUPS: list[tuple[str, list[str]]] = [
    ("古代+叡智", ["古代", "叡智"]),
    ("量子場", ["量子場"]),
    ("高次元+明かす", ["高次元", "明か"]),
    ("宇宙+告げる", ["宇宙", "告げ"]),
    ("スピリット+啓示", ["スピリット", "啓示"]),
    ("アカシックフィールド", ["アカシックフィールド"]),
    ("光の存在+伝える", ["光の存在", "伝え"]),
    ("ソースエネルギー", ["ソースエネルギー"]),
    ("ディバインマトリックス", ["ディバインマトリックス"]),
    ("異次元+存在", ["異次元", "存在"]),
    ("スターシード", ["スターシード"]),
    ("グレートセントラルサン", ["グレートセントラルサン"]),
    ("クリスタルグリッド", ["クリスタルグリッド"]),
    ("シューマン共鳴+証明", ["シューマン共鳴", "証明"]),
    # --- conspirituality ---
    ("隠蔽+研究", ["隠蔽", "研究"]),
    ("隠す+真実", ["隠", "真実"]),
    ("禁じられた知識", ["禁じ", "知識"]),
    ("禁止+情報", ["禁止", "情報"]),
    # --- fraternal ---
    ("秘儀+教える", ["秘儀", "教え"]),
    ("秘密+教義", ["秘密", "教義"]),
    ("内なる伝統", ["内なる伝統"]),
]

# Individual keywords for unnamed authority claims
UNNAMED_AUTHORITY_KEYWORDS: list[str] = [
    "科学者",  # scientists
    "専門家",  # experts
    "研究が示",  # studies show
    "研究が証明",  # research proves
    "科学的に証明",  # scientifically proven
    "医師",  # doctors
    "第一線の研究",  # leading researchers
    "トップ科学者",  # top scientists
    "多数の研究",  # numerous studies
    "データが確認",  # data confirms
    "証拠が証明",  # evidence proves
    "学者",  # scholars
    "歴史家",  # historians
    "情報筋",  # sources
    "内部関係者",  # insiders
    # --- conspirituality ---
    "内部告発",  # whistleblower
    "元関係者",  # former insiders
    "独立系研究",  # independent researchers
    "代替医療",  # alternative medicine
    "検閲",  # censored
]

# Keyword-based contradiction poles
CONTRADICTION_KEYWORD_PAIRS: list[tuple[str, list[str], list[str]]] = [
    (
        "エンパワーメント vs. 依存",
        ["力がある", "内なる力", "あなたが創造者"],
        ["これが必要", "従わなければ", "導きがなければ", "私を通じてのみ"],
    ),
    (
        "普遍性 vs. 排他性",
        ["すべての道", "多くの道", "あらゆる道", "真実はどこにでも"],
        ["唯一の道", "唯一の方法", "唯一の真実", "他に道はない"],
    ),
    (
        "無裁き vs. 非難",
        ["裁かない", "裁きなく", "裁きから自由", "批判してはならない"],
        ["低い波動", "引き寄せた", "カルマの負債", "苦しみを選んだ"],
    ),
    (
        "エゴの解体 vs. エゴの肥大",
        ["エゴを手放す", "エゴを解放", "エゴは幻想", "エゴの死"],
        ["選ばれた", "あなたは特別", "選ばれし少数", "魂は進化"],
    ),
    (
        "自律 vs. 疑念の抑圧",
        ["直感を信じて", "自分を信じて", "内なる知恵", "あなた自身の真実"],
        ["疑いは恐れ", "疑いは抵抗", "エゴが抵抗", "心は騙す"],
    ),
    (
        "無条件 vs. 取引的",
        ["無条件の愛", "条件のない愛", "愛は無償", "愛に値段はない"],
        ["離れたら", "進歩を失う", "遅れをとる", "機会を逃す"],
    ),
    # --- prosperity gospel ---
    (
        "清貧の美徳 vs. 繁栄の約束",
        ["貧しい者は幸い", "金は諸悪の根源", "清貧は美徳"],
        ["神はあなたに富を望む", "豊かさを宣言", "繁栄はあなたの権利"],
    ),
    # --- cult ---
    (
        "共同体の愛 vs. 追放",
        ["私たちは家族", "無条件に愛", "愛に満ちたコミュニティ"],
        ["追放", "歓迎されない", "除名"],
    ),
    # --- fraternal ---
    (
        "開放性 vs. 誓約の秘密",
        ["すべての求道者を歓迎", "開かれた", "誰も拒まない"],
        ["秘密を誓う", "誓約に縛られた", "血の誓約", "秘儀を決して明かすな"],
    ),
]

# Keyword stems per tier for escalation detection
ESCALATION_KEYWORD_MARKERS: list[tuple[int, list[str]]] = [
    (
        1,
        [
            "考えてみて",  # consider
            "かもしれません",  # you might
            "探求",  # explore
            "役立つ",  # helpful
            "試してみ",  # try
            "心を開い",  # open your mind/heart
            "少し時間",  # take a moment
            "振り返",  # reflect
            "気づき",  # notice
            "発見する",  # discover
            "助けになる",  # it can help
            "無料セッション",  # free session
            "ロッジを訪ね",  # visit the lodge
        ],
    ),
    (
        2,
        [
            "すべきです",  # you should
            "する必要がある",  # you need to
            "不可欠",  # essential
            "重要です",  # important
            "コミット",  # commit
            "専念",  # dedicate
            "投資",  # investment
            "今すぐ登録",  # enrol now
            "今日申し込",  # sign up today
            "プログラムに参加",  # join the programme
            "次のステップ",  # next step
            "もっと深く",  # go deeper
            "準備ができている",  # you are ready
            "信仰の種",  # seed of faith
            "アップグレード",  # upgrade
            "第一の位階",  # first degree
        ],
    ),
    (
        3,
        [
            "しなければならない",  # you must
            "選択肢はない",  # no choice
            "古い生活を捨て",  # abandon old life
            "縁を切れ",  # cut ties
            "ついてこない者",  # leave behind those who
            "私たちを通じてのみ",  # only through us
            "他に道はない",  # no other way
            "古い自分は死な",  # old self must die
            "完全な降伏",  # total surrender
            "完全な献身",  # complete devotion
            "すべての執着を断て",  # sever all attachments
            "すべてを捧げよ",  # give everything
            "財産を売り払え",  # sell possessions
            "拒む者は",  # those who refuse
            "完全なコミットメント",  # full commitment
            "ネガティブなコード",  # negative cords (keyword stem)
            "全財産を捧げ",  # give life savings
            "血の誓約",  # blood oath
        ],
    ),
]
