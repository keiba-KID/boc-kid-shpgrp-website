"use strict";
/**
 * BOCサービスAPI ライブラリ
 */
// 結果定数
/* エラーコード */
const BOC_RESULT_CD                    = 'err_code';
/* エラーメッセージ */
const BOC_RESULT_MSG                   = 'err_msg';

// エラーコード定数
/** 成功 */
const BOC_NO_ERROR                     = 0;

/** DB接続失敗 */
const BOC_DB_CONNECT_ERROR             = -1001;
/** クエリー失敗 */
const BOC_DB_QUERY_ERROR               = -1002;
/** SQL失敗 */
const BOC_DB_SQL_ERROR                 = -1003;

/** 認証エラー(ログインCDに誤りがあります) */
const BOC_INVALID_LOGIN_CD             = -2001;
/** 認証エラー(パスワードに誤りがあります) */
const BOC_INVALID_PASSWORD             = -2002;

/** メール送信エラー */
const BOC_FAILED_SEND_MAIL             = -3001;

/** パラメータエラー */
const BOC_INVALID_PAPAMETER            = -4001;
/** ポイント不足 */
const BOC_NOT_ENOUGH_POINT             = -4002;

/** 保存エラー */
const BOC_FAILED_SAVE_FILE             = -5001;

/** 既に取得済み */
const BOC_ALREADY_GET                  = -6001;

/** 投票タイムアウト */
const BOC_TIMEOUT                      = -7001;

/** その他サービスエラー */
const BOC_SERVICE_ERROR                = -9999;

/** ランキング期間種別 */
const BOC_RANKING_MONTH       = 1;
const BOC_RANKING_YEAR        = 2;
const BOC_RANKING_FIRST_HALF  = 3;
const BOC_RANKING_LAST_HALF   = 4;

/** ランキング種別 */
const BOC_POINT_RANKING       = 1;
const BOC_HONMEI_RANKING      = 2;
const BOC_TANSHO_RANKING      = 3;
const BOC_FUKUSHO_RANKING     = 4;

/* 機能定義 */
const BOC_USE_VOTE                = 'vote';
const BOC_USE_RACE_MANAGE         = 'race_manage';
const BOC_USE_RACE_REGIST         = 'race_regist';
const BOC_USE_RACE_RESULT_REGIST  = 'race_result_regist';
const BOC_USE_SCORE_MANAGE        = 'score_manage';
const BOC_USE_USER_MANAGE         = 'user_manage';
const BOC_USE_UPDATE_USER_INFO    = 'update_user_info';
const BOC_USE_INPUT_USER_SCORE    = 'input_user_score';

/* 開催場所区分 */
const BOC_KBN_RACE_PLACE = {
  東京  : 'tk',
  京都  : 'ky',
  中山  : 'nk',
  阪神  : 'hn',
  福島  : 'fk',
  小倉  : 'kk',
  中京  : 'ck',
  新潟  : 'ng',
  札幌  : 'sp',
  函館  : 'hk',
  帯広  : 'ob',
  門別  : 'mn',
  盛岡  : 'mo',
  水沢  : 'mz',
  浦和  : 'ur',
  船橋  : 'fn',
  大井  : 'oi',
  川崎  : 'kw',
  金沢  : 'kn',
  笠松  : 'ks',
  名古屋  : 'na',
  園田  : 'so',
  姫路  : 'hm',
  高知  : 'kc',
  佐賀  : 'sg',
};

/**
 * ユーザー情報を登録する。
 * @param {in}  params  : 登録情報
 *                          - user_cd       : ユーザCD
 *                          - login_type    : ログイン種別(デフォルトはemail)
 *                          - login_cd      : ログインCD
 *                          - login_passwd  : ログインパスワード
 *                          - pr            : 自己PR
 *                          - user_type     : ユーザ種別(admin,staff,user)
 *                          - user_rank     : ユーザランク(0:無料会員,1:有料会員.2:VIP)
 * @return ユーザ情報
 *  - err_cd    : エラーCD
 *  - err_msg   : エラーmsg
 *  - user_info : ユーザ情報(tbl_userの情報)
 */
function boc_regist_user(params){
  return request_ajax('boc_regist_user', params);
}

/**
 * ユーザー登録時の認証番号送信
 * @param {in} user_info              登録するユーザー情報
 *               - login_type          ログイン種別(現在はemailのみ)
 *               - login_cd            ログインCD(現在はメールアドレスのみ)
 *               - user_name           ユーザ名
 * @return ユーザー情報
 *           - err_code                エラーコード
 *           - err_msg                 エラーメッセージ
 *           - confirm_number          認証番号
 */
function boc_send_user_regist_confirm(params){
  return request_ajax('boc_send_user_regist_confirm', params);
}

/**
 * ユーザ情報を取得する。
 * @param {in} params   - パラメータ
 *                        -user_cd        : ユーザCD
 * @return ユーザ情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 *          - user_info : ユーザ情報(tbl_userの情報)
 */
function boc_get_user_info(params){
  return request_ajax('boc_get_user_info', params);
}

/**
 * 公開可能なユーザー情報を取得する。
 * @param {in}  params : パラメータ
 *                        -user_cd        : ユーザCD
 * @return ユーザ情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 *          - user_info : ユーザ情報(公開可能なtbl_userの情報)
 */
function boc_get_public_user_info(params){
  return request_ajax('boc_get_public_user_info', params);
}

/**
 * ユーザ一覧を取得する。
 * @param {in}  params  - パラメータ(otion)
 *                        - ope_user_cd : 操作ユーザーCD
 *                        - user_name : ユーザ名
 * @return ユーザリスト
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 *          - user_list : ユーザ情報(tbl_userの情報)
 */
function boc_get_user_list(params=null){
  return request_ajax('boc_get_user_list', params);
}

/**
 * ユーザー情報を削除する
 * @param {in}  params  : パラメータ
 *                        - user_cd : ユーザーCD
 * @return ユーザリスト
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 */
function boc_delete_user(params){
  return request_ajax('boc_delete_user', params);
}

/**
 * 指定されたメールアドレスにログインCD,パスワードを送信する
 * @param {in} $email    送信先メールアドレス
 * @return エラー情報
 *           - err_code                エラーコード
 *           - err_msg                 エラーメッセージ
 */
function boc_reminder(email){
  var req_param = {
    login_cd : email
  };
  return request_ajax('boc_reminder', req_param);
}

/**
 * レース情報を登録する
 * @param {in} params   - レース情報
 *                          - race_cd       : レースCD
 *                          - race_date     : 開催日
 *                          - race_place    : 開催場所
 *                          - race_num      : レース番号
 *                          - race_name     : レース名
 *                          - race_time     : 発走時刻
 *                          - race_type     : レース種別(1:予想バトル予選,2:準決勝,3:決勝)
 *                          - race_month    : 集計月
 *                          - race_horses   : 出走馬[配列]
 *                              - horse_num   : 馬番
 *                              - horse_name  : 馬名
 * @return エラー情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 */
function boc_regist_race(params){
  return request_ajax('boc_regist_race', params);
}


/**
 * レース情報を削除する
 * @param {in}  params  : パラメータ
 *                        - race_cd : レースCD
 * @return エラー情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 */
function boc_delete_race(params){
  return request_ajax('boc_delete_race', params);
}

/**
 * レース一覧を取得する
 * @param {in} params   - パラメータ
 *                        - ope_user_cd : 操作ユーザーCD
 *                        - race_date   : 開催日(オプション)
 * @return レース一覧
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 *          - race_list : レース情報[配列](tbl_m_raceの情報)
 */
function boc_get_race_list(params){
  return request_ajax('boc_get_race_list', params);
}

/**
 * レース情報を取得する
 * @param {in} params     - パラメータ
 *                          - race_cd : レースCD
 * @return レース情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 *          - race_info : レース情報
 *                          - race_cd     : レースCD
 *                          - race_date   : 開催日
 *                          - race_place  : 開催場所
 *                          - race_num    : レース番号
 *                          - race_name   : レース名
 *                          - race_time   : 発走時刻
 *                          - race_type   : レース種別(1:予想バトル予選,2:準決勝,3:決勝)
 *                          - race_month  : 集計月
 *                          - race_horses : 出走馬[配列]
 *                              - horse_num   : 馬番号
 *                              - horse_name  : 馬名
 */
function boc_get_race_info(params){
  return request_ajax('boc_get_race_info', params);
}

/**
 * ログイン処理を行う
 * @param {in}  params  : パラメータ
 *                        - login_id      : user_cdまたはメールアドレス
 *                        - login_passwd  : ログインパスワード
 * @return ユーザー情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 *          - user_info : ユーザー情報(tbl_userの情報)
 * 
 */
function boc_login(params){
  return request_ajax('boc_login', params);
}

/**
 * 投票可能なレース一覧を取得する。
 * @param {in}  params  : パラメータ
 *                        - user_cd : ユーザーCD
 * @return ユーザー情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 *          - race_list : レース一覧[配列]
 *                        - race_cd     : レース名
 *                        - race_date   : 開催日
 *                        - race_place  : 開催場所
 *                        - race_num    : レース番号
 *                        - race_name   : レース名
 *                        - race_time   : 発走時刻
 *                        - vote_status : 投票済みかどうか(投票済みなら済を表示)
 */
function boc_get_vote_race(params){
  return request_ajax('boc_get_vote_race', params);
}

/**
 * 投票を行う
 * @param {in}  params  : パラメータ
 *                        - user_cd : ユーザーCD
 *                        - race_cd : レースCD
 *                        - mark1   : ◎馬番
 *                        - mark2   : ○馬番
 *                        - mark3   : ▲馬番
 *                        - mark4   : ☆馬番
 *                        - mark5   : 穴馬番
 *                        - mark6   : 消馬番
 */
function boc_vote(params){
  return request_ajax('boc_vote', params);
}

/**
 * 自身の投票データを取得する。
 * @param {in}  params  : パラメータ
 *                        - user_cd   : ユーザーCD
 *                        - race_cd   : レースCD
 * @return レース情報リスト
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 *          - vote_info : 投票情報()
 *          - sale_vote : 予想販売一覧
 */
function boc_get_vote(params){
  return request_ajax('boc_get_vote', params);
}


/**
 * レース結果を登録する。
 * @param {in}  params  - パラメータ
 *                        - race_cd       : レースCD
 *                        - race_type     : レース種別(1:予選バトル,2:準決勝,3:決勝)
 *                        - rank1_umaban  : 1着馬番
 *                        - rank1_ozz     : 1着オッズ
 *                        - rank1_pay1    : 1着単勝払い戻し
 *                        - rank1_pay2    : 1着複勝払い戻し
 *                        - rank2_umaban  : 2着馬番
 *                        - rank2_ozz     : 2着オッズ
 *                        - rank2_pay1    : 2着単勝払い戻し
 *                        - rank2_pay2    : 2着複勝払い戻し
 *                        - rank3_umaban  : 3着馬番
 *                        - rank3_ozz     : 3着オッズ
 *                        - rank3_pay1    : 3着単勝払い戻し
 *                        - rank3_pay2    : 3着複勝払い戻し
 *                        - d_rank1_umban : 消し馬1番人気馬番
 *                        - d_pt1         : 消し馬1番人気消しポイント
 *                        - d_rank2_umban : 消し馬2番人気馬番
 *                        - d_pt2         : 消し馬2番人気消しポイント
 *                        - d_rank3_umban : 消し馬3番人気馬番
 *                        - d_pt3         : 消し馬3番人気消しポイント
 *                        - d_rank4_umban : 消し馬4番人気馬番
 *                        - d_pt4         : 消し馬4番人気消しポイント
 *                        - d_rank5_umban : 消し馬5番人気馬番
 *                        - d_pt5         : 消し馬5番人気消しポイント
 *                        - d_rank6_umban : 消し馬6番人気馬番
 *                        - d_pt6         : 消し馬6番人気消しポイント
 *                        - d_rank7_umban : 消し馬7番人気馬番
 *                        - d_pt7         : 消し馬7番人気消しポイント
 *                        - d_rank8_umban : 消し馬8番人気馬番
 *                        - d_pt8         : 消し馬8番人気消しポイント
 * @return エラー情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 */
function boc_regist_race_result(params){
  return request_ajax('boc_regist_race_result', params);
}

/**
 * レース結果を取得する
 * @param {in}  params  : パラメータ
 *                        - race_cd : レースCD
 * @return エラー情報
 *          - err_cd      : エラーCD
 *          - err_msg     : エラーMSG
 *          - race_result : レース結果[配列](tbl_m_race_resultの情報)
 */
function boc_get_race_result(params){
  return request_ajax('boc_get_race_result', params);
}

/**
 * 各種ランキングリストを取得する。
 * @param {in}  params  : パラメータ
 *                        - ranking_type  : ランキング種別
 *                                          - BOC_POINT_RANKING   : ポイントランキング
 *                                          - BOC_HONMEI_RANKING  : ◎的中率ランキング
 *                                          - BOC_TANSHO_RANKING  : 単勝回収率ランキング
 *                                          - BOC_FUKUSHO_RANKING : 複勝回収率ランキング
 *                        - sum_type      : 集計期間
 *                                          - BOC_RANKING_MONTH       : 月間
 *                                          - BOC_RANKING_YEAR        : 年間
 *                                          - BOC_RANKING_FIRST_HALF  : 上半期
 *                                          - BOC_RANKING_LAST_HALF   : 下半期
 * @return  ランキングリスト
 *          - err_cd        : エラーCD
 *          - err_msg       : エラーMSG
 *          - month         : 集計月(sum_typeがBOC_RANKING_MONTHの時に設定される)
 *          - ranking_list  : ランキングリスト[配列]
 *                              - rank        : 順位
 *                              - user_cd     : ユーザーCD
 *                              - user_name   : ユーザー名
 *                              - v_count     : 参加回数
 *                              - pt          : ポイント合計
 *                              - mark1_rate  : ◎的中率
 *                              - mark2_rate  : 〇的中率
 *                              - mark3_rate  : ▲的中率
 *                              - mark4_rate  : ☆的中率
 *                              - mark5_rate  : 穴的中率
 *                              - mark6_rate  : 消的中率
 *                              - pay1_rate   : 単勝回収率
 *                              - pay2_rate   : 複勝回収率
 */
function boc_get_ranking_list(params){
  return request_ajax('boc_get_ranking_list', params);
}

/**
 * 投票履歴も含めたユーザー情報リストを取得する
 * 取得するリストは投票回数が多い順にソートされている。
 * @param {in}  params  : パラメータ(オプション)
 *                        - ope_user_cd : 操作ユーザーCD
 *                        - user_cd : ユーザーCD
 * @return  ランキングリスト
 *          - err_cd        : エラーCD
 *          - err_msg       : エラーMSG
 *          - user_list     : ユーザーリスト[配列]
 *                            - user_cd       : ユーザーCD
 *                            - user_name     : ユーザー名
 *                            - login_cd      : メールアドレス
 *                            - login_passwd  : ログインパスワード
 *                            - ranking_rank  : ランキング称号
 *                            - rabking_img   : ランキング称号画像
 *                            - vote_history  : 投票履歴[配列](v_user_voteの情報)
 *                            - vote_overview : 投票概要
 *                                              - month_ranking : 月間ランキング
 *                                                                - pt    : ポイント獲得数
 *                                                                - mark1_rate  : ◎的中率
 *                                                                - mark2_rate  : 〇的中率
 *                                                                - mark3_rate  : ▲的中率
 *                                                                - mark4_rate  : ☆的中率
 *                                                                - mark5_rate  : 穴的中率
 *                                                                - mark6_rate  : 消的中率
 *                                                                - pay1_rate   : 単勝回収率
 *                                                                - pay2_rate   : 複勝回収率
 *                                              - year_ranking : 年間ランキング
 *                                                                - pt    : ポイント獲得数
 *                                                                - mark1_hit   : ◎的中数
 *                                                                - mark1_rate  : ◎的中率
 *                                                                - mark2_hit   : 〇的中数
 *                                                                - mark2_rate  : 〇的中率
 *                                                                - mark3_hit   : ▲的中数
 *                                                                - mark3_rate  : ▲的中率
 *                                                                - mark4_hit   : ☆的中数
 *                                                                - mark4_rate  : ☆的中率
 *                                                                - mark5_hit   : 穴的中数
 *                                                                - mark5_rate  : 穴的中率
 *                                                                - mark6_hit   : 消的中数
 *                                                                - mark6_rate  : 消的中率
 *                                                                - pay1_rate   : 単勝回収率
 *                                                                - pay2_rate   : 複勝回収率
 *                                              - first_half_ranking : 上半期ランキング
 *                                                                - pt    : ポイント獲得数
 *                                                                - mark1_rate  : ◎的中率
 *                                                                - mark2_rate  : 〇的中率
 *                                                                - mark3_rate  : ▲的中率
 *                                                                - mark4_rate  : ☆的中率
 *                                                                - mark5_rate  : 穴的中率
 *                                                                - mark6_rate  : 消的中率
 *                                                                - pay1_rate   : 単勝回収率
 *                                                                - pay2_rate   : 複勝回収率
 *                                              - last_half_ranking : 下半期ランキング
 *                                                                - pt    : ポイント獲得数
 *                                                                - mark1_rate  : ◎的中率
 *                                                                - mark2_rate  : 〇的中率
 *                                                                - mark3_rate  : ▲的中率
 *                                                                - mark4_rate  : ☆的中率
 *                                                                - mark5_rate  : 穴的中率
 *                                                                - mark6_rate  : 消的中率
 *                                                                - pay1_rate   : 単勝回収率
 *                                                                - pay2_rate   : 複勝回収率
 */
function boc_get_user_info_list(params){
  return request_ajax('boc_get_user_info_list', params);
}

/**
 * ユーザーが指定された機能を使用できるかをチェック
 * @param {in}  params  - パラメータ
 *                        - func_name     : 機能名
 *                                          BOC_USE_VOTE                : 投票機能
 *                                          BOC_USE_RACE_MANAGE         : レース管理機能
 *                                          BOC_USE_RACE_REGIST         : レース登録機能
 *                                          BOC_USE_RACE_RESULT_REGIST  : レース結果登録機能
 *                                          BOC_USE_SCORE_MANAGE        : 成績管理機能
 *                                          BOC_USE_USER_MANAGE         : ユーザー管理機能
 *                                          BOC_USE_UPDATE_USER_INFO    : ユーザー情報更新機能
 *                                          BOC_USE_INPUT_USER_SCORE    : ユーザー成績入力機能
 *                        - ope_user_cd   : 操作ユーザーCD
 *                        - param1        : 各機能に付随するパラメータ
 *                                          BOC_USE_VOTE              なし
 *                                          BOC_USE_RACE_MANAGE       なし
 *                                          BOC_USE_RACE_REGIST       レースCD
 *                                          BOC_USE_SCORE_MANAGE      なし
 *                                          BOC_USE_USER_MANAGE       なし
 *                                          BOC_USE_UPDATE_USER_INFO  編集するユーザーCD
 *                                          BOC_USE_INPUT_USER_SCORE  なし
 * @return  エラー情報
 *          - err_cd        : エラーCD
 *          - err_msg       : エラーMSG
 */
function boc_check_use_function(params){
  return request_ajax('boc_check_use_function', params);
}



/**
 * ポイントを付与する
 * @param {in}  params  - パラメータ
 *                        - user_cd             : ユーザーCD
 *                        - pt                  : ポイント数
 *                        - from_user_cd        : ポイント送信元ユーザーCD(システムの場合は未設定)
 *                        - detail              : 備考(オプション)
 */
function boc_add_point(params){
  return request_ajax('boc_add_point', params);
}

/**
 * ポイントを他のユーザーに付与する
 * @param {in}  params  - パラメータ
 *                        - frm_user_cd           : 送信元ユーザーCD
 *                        - dst_user_cd           : 送信先ユーザーCD
 *                        - pt                    : ポイント数
 *                        - detail                : 備考
 */
function boc_give_point(params){
  return request_ajax('boc_give_point', params);
}

/**
 * ポイント履歴を取得する
 * @param {in}  - パラメータ  
 *                - user_cd       : ユーザーCD
 *                - frm_date      : 開始期間
 *                - dst_date      : 終了期間
 * @return  エラー情報
 *          - err_cd        : エラーCD
 *          - err_msg       : エラーMSG
 *          - pt_histories  : ポイント履歴情報
 *                              - user_cd           : ユーザーCD
 *                              - user_name         : ユーザー名
 *                              - update_date       : 更新日付
 *                              - sender_from       : 送信元/送信先ユーザーCD
 *                              - sender_from_name  : 送信元/送信先ユーザー名
 *                              - pt                : ポイント
 *                              - detail            : 備考
 */
function boc_get_point_history(params){
  return request_ajax('boc_get_point_history', params);
}


/**
 * 指定されたユーザーの使用可能ポイント数を取得する
 * @param {in} params   - パラメータ
 *                        - user_cd     : ユーザーCD
 * @return  エラー情報
 *          - err_cd        : エラーCD
 *          - err_msg       : エラーMSG
 *          - avaival_pt    : 保有ポイント
 */
function boc_get_total_avaival_point(params){
  return request_ajax('boc_get_total_avaival_point', params);
}

/**
 * 成績管理取得用のユーザーCDリストを取得する
 * @return  エラー情報
 *          - err_cd          : エラーCD
 *          - err_msg         : エラーMSG
 *          - score_user_cds  : ユーザーCDリスト[配列]
 *                              - user_cd         : ユーザーCD
 *                              - last_vote_date  : 最終対象レース日時
 */
function boc_get_scores_user_cd(params){
  return request_ajax('boc_get_scores_user_cd', params);
}

/**
 * 予想を購入する
 * @param {in}  params  : パラメータ
 *                        - user_cd     : ユーザーCD
 *                        - vote_id     : 購入する予想投票ID
 * @return エラー情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 *          - buy_user_cd : 購入対象のユーザーCD
 *          - buy_race_cd : 購入対象のレースCD
 */
function boc_buy_vote(params){
  return request_ajax('boc_buy_vote', params);
}

/**
 * 購入した予想を取得する
 * @param {in}  params  : パラメータ
 *                        - user_cd     : ユーザーCD
 *                        - vote_id     : 購入する予想投票ID
 * @return 購入した予想情報
 *          - err_cd      : エラーCD
 *          - err_msg     : エラーMSG
 *          - vote_info : 投票情報()
 */
function boc_get_buy_vote(params){
  return request_ajax('boc_get_buy_vote', params);
}

/////////////////////////////////////////////////
// これ以降、内部関数
//

/**
 * サービスをAjax形式でリクエストする。
 * @param {*} method        : メソッド名
 * @param {*} method_param  : メソッドパラメータ 
 * @param {*} cb            : コールバック(option)。設定されていれば非同期で結果が通知される 
 */
function request_ajax(method, method_param, cb = null){
  var req_result = {
    err_code         : BOC_NO_ERROR,
    err_msg          : ''
  };

  /* コールバックが指定されていれば非同期処理 */
  var is_async = false;
  if (cb != null)
  {
    is_async = true;
  }

  /* urlの設定 */
  var url = BOC_SERVICE_DOMAIN + "bin/service_controller.php?method=" + method;

  /* AJAX送信 */
  $.ajax(
  {
    type        : "POST",
    url         : "https://boc-kid.shpgrp.com/bin/service_controller.php?method=" + method,
    dataType	  : "json",
    data        : method_param,
    async       : is_async
  })
  .done( function( service_result )
  {
    if (cb != null)
    {
      cb(service_result);
    }
    else
    {
      req_result = service_result;
    }
  })
  .fail( function( result )
  {
    try{
      var check_result = JSON.parse(result.responseText);
      req_result = check_result;
      if (is_async)
      {
        cb(req_result);
      }
      else
      {
        req_result = result;
      }
    } catch(e){
      req_result['err_code']  = BOC_SERVICE_ERROR;
      req_result['err_msg']   = result.responseText;
    }
  });
  return req_result;
}