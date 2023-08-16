<?php
/******************************************
 * あ～らくサービス
 */
require_once(dirname(__FILE__) . '/common/db.php');		          // DBをインポート
require_once(dirname(__FILE__) . '/common/logger.php');		      // loggerをインポート

require_once(dirname(__FILE__) . '/service_config.php');        // サービス設定をインポート

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

/** データが存在しない */
const BOC_NOT_FOUND                    = -2003;

/** メール送信エラー */
const BOC_FAILED_SEND_MAIL             = -3001;

/** パラメータエラー */
const BOC_INVALID_PAPAMETER            = -4001;

/** 保存エラー */
const BOC_FAILED_SAVE_FILE             = -5001;

/** 既に取得済み */
const BOC_ALREADY_GET                  = -6001;

/** 投票タイムアウト */
const BOC_TIMEOUT                      = -7001;

/** 権限エラー */
const BOC_INVALID_USER_TYPE            = -8001;

/** その他サービスエラー */
const BOC_SERVICE_ERROR                = -9999;

/* ランキング期間種別 */
const BOC_RANKING_MONTH       = 1;
const BOC_RANKING_YEAR        = 2;
const BOC_RANKING_FIRST_HALF  = 3;
const BOC_RANKING_LAST_HALF   = 4;

/* ランキング種別 */
const BOC_POINT_RANKING       = 1;
const BOC_HONMEI_RANKING      = 2;
const BOC_TANSHO_RANKING      = 3;
const BOC_FUKUSHO_RANKING     = 4;
const BOC_VOTE_RANKING        = 5;

/* 機能定義 */
const BOC_USE_VOTE                = 'vote';
const BOC_USE_RACE_MANAGE         = 'race_manage';
const BOC_USE_RACE_REGIST         = 'race_regist';
const BOC_USE_RACE_RESULT_REGIST  = 'race_result_regist';
const BOC_USE_SCORE_MANAGE        = 'score_manage';
const BOC_USE_USER_MANAGE         = 'user_manage';
const BOC_USE_UPDATE_USER_INFO    = 'update_user_info';
const BOC_USE_INPUT_USER_SCORE    = 'input_user_score';



// テーブル定数
const SCHEMA_WASHAPP            = "boc";
const TBL_USER                  = SCHEMA_WASHAPP . ".tbl_user";
const TBL_USER_VOTE             = SCHEMA_WASHAPP . ".tbl_user_vote";
const TBL_M_RACE                = SCHEMA_WASHAPP . ".tbl_m_race";
const TBL_M_RACE_HORSE          = SCHEMA_WASHAPP . ".tbl_m_race_horse";
const TBL_M_RACE_RESULT         = SCHEMA_WASHAPP . ".tbl_m_race_result";
const TBL_M_USER_TYPE           = SCHEMA_WASHAPP . ".tbl_m_user_type";
const TBL_M_USER_RANK           = SCHEMA_WASHAPP . ".tbl_m_user_rank";
const TBL_RACE_DEL_HORSE        = SCHEMA_WASHAPP . ".tbl_race_del_horse";

// View定数
const V_USER_VOTE               = SCHEMA_WASHAPP . ".v_user_vote";
const V_USER_VOTE_RESULT        = SCHEMA_WASHAPP . ".v_user_vote_result";

// タイトル定数
const BOC_TITLE_WG              = 90;
const BOC_TITLE_G1              = 80;
const BOC_TITLE_G2              = 70;
const BOC_TITLE_G3              = 60;
const BOC_TITLE_OL              = 50;
const BOC_TITLE_W3              = 40;
const BOC_TITLE_W2              = 30;
const BOC_TITLE_W1              = 20;
const BOC_TITLE_UW              = 10;
const BOC_TITLE_NR              = 0;

const BOC_TITLE_INFO  = array(
  BOC_TITLE_NR  => array('name' => '新馬'           , 'img' => 'title_nr.png'),
  BOC_TITLE_UW  => array('name' => '未勝利'         , 'img' => 'title_uw.png'),
  BOC_TITLE_W1  => array('name' => '1勝クラス'      , 'img' => 'title_w1.png'),
  BOC_TITLE_W2  => array('name' => '2勝クラス'      , 'img' => 'title_w2.png'),
  BOC_TITLE_W3  => array('name' => '3勝クラス'      , 'img' => 'title_w3.png'),
  BOC_TITLE_OL  => array('name' => 'オープンクラス'  , 'img' => 'title_ol.png'),
  BOC_TITLE_G3  => array('name' => 'G3クラス'       , 'img' => 'title_g3.png'),
  BOC_TITLE_G2  => array('name' => 'G2クラス'       , 'img' => 'title_g2.png'),
  BOC_TITLE_G1  => array('name' => 'G1クラス'       , 'img' => 'title_g1.png'),
  BOC_TITLE_WG  => array('name' => '世界G1クラス'    , 'img' => 'title_wg.png'),
);

// 機能制限定義


/////////////////////////////////////////////////////////////
// 公開API関数                                                                                 
//

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
 function boc_send_user_regist_confirm($user_info){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'ad_infos'      => null
  );

  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    /* ログインCDとパスワードでチェック */
    if (!array_key_exists('login_type', $user_info) 
      ||!array_key_exists('login_cd', $user_info)){
      /* ログイン手段もログインCDも未設定ならパラメータエラー */
      throw new Exception("Invalid paramter. if user_cd is not found, you must set login_method and login_cd.", BOC_INVALID_PAPAMETER);
    }
    $sql  = "SELECT * FROM " . TBL_USER;
    $sql .= sprintf(" WHERE login_type = '%s'", $user_info['login_type']);
    $sql .= sprintf(" AND login_cd = '%s'", $user_info['login_cd']);
    $user_result = GetSqlResults($db, $sql);
    if (count($user_result) > 0){
      // 既にユーザーが存在する場合はエラー
      throw new Exception("Already email is used.", BOC_INVALID_LOGIN_CD);
    }
    // ここまで来れば認証番号を発行してメール送信
    // 認証番号を発行
    $str_confirm_number="";
    for($i=0;$i<6;$i++){
        $str_confirm_number.=mt_rand(0,9);
    }
    // メールを送信
    mb_language("Japanese");
    mb_internal_encoding("UTF-8");    
    /* 宛先 */
    $to = $user_info['login_cd'];
    /* タイトル */
    $title = "BOCコミュニティ【仮ユーザー登録】";
    /* メール本文 */
    $tpl_for_reminder = ABS_ROOT_PATH . "/bin/data/tpl_mail_confirm_number.txt";
    $content = file_get_contents($tpl_for_reminder);
    $content = sprintf($content, $user_info['user_name'], $str_confirm_number);

    // メール送信
    $result = boc_SendMail(array(
      'dest'      => $to,
      'sender'    => 'system@shpgrp.com',
      'subject'   => $title,
      'contents'  => $content,
    ));
    if ($result[BOC_RESULT_CD] != BOC_NO_ERROR){
      $result[BOC_RESULT_CD] = BOC_FAILED_SEND_MAIL;
      $result[BOC_RESULT_MSG] = 'Failed to mail to ' . $to;
      return $result;
    }
    // 認証番号を設定
    $result['confirm_number'] = $str_confirm_number;

  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
 }


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
function boc_regist_user($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'user_info'     => null
  );

  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // ユーザーCDが未設定ならレコードを追加する
    $user_cd = "";
    if (!array_key_exists('user_cd', $params)){
      /* ユーザーCDが未設定ならログインCDとパスワードでチェック */
      if (!array_key_exists('login_type', $params) 
        ||!array_key_exists('login_cd', $params)){
        /* ログイン手段もログインCDも未設定ならパラメータエラー */
        throw new Exception("Invalid paramter. if user_cd is not found, you must set login_type and login_cd.", BOC_INVALID_PAPAMETER);
      }
      $sql  = "SELECT * FROM " . TBL_USER;
      $sql .= sprintf(" WHERE login_type = '%s'", $params['login_type']);
      $sql .= sprintf(" AND login_cd = '%s'", $params['login_cd']);
      $user_result = GetSqlResults($db, $sql);
      if (count($user_result) == 0){
        /* ユーザーが存在しないのでこのタイミングでユーザーコードを作成 */
        /* ユーザーCDを取得 */
        $user_cd = md5(uniqid(mt_rand(1000000,9999999),1));
        $sql  = "INSERT INTO " . TBL_USER;
        $sql .= "(user_cd, login_type, login_cd, login_passwd, user_name)";
        $sql .= sprintf(" VALUES('%s','%s','%s','%s','%s');",
                        $user_cd, 
                        $params['login_type'],
                        $params['login_cd'],
                        $params['login_passwd'],
                        '');
        $sql .= " commit;";
        $update_result = array();
        $ret = ExecuteSelect($db, $sql, $update_result);
        if ($ret==false){
          throw new Exception("Failed to sql. " . $sql, BOC_DB_SQL_ERROR);
        }
      }
      else{
        /* 既にユーザが存在する場合はエラー */
        throw new Exception("Already email is used.", BOC_INVALID_LOGIN_CD);
      }
    }
    else{
      /* ユーザCDが指定されている場合はパラメータのuser_cdを使用する */
      $user_cd = $params['user_cd'];
    }

    /* ここまでくればレコードは存在するはずなので、レコードを更新 */
    foreach($params as $c => $v){
      info("column:$c val:$v");
      $sql = "UPDATE " . TBL_USER;
      if ($c == 'user_cd' || $c == 'method' || $c == 'mode'){
        info("Skipped $c");
        continue;
      }
      elseif ($c == 'user_name'
            ||$c == 'login_type'
            ||$c == 'login_cd'
            ||$c == 'login_passwd'
            ||$c == 'pr'
            ||$c == 'user_type'
            ){
        /* 文字列型 */
        $sql .= sprintf(" SET %s = '%s'", $c, $v);
        $sql .= sprintf(" WHERE user_cd = '%s';", $user_cd);
      }
      else if($c == 'user_rank'){
        /* 数値型 */        
        $sql .= sprintf(" SET %s = %s", $c, $v);
        $sql .= sprintf(" WHERE user_cd = '%s';", $user_cd);
      }
      else{
        throw new Exception( sprintf("Invalid paramter: %s = %s", $c, $v), BOC_INVALID_PAPAMETER );
      }
      $sql .= " COMMIT;";
      $update_result = array();
      $ret = ExecuteSelect($db, $sql, $update_result);
      if ($ret==false){
        throw new Exception("Failed to sql." . $sql, BOC_DB_SQL_ERROR);
      }
    }

    /* 更新後のユーザー情報を取得 */
    $sql = "SELECT * FROM " . TBL_USER;
    $sql .= sprintf(" WHERE user_cd = '%s'", $user_cd);
    $user_info = GetSqlResults($db, $sql);
    $result['user_info'] = $user_info[0];

    // modeがスーパーユーザーでなければ、メール送信を行う。
    if (!array_key_exists('mode', $params)){
      if (array_key_exists('login_cd', $params)){
        $email = $params['login_cd'];
        // 登録完了メールを送信
        mb_language("Japanese");
        mb_internal_encoding("UTF-8");    
        /* 宛先 */
        $to = $email;
        /* タイトル */
        $title = "BOCコミュニティ【登録完了】";
        /* メール本文 */
        $tpl_for_completed = ABS_ROOT_PATH . "/bin/data/tpl_mail_regist_completed.txt";
        $content = file_get_contents($tpl_for_completed);
        $content = sprintf($content, $user_info[0]['login_cd'], $user_info[0]['login_passwd']);

        // メール送信
        $mail_result = boc_SendMail(array(
          'dest'      => $to,
          'sender'    => 'system@shpgrp.com',
          'subject'   => $title,
          'contents'  => $content,
        ));
        if ($mail_result[BOC_RESULT_CD] != BOC_NO_ERROR){
          $result[BOC_RESULT_CD] = BOC_FAILED_SEND_MAIL;
          $result[BOC_RESULT_MSG] = 'Failed to mail to ' . $to;
          return $result;
        }
      }
    }
    elseif($params['mode'] == 'superuser'){
      /* スーパーユーザーなら入力したメールアドレスにユーザー情報の更新をメールでお知らせする。 */
      if (array_key_exists('login_cd', $params)){
        $email = $params['login_cd'];
        // 登録完了メールを送信
        mb_language("Japanese");
        mb_internal_encoding("UTF-8");    
        /* 宛先 */
        $to = $email;
        /* タイトル */
        $title = "BOCコミュニティ【ユーザー情報のお知らせ】";
        /* メール本文 */
        $tpl_for_completed = ABS_ROOT_PATH . "/bin/data/tpl_mail_update_user_info.txt";
        $content = file_get_contents($tpl_for_completed);
        $content = sprintf($content,
                    $user_info[0]['user_name'], 
                    $user_info[0]['user_cd'], 
                    $user_info[0]['user_name'], 
                    $user_info[0]['login_cd'], 
                    $user_info[0]['login_passwd']);

        // メール送信
        $mail_result = boc_SendMail(array(
          'dest'      => $to,
          'sender'    => 'system@shpgrp.com',
          'subject'   => $title,
          'contents'  => $content,
        ));
        if ($mail_result[BOC_RESULT_CD] != BOC_NO_ERROR){
          $result[BOC_RESULT_CD] = BOC_FAILED_SEND_MAIL;
          $result[BOC_RESULT_MSG] = 'Failed to mail to ' . $to;
          return $result;
        }
      }

    }
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
}

/**
 * 指定されたメールアドレスにログインCD,パスワードを送信する
 * @param {in}  params  パラメータ
 *                        - email    送信先メールアドレス
 * @return エラー情報
 *           - err_code                エラーコード
 *           - err_msg                 エラーメッセージ
 */
function boc_reminder($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => ""
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }
  
    /* パスワードを取得 */
    $email = $params['login_cd'];
    $sql  = "SELECT * FROM " . TBL_USER;
    $sql .= " WHERE login_type = 'email'";
    $sql .= sprintf(" AND login_cd = '%s'", $email);
    $user_result = GetSqlResults($db, $sql);
    if (count($user_result) == 0){
      throw new Exception("Invalid email. email=" . $email, BOC_INVALID_LOGIN_CD);
    }
  
    // 新規パスワードを発行
    $new_passwd = strtr(rtrim(base64_encode(pack('H*', hash('md5', uniqid(mt_rand(1000000,9999999)) ))), '='), '+/', '-_');
  
    /* パスワードを更新 */
    $sql = "UPDATE " . TBL_USER;
    $sql .= sprintf(" SET login_passwd = '%s'", $new_passwd);
    $sql .= " WHERE login_type = 'email'";
    $sql .= sprintf(" AND login_cd = '%s'", $email);
    $sql .= sprintf(" AND login_passwd = '%s';", $user_result[0]['login_passwd']);
    $sql .= " commit;";
    $update_array = array();
    $ret = ExecuteSelect($db, $sql, $update_array);
    if ($ret == false){
      throw new Exception("Failed to update password.", BOC_DB_SQL_ERROR);
    }
  
    // メールを送信
    mb_language("Japanese");
    mb_internal_encoding("UTF-8");    
    /* 宛先 */
    $to = $email;
    /* タイトル */
    $title = "BOCコミュニティ【仮パスワード発行】";
    /* メール本文 */
    $tpl_for_reminder = ABS_ROOT_PATH . "/bin/data/tpl_mail_reminder.txt";
    $content = file_get_contents($tpl_for_reminder);
    $content = sprintf($content, $user_result[0]['login_cd'], $new_passwd);
  
    // メール送信
    $result = boc_SendMail(array(
      'dest'      => $to,
      'sender'    => 'system@aobconsulting.co.jp',
      'subject'   => $title,
      'contents'  => $content,
    ));
    if ($result[BOC_RESULT_CD] != BOC_NO_ERROR){
      $result[BOC_RESULT_CD] = BOC_FAILED_SEND_MAIL;
      $result[BOC_RESULT_MSG] = 'Failed to mail to ' . $to;
      return $result;
    }
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
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
function boc_get_user_info($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'user_info'      => null
  );
  
  try{
    if (array_key_exists('mode', $params)){
      if ($params['mode'] != 'superuser'){
        throw new Exception('権限がありません。理由:modeがsuperuserでない', BOC_INVALID_USER_TYPE);
      }
      /* ログインユーザーの権限をチェック */
      if (!array_key_exists('self_user_cd', $params)){
        /* モードがスーパーユーザーでログインユーザーCDがなければ不正アクセス */
        throw new Exception('権限がありません。理由:self_user_cdが存在しない', BOC_INVALID_USER_TYPE);
      }
      /* 公開情報を取得 */
      debug("self_user_cd: ".$params['self_user_cd']);
      $svc_result = boc_get_public_user_info(
        array('user_cd' => $params['self_user_cd'])
      );
      if ($svc_result[BOC_RESULT_CD] != BOC_NO_ERROR){
        /* 正常に公開ユーザー情報を取得できなければエラー */
        throw new Exception('権限がありません。理由：ユーザーが存在しない', BOC_INVALID_USER_TYPE);
      }
      /* ユーザー種別をチェック */
      if ($svc_result['user_info']['user_type'] != 'superuser'){
        throw new Exception('権限がありません。理由：ユーザーは存在するが、superuserでない', BOC_INVALID_USER_TYPE);
      }
    }

    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // ユーザ情報を取得
    $sql = sprintf("SELECT * FROM %s WHERE user_cd= '%s';", TBL_USER, $params['user_cd']);
    $user_result = GetSqlResults($db, $sql);
    if (count($user_result) == 0){
      throw new Exception("Not Found user. user_cd=" . $params['user_cd'], BOC_NOT_FOUND);
    }
    $result['user_info'] = $user_result[0];
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
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
function boc_get_public_user_info($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'user_info'      => null
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // ユーザ情報を取得
    $sql = sprintf("SELECT user_cd,user_name,user_type,user_rank FROM %s WHERE user_cd= '%s';", TBL_USER, $params['user_cd']);
    $user_result = GetSqlResults($db, $sql);
    if (count($user_result) == 0){
      throw new Exception("Not Found user. user_cd=" . $params['user_cd'], BOC_NOT_FOUND);
    }
    $result['user_info'] = $user_result[0];
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;

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
function boc_get_user_list($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'user_list'      => null
  );
  
  try{
    // 権限チェック
    if (!array_key_exists('ope_user_cd', $params)){
      // 操作ユーザーCDが存在しなければ権限エラー
      throw new Exception('Invalid user type.', BOC_INVALID_USER_TYPE);
    }
    // 権限チェック
    $svc_result = boc_check_use_function(array(
      'func_name'   => BOC_USE_USER_MANAGE,
      'ope_user_cd' => $params['ope_user_cd']
    ));
    if ($svc_result[BOC_RESULT_CD] != BOC_NO_ERROR){
      throw new Exception('Invalid user type.', BOC_INVALID_USER_TYPE);
    }
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }
    // ユーザリストを取得する
    $sql  = "SELECT";
    $sql .= " m.user_cd,";
    $sql .= " m.user_name,";
    // セキュリティ対策 不要な情報はクライアントに返さない
    // $sql .= " m.login_type,";
    // $sql .= " m.login_cd,";
    // $sql .= " m.login_passwd,";
    $sql .= " m1.name as user_type_name,";
    $sql .= " m2.rank_name as user_rank_name";
    $sql .= " FROM ".TBL_USER." m";
    $sql .= " left join ".TBL_M_USER_TYPE." m1 on m.user_type = m1.user_type"; 
    $sql .= " left join ".TBL_M_USER_RANK." m2 on m.user_rank = m2.rank_id";
    if (array_key_exists('user_name', $params)){
      $sql .= " WHERE m.user_name like '%" . $params['user_name'] . "%'";
    }
    $sql .= " order by m.user_cd";
    info($sql);
    $result['user_list'] = GetSqlResults($db, $sql);
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
}

/**
 * ユーザー情報を削除する
 * @param {in}  params  : パラメータ
 *                        - user_cd : ユーザーCD
 * @return ユーザリスト
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 */
function boc_delete_user($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => ""
  );
  
  try{
    // ユーザー権限をチェック
    if (!checkUserType($params['self_user_cd'],'superuser')){
      throw new Exception('Not authorized', BOC_DB_CONNECT_ERROR);
    }

    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_INVALID_USER_TYPE);
    }

    // 関連テーブルからユーザー情報を削除
    $sql  = " DELETE FROM %s WHERE user_cd = '%s';";
    $sql .= " DELETE FROM %s WHERE user_cd = '%s';";
    $sql .= " commit;";
    $sql = sprintf($sql, TBL_USER_VOTE, $params['user_cd'], TBL_USER, $params['user_cd']);
    $update_array = array();
    $ret = ExecuteSelect($db, $sql, $update_array);
    if ($ret==false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
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
function boc_regist_race($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => ""
  );
  
  try{
    // ユーザー権限をチェック
    if (!checkUserType($params['self_user_cd'],'staff')){
      throw new Exception('Not authorized', BOC_DB_CONNECT_ERROR);
    }

    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // 既存データが存在するかをチェック
    $sql = sprintf("SELECT * FROM %s", TBL_M_RACE);
    $sql .= sprintf(" WHERE race_cd = '%s'", $params['race_cd']);
    $sql_result = GetSqlResults($db, $sql);
    if (count($sql_result)==0){
      /* レコードが存在しないのでレコードを追加 */
      $sql = sprintf("INSERT INTO %s(race_cd) VALUES('%s')", TBL_M_RACE, $params['race_cd']);
      $update_array = array();
      $ret = ExecuteSelect($db, $sql, $update_array);
      if ($ret==false){
        throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
      }
    }
    // ここまで来ればレコードは存在しているはず
    foreach($params as $c => $v){
      $sql = sprintf("UPDATE %s ", TBL_M_RACE);
      if ($c=='method' || $c=='race_cd' || $c=='race_horses'){
        continue;
      }
      elseif(  $c=='race_date'
            || $c=='race_place'
            || $c=='race_name'
            || $c=='race_time'
      ){
        /* 文字型、日付型 */
        $sql .= sprintf("SET %s = '%s'", $c, $v);
      }
      elseif(  $c=='race_num'
            || $c=='race_type'
            || $c=='race_month'
      ){
        /* 数字型 */
        $sql .= sprintf("SET %s = %s", $c, $v);
      }
      else{
        /* 上記以外は無視 */
        warn( sprintf("ignore column: %s", $c) );
        continue;
      }
      $sql .= sprintf(" WHERE race_cd = '%s';", $params['race_cd']);
      $sql .= " commit;";
      $update_array = array();
      $ret = ExecuteSelect($db, $sql, $update_array);
      if ($ret==false){
        throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
      }
    }
    /* 馬番情報を更新 */
    if (array_key_exists('race_horses', $params)){
      $sql  = sprintf("DELETE FROM %s WHERE race_cd='%s';", TBL_M_RACE_HORSE, $params['race_cd']);
      $sql .= " commit;";
      $update_array = array();
      $ret = ExecuteSelect($db, $sql, $update_array);
      if ($ret==false){
        throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
      }

      foreach($params['race_horses'] as $horse_info){
        $sql .= "INSERT INTO %s(race_cd, horse_num, horse_name)";
        $sql .= " VALUES('%s', %d, '%s');";
        $sql = sprintf($sql, TBL_M_RACE_HORSE, $params['race_cd'], $horse_info['horse_num'], $horse_info['horse_name']);
        $sql .= " commit;";
        $ret = ExecuteSelect($db, $sql, $update_array);
        if ($ret==false){
          throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
        }
      }
    }

  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
}

/**
 * レース情報を削除する
 * @param {in}  params  : パラメータ
 *                        - race_cd : レースCD
 * @return エラー情報
 *          - err_cd    : エラーCD
 *          - err_msg   : エラーMSG
 */
function boc_delete_race($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => ""
  );
  
  try{
    // ユーザー権限をチェック
    $svc_result = boc_check_use_function(array(
      'func_name'   => BOC_USE_RACE_REGIST,
      'ope_user_cd' => $params['self_user_cd'],
      'param1'      => $params['race_cd']
    ));
    if ($svc_result[BOC_RESULT_CD] != BOC_NO_ERROR){
      throw new Exception('Invalid User type', BOC_INVALID_USER_TYPE);
    }

    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // レース情報を削除
    $race_cd = $params['race_cd'];
    $sql  = sprintf("delete from %s where race_cd = '%s';", TBL_M_RACE, $race_cd);
    $sql .= " commit;";
    $update_array = array();
    $ret = ExecuteSelect($db, $sql, $update_array);
    if ($ret==false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }

    // 出馬情報を削除
    $sql  = sprintf("delete from %s where race_cd = '%s';", TBL_M_RACE_HORSE, $race_cd);
    $sql .= " commit;";
    $update_array = array();
    $ret = ExecuteSelect($db, $sql, $update_array);
    if ($ret==false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }

    // レース結果を削除
    $sql  = sprintf("delete from %s where race_cd = '%s';", TBL_M_RACE_RESULT, $race_cd);
    $sql .= " commit;";
    $update_array = array();
    $ret = ExecuteSelect($db, $sql, $update_array);
    if ($ret==false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }

    // 消し馬を削除
    $sql  = sprintf("delete from %s where race_cd = '%s';", TBL_RACE_DEL_HORSE, $race_cd);
    $sql .= " commit;";
    $update_array = array();
    $ret = ExecuteSelect($db, $sql, $update_array);
    if ($ret==false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }

    // 関連するユーザー投票データを削除
    $sql  = sprintf("delete from %s where race_cd = '%s';", TBL_USER_VOTE, $race_cd);
    $sql .= " commit;";
    $update_array = array();
    $ret = ExecuteSelect($db, $sql, $update_array);
    if ($ret==false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }

  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
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
function boc_get_race_list($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'race_list'      => null
  );
  
  try{
    // 権限チェック
    if (!array_key_exists('ope_user_cd', $params)){
      throw new Exception('Invalid user type.', $params);
    }
    $svc_result = boc_check_use_function(array(
      'func_name'    => BOC_USE_RACE_MANAGE,
      'ope_user_cd'  => $params['ope_user_cd']
    ));
    if ($svc_result[BOC_RESULT_CD] != BOC_NO_ERROR){
      throw new Exception('Invalid user type.', $params);
    }
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // レース一覧を取得する
    $sql = sprintf("SELECT * FROM %s", TBL_M_RACE);
    if (array_key_exists('race_date', $params)){
      $sql .= sprintf(" WHERE race_date = '%s'", $params['race_date']);
    }
    $sql .= " order by race_time desc";
    $sql_result = GetSqlResults($db, $sql);
    $result['race_list'] = $sql_result;
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
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
function boc_get_race_info($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'race_list'      => null
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // レース基本情報を取得
    $sql  = sprintf("SELECT * FROM %s", TBL_M_RACE);
    $sql .= sprintf(" WHERE race_cd = '%s'", $params['race_cd']);
    $sql_result = GetSqlResults($db, $sql);
    if (count($sql_result)==0){
      throw new Exception("Not Found race. race_cd:".$params['race_cd'], BOC_NOT_FOUND);
    }
    // 出走馬情報を取得
    $sql  = "SELECT * FROM %s";
    $sql .= " WHERE race_cd = '%s'";
    $sql .= " ORDER BY horse_num";
    $sql = sprintf($sql, TBL_M_RACE_HORSE, $params['race_cd']);
    $race_horses = GetSqlResults($db, $sql);
    $result['race_info'] = $sql_result[0];
    $result['race_info']['race_horses'] = $race_horses;
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }

  return $result;
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
function boc_login($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'user_info'      => null
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // まずuser_cdとパスワードでチェック
    $sql  = "SELECT user_cd,user_name,user_type,user_rank FROM %s";
    $sql .= " WHERE user_cd = '%s'";
    $sql .= " AND login_passwd = '%s'";
    $sql = sprintf($sql, TBL_USER, $params['login_id'], $params['login_passwd']);
    $user_result = GetSqlResults($db, $sql);
    if (count($user_result)>0){
      /* ユーザーを発見したのでこれ以上の処理は不要 */
      $result['user_info'] = $user_result[0];
      return $result;
    }

    /* 次にメールアドレスとパスワードでチェック */
    $sql  = "SELECT user_cd,user_name,user_type,user_rank FROM %s";
    $sql .= " WHERE login_type = 'email'";
    $sql .= " AND login_cd = '%s'";
    $sql .= " AND login_passwd = '%s'";
    $sql = sprintf($sql, TBL_USER, $params['login_id'], $params['login_passwd']);
    $user_result = GetSqlResults($db, $sql);
    if (count($user_result)>0){
      /* ユーザーを発見したのでこれ以上の処理は不要 */
      $result['user_info'] = $user_result[0];
      return $result;
    }

    /* ここまで来たらユーザーは存在しない */
    throw new Exception("Not Found user.", BOC_NOT_FOUND);
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }
  return $result;
}

/**
 * 投票可能なレース一覧を取得する。
 * @param {in}  params  : パラメータ
 *                        - user_cd   : ユーザーCD
 *                        - race_date : レース日
 * @return レース情報リスト
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
function boc_get_vote_race($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'race_list'      => null
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // まだ締め切りになっていないレース一覧を取得
    $sql  = "SELECT";
    $sql .= " race_cd,";
    $sql .= " race_date,";
    $sql .= " race_place,";
    $sql .= " race_num,";
    $sql .= " race_name,";
    $sql .= " race_time";
    $sql .= " FROM " . TBL_M_RACE;
    $sql .= " WHERE CURRENT_TIMESTAMP < (race_time  + '-2 minutes')";
    $sql .= " ORDER BY race_time";    
    $vote_race_result = GetSqlResults($db, $sql);
    if (count($vote_race_result) > 0){
      /* 投票可能なレースに対して自身が投票済みかをチェック */
      $vote_idx = 0;
      foreach($vote_race_result as $vote_race){
        $sql = sprintf("SELECT * FROM %s WHERE race_cd = '%s' AND user_cd = '%s'"
                , TBL_USER_VOTE, $vote_race['race_cd'], $params['user_cd']);
        $vote_result = GetSqlResults($db, $sql);
        if (count($vote_result) > 0){
          $vote_race_result[$vote_idx]['vote_status'] = '済';
        }
        else{
          $vote_race_result[$vote_idx]['vote_status'] = '';
        }
        $vote_idx++;
      }
      $result['race_list'] = $vote_race_result;
    }
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }
  return $result;
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
function boc_vote($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'race_list'      => null
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // レース情報を取得
    $sql = sprintf("SELECT * FROM %s WHERE race_cd = '%s' AND CURRENT_TIMESTAMP < (race_time  + '-2 minutes')"
            , TBL_M_RACE, $params['race_cd']);
    $sql_result = GetSqlResults($db, $sql);
    if (count($sql_result)==0){
      throw new Exception("vote is timeout.", BOC_TIMEOUT);
    }

    /* 既存レコードが存在しなければ追加する */
    $vote_id = 0;
    $sql = sprintf("SELECT * FROM %s WHERE user_cd = '%s' and race_cd = '%s'"
            , TBL_USER_VOTE, $params['user_cd'], $params['race_cd']);
    $sql_result = GetSqlResults($db, $sql);
    if (count($sql_result)==0){
      /* レコードが存在しないので追加 */
      $sql  = "INSERT INTO %s(vote_id, user_cd, race_cd)";
      $sql .= " SELECT case when MAX(vote_id) is null then 1 else MAX(vote_id) + 1 end as max_vote_id";
      $sql .= " ,'%s'";
      $sql .= " ,'%s'";
      $sql .= " FROM %s;";
      $sql .= " commit;";
      $sql = sprintf($sql, TBL_USER_VOTE, $params['user_cd'], $params['race_cd'], TBL_USER_VOTE);
      $update_array = array();
      $ret = ExecuteSelect($db, $sql, $update_array);
      if ($ret==false){
        throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
      }
      /* 追加された投票IDを取得 */
      $sql = sprintf("SELECT MAX(vote_id) as max_vote_id FROM %s WHERE user_cd='%s'"
              , TBL_USER_VOTE, $params['user_cd']);
      $sql_result = GetSqlResults($db, $sql);
      $vote_id = $sql_result[0]['max_vote_id'];
    }
    else{
      /* 存在する場合は既存のvote_idを設定 */
      $vote_id = $sql_result[0]['vote_id'];
    }
    // ここまでくれば必ずレコードは存在するのでupdateを行う
    $mark1 = $params['mark1'];
    $mark2 = 0;
    if (array_key_exists('mark2', $params)){
      $mark2 = $params['mark2'];
    }
    $mark3 = 0;
    if (array_key_exists('mark3', $params)){
      $mark3 = $params['mark3'];
    }
    $mark4 = 0;
    if (array_key_exists('mark4', $params)){
      $mark4 = $params['mark4'];
    }
    $mark5 = $params['mark5'];
    $mark6 = $params['mark6'];

    $sql  = "UPDATE %s SET mark1 = %d"; /* ◎ */
    $sql .= " ,mark2 = %d";             /* ○ */
    $sql .= " ,mark3 = %d";             /* ▲ */
    $sql .= " ,mark4 = %d";             /* ☆ */
    $sql .= " ,mark5 = %d";             /* 穴 */
    $sql .= " ,mark6 = %d";             /* 消 */
    $sql .= " WHERE vote_id = %d";
    $sql = sprintf($sql, TBL_USER_VOTE, $mark1, $mark2, $mark3, $mark4, $mark5, $mark6, $vote_id);
    $update_array = array();
    $ret = ExecuteSelect($db, $sql, $update_array);
    if ($ret==false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }
  return $result;
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
 */
function boc_get_vote($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'vote_info'      => null
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }
    // 投票データを取得
    $sql = sprintf("SELECT * FROM %s WHERE race_cd='%s' and user_cd='%s'"
            , V_USER_VOTE, $params['race_cd'], $params['user_cd']);
    $sql_result = GetSqlResults($db, $sql);
    if (count($sql_result)>0){
      $result['vote_info'] = $sql_result[0];  
    }
            
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }
  return $result;
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
function boc_regist_race_result($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'vote_info'      => null
  );
  
  try{
    // ユーザー権限をチェック
    if (!checkUserType($params['self_user_cd'],'staff')){
      throw new Exception('Not authorized', BOC_DB_CONNECT_ERROR);
    }

    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // 既存データを削除
    $race_cd = $params['race_cd'];
    $sql  = "DELETE FROM %s WHERE race_cd='%s';";
    $sql .= " commit;";
    $sql = sprintf($sql, TBL_M_RACE_RESULT, $race_cd);
    $update_result = array();
    $ret = ExecuteSelect($db, $sql, $update_result);
    if ($ret == false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }

    // 消し馬の既存データも削除
    $sql  = "DELETE FROM %s WHERE race_cd='%s';";
    $sql .= " commit;";
    $sql = sprintf($sql, TBL_RACE_DEL_HORSE, $race_cd);
    $update_result = array();
    $ret = ExecuteSelect($db, $sql, $update_result);
    if ($ret == false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }

    // 改めてレース結果を登録
    /* 1着データ */
    $sql  = "INSERT INTO %s(race_cd, race_rank, horse_num, last_ozz, pay1, pay2)";
    $sql .= " VALUES('%s', %d, %d, %s, %d, %d);";
    $sql .= " commit;";
    $sql = sprintf($sql, 
            TBL_M_RACE_RESULT, $race_cd, 1
            , $params['rank1_umaban'], $params['rank1_ozz'], $params['rank1_pay1'], $params['rank1_pay2']);
    $ret = ExecuteSelect($db, $sql, $update_result);
    if ($ret == false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }
    /* 2着データ */
    $sql  = "INSERT INTO %s(race_cd, race_rank, horse_num, last_ozz, pay2)";
    $sql .= " VALUES('%s', %d, %d, %s, %d);";
    $sql .= " commit;";
    $sql = sprintf($sql, 
            TBL_M_RACE_RESULT, $race_cd, 2
            , $params['rank2_umaban'], $params['rank2_ozz'], $params['rank2_pay2']);
    $ret = ExecuteSelect($db, $sql, $update_result);
    if ($ret == false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }
    /* 3着データ */
    $sql  = "INSERT INTO %s(race_cd, race_rank, horse_num, last_ozz, pay2)";
    $sql .= " VALUES('%s', %d, %d, %s, %d);";
    $sql .= " commit;";
    $sql = sprintf($sql, 
            TBL_M_RACE_RESULT, $race_cd, 3
            , $params['rank3_umaban'], $params['rank3_ozz'], $params['rank3_pay2']);
    $ret = ExecuteSelect($db, $sql, $update_result);
    if ($ret == false){
      throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
    }

    // 消し馬情報も登録
    for($di=1; $di<=8; $di++){
      if ( array_key_exists('d_rank'.$di.'_umban', $params)
        && !empty($params['d_rank'.$di.'_umban'])){
        $sql = "INSERT INTO %s(race_cd, d_rank, umaban, del_point)";
        $sql .= " VALUES('%s', %d, %d, %d);";
        $sql .= " commit;";
        $sql = sprintf($sql, 
                TBL_RACE_DEL_HORSE, $race_cd, $di
                , $params['d_rank'.$di.'_umban'], $params['d_pt'.$di]);
        $ret = ExecuteSelect($db, $sql, $update_result);
        if ($ret == false){
          throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
        }
      }
    }

    /* このレースで穴馬投票が有効かをチェック */
    // 1着から3着まで全て消し馬候補で決まった場合は人気決着したものとして
    // 穴馬投票は無効とする。
    $is_dark_horse_enable = false;
    for($ri=1; $ri<=3; $ri++){
      $chk_umaban = $params['rank'.$ri.'_umaban'];
      $is_found = false;
      for($di=1; $di<=8; $di++){
        if ( array_key_exists('d_rank'.$di.'_umban', $params)
          && array_key_exists('d_pt'.$di, $params)
          && $params['d_pt'.$di]>0){
          if ($chk_umaban == $params['d_rank'.$di.'_umban']){
            /* 人気馬と判定 */
            $is_found = true;
            break;
          }
        }
      }
      if ($is_found) continue;
      /* ここまで来たら消し候補馬以外が馬券内に来たと判断して穴馬投票は有効 */
      $is_dark_horse_enable = true;
      break;
    }

    /* 投票結果に対して各結果を反映 */
    $sql = sprintf("SELECT * FROM %s WHERE race_cd = '%s'"
            , TBL_USER_VOTE, $race_cd);
    $votes = GetSqlResults($db, $sql);
    $vote_count = count($votes);
    if ($votes>0){
      for($i=0; $i<$vote_count; $i++){
        $vote_info = $votes[$i];
        $v_pay1 = 0;
        $v_pay2 = 0;
        $v_mark1_pt = 0;
        $v_mark2_pt = 0;
        $v_mark3_pt = 0;
        $v_mark4_pt = 0;
        $v_mark5_pt = 0;
        $v_mark6_pt = 0;
        $v_bonus1 = 0;  /* 単勝ボーナス */
        $v_bonus2 = 0;  /* 馬連ボーナス */
        $v_bonus3 = 0;  /* ３複ボーナス */

        /* ◎判定 */
        if (   $vote_info['mark1'] == $params['rank1_umaban']
            || $vote_info['mark1'] == $params['rank2_umaban']
            || $vote_info['mark1'] == $params['rank3_umaban']
            ){
          /* 馬券内ならまず◎ポイントと複勝を設定 */
          if ($vote_info['mark1'] == $params['rank1_umaban']){
            /* 1着ならポイント、単勝、複勝を設定 */
            $v_mark1_pt = $params['rank1_ozz'];
            $v_pay1 = $params['rank1_pay1'];
            $v_pay2 = $params['rank1_pay2'];
          }
          if ($vote_info['mark1'] == $params['rank2_umaban']){
            /* 2着ならポイント、複勝を設定 */
            $v_mark1_pt = $params['rank2_ozz'];
            $v_pay2 = $params['rank2_pay2'];
          }
          if ($vote_info['mark1'] == $params['rank3_umaban']){
            /* 3着ならポイント、複勝を設定 */
            $v_mark1_pt = $params['rank3_ozz'];
            $v_pay2 = $params['rank3_pay2'];
          }
          // 単勝ボーナスは後で設定する
          if ($vote_info['mark1'] == $params['rank1_umaban']){
            $v_bonus1 = 200;
          }
        }
        /* ○判定 */
        if (   $vote_info['mark2'] == $params['rank1_umaban']
            || $vote_info['mark2'] == $params['rank2_umaban']
            || $vote_info['mark2'] == $params['rank3_umaban']
            ){
          /* 馬券内ならまず○ポイントを設定 */
          if ($vote_info['mark2'] == $params['rank1_umaban']){
            /* 1着ならポイントを設定 */
            $v_mark2_pt = $params['rank1_ozz'];
          }
          if ($vote_info['mark2'] == $params['rank2_umaban']){
            /* 2着ならポイント */
            $v_mark2_pt = $params['rank2_ozz'];
          }
          if ($vote_info['mark2'] == $params['rank3_umaban']){
            /* 3着ならポイントを設定 */
            $v_mark2_pt = $params['rank3_ozz'];
          }
          // 馬連ボーナスを設定する
          if ( $vote_info['mark1'] == $params['rank1_umaban']
            || $vote_info['mark1'] == $params['rank2_umaban']){
            /* ◎が1着または2着 */
            if ( $vote_info['mark2'] == $params['rank1_umaban']
              || $vote_info['mark2'] == $params['rank2_umaban']){
              /* かつ、〇も1着または2着 */
              $v_bonus2 = 100;
            }
          }
        }
        /* ▲判定 */
        if (   $vote_info['mark3'] == $params['rank1_umaban']
            || $vote_info['mark3'] == $params['rank2_umaban']
            || $vote_info['mark3'] == $params['rank3_umaban']
            ){
          /* 馬券内ならまず▲ポイントを設定 */
          if ($vote_info['mark3'] == $params['rank1_umaban']){
            /* 1着ならポイントを設定 */
            $v_mark3_pt = $params['rank1_ozz'];
          }
          if ($vote_info['mark3'] == $params['rank2_umaban']){
            /* 2着ならポイント */
            $v_mark3_pt = $params['rank2_ozz'];
          }
          if ($vote_info['mark3'] == $params['rank3_umaban']){
            /* 3着ならポイントを設定 */
            $v_mark3_pt = $params['rank3_ozz'];
          }
          // 3複ボーナスは後で設定する
          if ( $vote_info['mark1'] == $params['rank1_umaban']
            || $vote_info['mark1'] == $params['rank2_umaban']
            || $vote_info['mark1'] == $params['rank3_umaban']){
            /* ◎が1着または2着または3着 */
            if ( $vote_info['mark2'] == $params['rank1_umaban']
              || $vote_info['mark2'] == $params['rank2_umaban']
              || $vote_info['mark2'] == $params['rank3_umaban']){
              /* かつ、〇も1着または2着または3着 */
              if ( $vote_info['mark3'] == $params['rank1_umaban']
                || $vote_info['mark3'] == $params['rank2_umaban']
                || $vote_info['mark3'] == $params['rank3_umaban']){
                /* かつ▲も1着または2着または3着 */
                $v_bonus3 = 300;
              }
            }
          }

        }
        /* ☆判定 */
        if (   $vote_info['mark4'] == $params['rank1_umaban']
            || $vote_info['mark4'] == $params['rank2_umaban']
            || $vote_info['mark4'] == $params['rank3_umaban']
            ){
          /* 馬券内ならまず☆ポイントを設定 */
          if ($vote_info['mark4'] == $params['rank1_umaban']){
            /* 1着ならポイントを設定 */
            $v_mark4_pt = $params['rank1_ozz'];
          }
          if ($vote_info['mark4'] == $params['rank2_umaban']){
            /* 2着ならポイント */
            $v_mark4_pt = $params['rank2_ozz'];
          }
          if ($vote_info['mark4'] == $params['rank3_umaban']){
            /* 3着ならポイントを設定 */
            $v_mark4_pt = $params['rank3_ozz'];
          }
        }
        /* 穴判定 */
        if ($is_dark_horse_enable){
          // 穴馬投票が有効な場合のみ行う
          if (   $vote_info['mark5'] == $params['rank1_umaban']
          || $vote_info['mark5'] == $params['rank2_umaban']
          || $vote_info['mark5'] == $params['rank3_umaban']
          ){
            /* 馬券内ならまず穴ポイントを設定 */
            if ($vote_info['mark5'] == $params['rank1_umaban']){
              /* 1着ならポイントを設定 */
              $v_mark5_pt = $params['rank1_ozz'];
            }
            if ($vote_info['mark5'] == $params['rank2_umaban']){
              /* 2着ならポイント */
              $v_mark5_pt = $params['rank2_ozz'];
            }
            if ($vote_info['mark5'] == $params['rank3_umaban']){
              /* 3着ならポイントを設定 */
              $v_mark5_pt = $params['rank3_ozz'];
            }
          }
        }
        else{
          $v_mark5_pt = 'NULL';
        }
        /* 消判定 */
        if (   $vote_info['mark6'] != $params['rank1_umaban']
            && $vote_info['mark6'] != $params['rank2_umaban']
            && $vote_info['mark6'] != $params['rank3_umaban']
            ){
          /* 穴が馬券外なら消ポイントを設定 */
          for($di=1; $di<=8; $di++){
            if ( array_key_exists('d_rank'.$di.'_umban', $params)
              && array_key_exists('d_pt'.$di, $params)
              && $params['d_pt'.$di]>0){
              if ($vote_info['mark6'] == $params['d_rank'.$di.'_umban']){
                /* 人気馬と判定 */
                $v_mark6_pt = $params['d_pt'.$di];
                break;
              }
            }
          }
        }
        /* ポイント、払い戻しを設定する */
        $sql  = "UPDATE %s SET pay1 = %d";
        $sql .= ",pay2 = %d";
        $sql .= ",mark1_pt = %s";
        $sql .= ",mark2_pt = %s";
        $sql .= ",mark3_pt = %s";
        $sql .= ",mark4_pt = %s";
        $sql .= ",mark5_pt = %s";
        $sql .= ",mark6_pt = %s";
        $sql .= ",bonus1 = %s";
        $sql .= ",bonus2 = %s";
        $sql .= ",bonus3 = %s";
        $sql .= " WHERE vote_id = %s";
        $sql .= " AND user_cd = '%s';";
        $sql .= " commit;";
        $sql = sprintf($sql, TBL_USER_VOTE
                , $v_pay1, $v_pay2, $v_mark1_pt, $v_mark2_pt, $v_mark3_pt, $v_mark4_pt, $v_mark5_pt, $v_mark6_pt
                , $v_bonus1, $v_bonus2, $v_bonus3
                , $vote_info['vote_id'], $vote_info['user_cd']);
        $ret = ExecuteSelect($db, $sql, $update_result);
        if ($ret == false){
          throw new Exception("Failed to sql. sql:".$sql, BOC_DB_SQL_ERROR);
        }
      }
    }
        
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }
  return $result;
}

/**
 * レース結果を取得する
 * @param {in}  params  : パラメータ
 *                        - race_cd : レースCD
 * @return エラー情報
 *          - err_cd      : エラーCD
 *          - err_msg     : エラーMSG
 *          - race_result : レース結果[配列](tbl_m_race_resultの情報)
 *          - d_horses    : 消し馬情報[配列](tbl_race_del_horseの情報)
 */
function boc_get_race_result($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'race_result'      => null
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    /* レース結果を取得する */
    $sql = sprintf("SELECT * FROM %s WHERE race_cd = '%s' order by race_rank", TBL_M_RACE_RESULT, $params['race_cd']);
    $sql_result = GetSqlResults($db, $sql);
    if (count($sql_result)>0){
      $result['race_result'] = $sql_result;  
    }

    // 消し馬情報も取得
    $sql = "SELECT * FROM %s WHERE race_cd= '%s' order by d_rank";
    $sql = sprintf($sql, TBL_RACE_DEL_HORSE, $params['race_cd']);
    $sql_result = GetSqlResults($db, $sql);
    if (count($sql_result)>0){
      $result['d_horses'] = $sql_result;  
    }

  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }
  return $result;
}

/**
 * 各種ランキングリストを取得する。
 * @param {in}  params  : パラメータ
 *                        - ranking_type  : ランキング種別
 *                                          - BOC_POINT_RANKING   : ポイントランキング
 *                                          - BOC_HONMEI_RANKING  : ◎的中率ランキング
 *                                          - BOC_TANSHO_RANKING  : 単勝回収率ランキング
 *                                          - BOC_FUKUSHO_RANKING : 複勝回収率ランキング
 *                                          - BOC_VOTE_RANKING    : 投票回数ランキング
 *                        - sum_type      : 集計期間
 *                                          - BOC_RANKING_MONTH       : 月間
 *                                          - BOC_RANKING_YEAR        : 年間
 *                                          - BOC_RANKING_FIRST_HALF  : 上半期
 *                                          - BOC_RANKING_LAST_HALF   : 下半期
 *                        - user_cd       : ユーザーCD(オプション)
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
 *                              - mark1_hit   : ◎的中数
 *                              - mark1_rate  : ◎的中率
 *                              - mark2_hit   : 〇的中数
 *                              - mark2_rate  : 〇的中率
 *                              - mark3_hit   : ▲的中数
 *                              - mark3_rate  : ▲的中率
 *                              - mark4_hit   : ☆的中数
 *                              - mark4_rate  : ☆的中率
 *                              - mark5_hit   : 穴的中数
 *                              - mark5_rate  : 穴的中率
 *                              - mark6_hit   : 消的中数
 *                              - mark6_rate  : 消的中率
 *                              - pay1_rate   : 単勝回収率
 *                              - pay2_rate   : 複勝回収率
 */
function boc_get_ranking_list($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'ranking_list'   => null
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // 月間、年間、上半期、下半期の規定回数を算出
    // 月間は規定50%,年間、上半期、下半期は規定60%
    $tgt_month = 1;
    $limit_month_v_count = 1;
    $limit_year_v_count = 1;
    $limit_first_half_v_count = 1;
    $limit_last_half_v_count = 1;
    /* 集計月 */
    $sql  = "SELECT MAX(race_month) as tgt_month FROM %s";
    $sql .= " WHERE race_type IN (1,3,5);";
    $sql = sprintf($sql, V_USER_VOTE);
    $tgt_month_result = GetSqlResults($db, $sql);
    if (count($tgt_month_result) > 0){
      $tgt_month = $tgt_month_result[0]['tgt_month'];
    }

    if (!array_key_exists('user_cd', $params)){
      /* 月間 */
      $sql  = "SELECT count(*) as r_count FROM %s";
      $sql .= " WHERE race_type IN (1,3,5)";
      $sql .= " AND race_month = %d";
      $sql = sprintf($sql, TBL_M_RACE, $tgt_month);
      $sql_result = GetSqlResults($db, $sql);
      if (count($sql_result) > 0){
        $limit_month_v_count = $sql_result[0]['r_count'];
        $limit_month_v_count = round($limit_month_v_count / 2);
      }

      /* 年間 */
      if ($params['ranking_type'] != BOC_VOTE_RANKING){
        $sql  = "SELECT count(*) as r_count FROM %s";
        $sql .= " WHERE race_type IN (1,3,5);";
        $sql = sprintf($sql, TBL_M_RACE, $tgt_month);
        $sql_result = GetSqlResults($db, $sql);
        if (count($sql_result) > 0){
          $limit_year_v_count = $sql_result[0]['r_count'];
          $limit_year_v_count = round($limit_year_v_count * 0.6);
        }
      }

      /* 上半期 */
      $sql  = "SELECT count(*) as r_count FROM %s";
      $sql .= " WHERE race_type IN (1,3,5)";
      $sql .= " AND race_month IN (1,2,3,4,5,6)";
      $sql = sprintf($sql, TBL_M_RACE, $tgt_month);
      $sql_result = GetSqlResults($db, $sql);
      if (count($sql_result) > 0){
        $limit_first_half_v_count = $sql_result[0]['r_count'];
        $limit_first_half_v_count = round($limit_first_half_v_count * 0.6);
      }

      /* 下半期 */
      $sql  = "SELECT count(*) as r_count FROM %s";
      $sql .= " WHERE race_type IN (1,3,5)";
      $sql .= " AND race_month IN (7,8,9,10,11,12)";
      $sql = sprintf($sql, TBL_M_RACE, $tgt_month);
      $sql_result = GetSqlResults($db, $sql);
      if (count($sql_result) > 0){
        $limit_last_half_v_count = $sql_result[0]['r_count'];
        $limit_last_half_v_count = round($limit_last_half_v_count * 0.6);
      }
    }

    // ベースとなるSQLを組み立て
    $sql  = "SELECT v.user_cd, v.user_name, count(*) AS v_count,";
    $sql .= " CASE WHEN sum(v.mark1_pt + v.mark2_pt + v.mark3_pt + v.mark4_pt + v.mark5_pt + v.mark6_pt + v.bonus1 + v.bonus2 + v.bonus3) is null THEN 0";
    $sql .= "      ELSE sum(v.mark1_pt + v.mark2_pt + v.mark3_pt + v.mark4_pt + v.mark5_pt + v.mark6_pt + v.bonus1 + v.bonus2 + v.bonus3) END AS pt,";
    $sql .= " sum(v.hit_mark1) as mark1_hit,"; 
    $sql .= " sum(v.hit_mark1) * 100 / count(*) AS mark1_rate,"; 
    $sql .= " sum(v.hit_mark2) as mark2_hit,"; 
    $sql .= " sum(v.hit_mark2) * 100 / count(*) AS mark2_rate,"; 
    $sql .= " sum(v.hit_mark3) as mark3_hit,"; 
    $sql .= " sum(v.hit_mark3) * 100 / count(*) AS mark3_rate,"; 
    $sql .= " sum(v.hit_mark4) as mark4_hit,"; 
    $sql .= " sum(v.hit_mark4) * 100 / count(*) AS mark4_rate,"; 
    $sql .= " sum(v.hit_mark5) as mark5_hit,"; 
    $sql .= " sum(v.hit_mark5) * 100 / count(*) AS mark5_rate,"; 
    $sql .= " sum(v.hit_mark6) as mark6_hit,"; 
    $sql .= " sum(v.hit_mark6) * 100 / count(*) AS mark6_rate,"; 
    $sql .= " sum(v.pay1) * 100 / (count(*) * 100) AS pay1_rate,"; 
    $sql .= " sum(v.pay2) * 100 / (count(*) * 100) AS pay2_rate";
    $sql .= " FROM boc.v_user_vote_result v";
    $sql .= " WHERE v.race_type IN (1,3,5)";
    /* 集計期間によって条件を変更 */
    if ($params['sum_type'] == BOC_RANKING_MONTH){
      $sql .= " AND v.race_month = " . $tgt_month;
      $result['month'] = $tgt_month;
    }
    elseif($params['sum_type'] == BOC_RANKING_FIRST_HALF){
      $sql .= " AND v.race_month IN (1,2,3,4,5,6)";
    }
    elseif($params['sum_type'] == BOC_RANKING_LAST_HALF){
      $sql .= " AND v.race_month IN (7,8,9,10,11,12)";
    }
    /* ユーザーCDが指定されている場合はユーザーCDで絞り込む */
    if (array_key_exists('user_cd', $params)){
      $sql .= sprintf(" AND v.user_cd = '%s'", $params['user_cd']);
    }
    $sql .= " GROUP BY v.user_cd, v.user_name";
    /* ランキング種別に応じてorder byを変更する */
    if ($params['ranking_type'] == BOC_POINT_RANKING){
      /* ポイントランキング */
      // $sql .= " ORDER BY sum(v.mark1_pt + v.mark2_pt + v.mark3_pt + v.mark4_pt + v.mark5_pt + v.bonus1 + v.bonus2 + v.bonus3) DESC;";
      $sql .= " ORDER BY pt DESC;";
    }
    elseif ($params['ranking_type'] == BOC_HONMEI_RANKING){
      /* ◎的中率 */
      $sql .= " ORDER BY mark1_rate DESC;";
    }
    elseif ($params['ranking_type'] == BOC_TANSHO_RANKING){
      /* ◎的中率 */
      $sql .= " ORDER BY pay1_rate DESC;";
    }
    elseif ($params['ranking_type'] == BOC_FUKUSHO_RANKING){
      /* ◎的中率 */
      $sql .= " ORDER BY pay2_rate DESC;";
    }
    else {
      /* 上記以外なら投票回数ランキングとみなす */
      $sql .= " ORDER BY v_count DESC;";
    }
    $sql_result = GetSqlResults($db, $sql);
    
    // 規定回数以上の物だけを返す
    $r_result = array();
    if ($sql_result){
      foreach($sql_result as $rec_info){
        if ($params['sum_type'] == BOC_RANKING_MONTH){
          if ($rec_info['v_count'] >= $limit_month_v_count){
            /* セキュリティ対策の為、クライアントにはユーザーCDは通知しない */
            $rank_info = [
              'user_name'   => $rec_info['user_name'],
              'v_count'     => $rec_info['v_count'],
              'pt'          => $rec_info['pt'],
              'mark1_hit'   => $rec_info['mark1_hit'],
              'mark1_rate'  => $rec_info['mark1_rate'],
              'mark2_hit'   => $rec_info['mark2_hit'],
              'mark2_rate'  => $rec_info['mark2_rate'],
              'mark3_hit'   => $rec_info['mark3_hit'],
              'mark3_rate'  => $rec_info['mark3_rate'],
              'mark4_hit'   => $rec_info['mark4_hit'],
              'mark4_rate'  => $rec_info['mark4_rate'],
              'mark5_hit'   => $rec_info['mark5_hit'],
              'mark5_rate'  => $rec_info['mark5_rate'],
              'mark6_hit'   => $rec_info['mark6_hit'],
              'mark6_rate'  => $rec_info['mark6_rate'],
              'pay1_rate'   => $rec_info['pay1_rate'],
              'pay2_rate'   => $rec_info['pay2_rate']
            ];
            if (array_key_exists('mode', $params) && $params['mode'] == 'inside'){
              /* 内部モードならuser_cdを含める */
              $rank_info['user_cd'] = $rec_info['user_cd'];
            }
            array_push($r_result, $rank_info);
          }
        }
        elseif ($params['sum_type'] == BOC_RANKING_FIRST_HALF){
          if ($rec_info['v_count'] >= $limit_first_half_v_count){
            /* セキュリティ対策の為、クライアントにはユーザーCDは通知しない */
            $rank_info = [
              'user_name'   => $rec_info['user_name'],
              'v_count'     => $rec_info['v_count'],
              'pt'          => $rec_info['pt'],
              'mark1_hit'   => $rec_info['mark1_hit'],
              'mark1_rate'  => $rec_info['mark1_rate'],
              'mark2_hit'   => $rec_info['mark2_hit'],
              'mark2_rate'  => $rec_info['mark2_rate'],
              'mark3_hit'   => $rec_info['mark3_hit'],
              'mark3_rate'  => $rec_info['mark3_rate'],
              'mark4_hit'   => $rec_info['mark4_hit'],
              'mark4_rate'  => $rec_info['mark4_rate'],
              'mark5_hit'   => $rec_info['mark5_hit'],
              'mark5_rate'  => $rec_info['mark5_rate'],
              'mark6_hit'   => $rec_info['mark6_hit'],
              'mark6_rate'  => $rec_info['mark6_rate'],
              'pay1_rate'   => $rec_info['pay1_rate'],
              'pay2_rate'   => $rec_info['pay2_rate']
            ];
            if (array_key_exists('mode', $params) && $params['mode'] == 'inside'){
              /* 内部モードならuser_cdを含める */
              $rank_info['user_cd'] = $rec_info['user_cd'];
            }
            array_push($r_result, $rank_info);
          }
        }
        elseif ($params['sum_type'] == BOC_RANKING_LAST_HALF){
          if ($rec_info['v_count'] >= $limit_last_half_v_count){
            /* セキュリティ対策の為、クライアントにはユーザーCDは通知しない */
            $rank_info = [
              'user_name'   => $rec_info['user_name'],
              'v_count'     => $rec_info['v_count'],
              'pt'          => $rec_info['pt'],
              'mark1_hit'   => $rec_info['mark1_hit'],
              'mark1_rate'  => $rec_info['mark1_rate'],
              'mark2_hit'   => $rec_info['mark2_hit'],
              'mark2_rate'  => $rec_info['mark2_rate'],
              'mark3_hit'   => $rec_info['mark3_hit'],
              'mark3_rate'  => $rec_info['mark3_rate'],
              'mark4_hit'   => $rec_info['mark4_hit'],
              'mark4_rate'  => $rec_info['mark4_rate'],
              'mark5_hit'   => $rec_info['mark5_hit'],
              'mark5_rate'  => $rec_info['mark5_rate'],
              'mark6_hit'   => $rec_info['mark6_hit'],
              'mark6_rate'  => $rec_info['mark6_rate'],
              'pay1_rate'   => $rec_info['pay1_rate'],
              'pay2_rate'   => $rec_info['pay2_rate']
            ];
            if (array_key_exists('mode', $params) && $params['mode'] == 'inside'){
              /* 内部モードならuser_cdを含める */
              $rank_info['user_cd'] = $rec_info['user_cd'];
            }
            array_push($r_result, $rank_info);
          }
        }
        elseif ($params['sum_type'] == BOC_RANKING_YEAR){
          if ($rec_info['v_count'] >= $limit_year_v_count){
            /* セキュリティ対策の為、クライアントにはユーザーCDは通知しない */
            $rank_info = [
              'user_name'   => $rec_info['user_name'],
              'v_count'     => $rec_info['v_count'],
              'pt'          => $rec_info['pt'],
              'mark1_hit'   => $rec_info['mark1_hit'],
              'mark1_rate'  => $rec_info['mark1_rate'],
              'mark2_hit'   => $rec_info['mark2_hit'],
              'mark2_rate'  => $rec_info['mark2_rate'],
              'mark3_hit'   => $rec_info['mark3_hit'],
              'mark3_rate'  => $rec_info['mark3_rate'],
              'mark4_hit'   => $rec_info['mark4_hit'],
              'mark4_rate'  => $rec_info['mark4_rate'],
              'mark5_hit'   => $rec_info['mark5_hit'],
              'mark5_rate'  => $rec_info['mark5_rate'],
              'mark6_hit'   => $rec_info['mark6_hit'],
              'mark6_rate'  => $rec_info['mark6_rate'],
              'pay1_rate'   => $rec_info['pay1_rate'],
              'pay2_rate'   => $rec_info['pay2_rate']
            ];
            if (array_key_exists('mode', $params) && $params['mode'] == 'inside'){
              /* 内部モードならuser_cdを含める */
              $rank_info['user_cd'] = $rec_info['user_cd'];
            }
            array_push($r_result, $rank_info);
          }
        }
        else{
          /* セキュリティ対策の為、クライアントにはユーザーCDは通知しない */
          $rank_info = [
            'user_name'   => $rec_info['user_name'],
            'v_count'     => $rec_info['v_count'],
            'pt'          => $rec_info['pt'],
            'mark1_hit'   => $rec_info['mark1_hit'],
            'mark1_rate'  => $rec_info['mark1_rate'],
            'mark2_hit'   => $rec_info['mark2_hit'],
            'mark2_rate'  => $rec_info['mark2_rate'],
            'mark3_hit'   => $rec_info['mark3_hit'],
            'mark3_rate'  => $rec_info['mark3_rate'],
            'mark4_hit'   => $rec_info['mark4_hit'],
            'mark4_rate'  => $rec_info['mark4_rate'],
            'mark5_hit'   => $rec_info['mark5_hit'],
            'mark5_rate'  => $rec_info['mark5_rate'],
            'mark6_hit'   => $rec_info['mark6_hit'],
            'mark6_rate'  => $rec_info['mark6_rate'],
            'pay1_rate'   => $rec_info['pay1_rate'],
            'pay2_rate'   => $rec_info['pay2_rate']
          ];
          if (array_key_exists('mode', $params) && $params['mode'] == 'inside'){
            /* 内部モードならuser_cdを含める */
            $rank_info['user_cd'] = $rec_info['user_cd'];
          }
        array_push($r_result, $rank_info);
        }
      }
    }
    $result['ranking_list'] = $r_result;
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }
  return $result;
}

/**
 * 投票履歴も含めたユーザー情報リストを取得する
 * 取得するリストは投票回数が多い順にソートされている。
 * @param {in}  params  : パラメータ(オプション)
 *                        - user_cd     : ユーザーCD
 *                        - ope_user_cd : 操作ユーザーCD
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
function boc_get_user_info_list($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'user_list'      => null
  );
  
  try{
    // 権限チェック
    if (!array_key_exists('user_cd', $params)){
      /* ユーザーCDが未設定の場合、取得できるのは操作ユーザーCDが権限を持っている場合のみ */
      if (!array_key_exists('ope_user_cd', $params)){
        /* 操作ユーザーCDが無ければエラー */
        throw new Exception("Invalid user type.", BOC_INVALID_USER_TYPE);
      }
      $svc_result = boc_check_use_function(array(
        'func_name'     => BOC_USE_SCORE_MANAGE,
        'ope_user_cd'   => $params['ope_user_cd']
      ));
      if ($svc_result[BOC_RESULT_CD] != BOC_NO_ERROR){
        throw new Exception("Invalid user type.", BOC_INVALID_USER_TYPE);
      }
    }

    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // まずはベースとなるユーザーリストを取得
    $req_param = array(
      'ranking_type'  => BOC_VOTE_RANKING,
      'sum_type'      => BOC_RANKING_YEAR,
      'mode'          => 'inside'
    );
    if (array_key_exists('user_cd', $params)){
      $req_param['user_cd'] = $params['user_cd'];
    }
    $service_result = boc_get_ranking_list($req_param);
    if ($service_result[BOC_RESULT_CD] != BOC_NO_ERROR){
      return $service_result;
    }
    // リスト取得に成功したらユーザー単位でデータを設定
    $svc_user_list = $service_result['ranking_list'];
    $r_user_list = array();
    foreach($svc_user_list as $svc_user_info){
      // 基本情報を設
      $service_result = boc_get_public_user_info(
        array('user_cd' => $svc_user_info['user_cd'])
      );
      if ($service_result[BOC_RESULT_CD] != BOC_NO_ERROR){
        return $service_result;
      }
      $user_info = $service_result['user_info'];
      // ランキング称号と称号画像を設定
      if ($svc_user_info['mark1_rate'] >= BOC_TITLE_WG){
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_WG]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_WG]['img'];
      }
      elseif ($svc_user_info['mark1_rate'] >= BOC_TITLE_G1){
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_G1]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_G1]['img'];
      }
      elseif ($svc_user_info['mark1_rate'] >= BOC_TITLE_G2){
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_G2]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_G2]['img'];
      }
      elseif ($svc_user_info['mark1_rate'] >= BOC_TITLE_G3){
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_G3]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_G3]['img'];
      }
      elseif ($svc_user_info['mark1_rate'] >= BOC_TITLE_OL){
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_OL]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_OL]['img'];
      }
      elseif ($svc_user_info['mark1_rate'] >= BOC_TITLE_W3){
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_W3]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_W3]['img'];
      }
      elseif ($svc_user_info['mark1_rate'] >= BOC_TITLE_W2){
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_W2]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_W2]['img'];
      }
      elseif ($svc_user_info['mark1_rate'] >= BOC_TITLE_W1){
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_W1]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_W1]['img'];
      }
      elseif ($svc_user_info['mark1_rate'] >= BOC_TITLE_UW){
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_UW]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_UW]['img'];
      }
      else{
        $user_info['ranking_rank'] = BOC_TITLE_INFO[BOC_TITLE_NR]['name'];
        $user_info['rabking_img'] = BOC_TITLE_INFO[BOC_TITLE_NR]['img'];
      }
      // ユーザーの投稿履歴を取得する
      $sql = "SELECT * FROM %s WHERE user_cd = '%s' ORDER BY race_time desc;";
      $sql = sprintf($sql, V_USER_VOTE, $user_info['user_cd']);
      $user_info['vote_history'] = GetSqlResults( $db, $sql );
      // ユーザーの的中率を設定
      /* 月間成績 */
      $service_result = boc_get_ranking_list(
        array(
          'ranking_type'  => BOC_POINT_RANKING,
          'sum_type'      => BOC_RANKING_MONTH,
          'user_cd'       => $user_info['user_cd']
        )
      );
      if ($service_result[BOC_RESULT_CD] == BOC_NO_ERROR){
        if (count($service_result['ranking_list'])>0){
          $user_info['vote_overview']['month_ranking'] = $service_result['ranking_list'][0];
        }
        else{
          $user_info['vote_overview']['month_ranking'] = null;
        }
      }
      /* 年間成績 */
      $service_result = boc_get_ranking_list(
        array(
          'ranking_type'  => BOC_POINT_RANKING,
          'sum_type'      => BOC_RANKING_YEAR,
          'user_cd'       => $user_info['user_cd']
        )
      );
      if ($service_result[BOC_RESULT_CD] == BOC_NO_ERROR){
        if (count($service_result['ranking_list'])>0){
          $user_info['vote_overview']['year_ranking'] = $service_result['ranking_list'][0];
        }
        else{
          $user_info['vote_overview']['year_ranking'] = null;
        }
      }
      /* 上半期成績 */
      $service_result = boc_get_ranking_list(
        array(
          'ranking_type'  => BOC_POINT_RANKING,
          'sum_type'      => BOC_RANKING_FIRST_HALF,
          'user_cd'       => $user_info['user_cd']
        )
      );
      if ($service_result[BOC_RESULT_CD] == BOC_NO_ERROR){
        if (count($service_result['ranking_list'])>0){
          $user_info['vote_overview']['first_half_ranking'] = $service_result['ranking_list'][0];
        }
        else{
          $user_info['vote_overview']['first_half_ranking'] = null;
        }
      }
      /* 下半期成績 */
      $service_result = boc_get_ranking_list(
        array(
          'ranking_type'  => BOC_POINT_RANKING,
          'sum_type'      => BOC_RANKING_LAST_HALF,
          'user_cd'       => $user_info['user_cd']
        )
      );
      if ($service_result[BOC_RESULT_CD] == BOC_NO_ERROR){
        if (count($service_result['ranking_list'])>0){
          $user_info['vote_overview']['last_half_ranking'] = $service_result['ranking_list'][0];
        }
        else{
          $user_info['vote_overview']['last_half_ranking'] = null;
        }
      }
      // ユーザー情報を返却リストに追加
      array_push($r_user_list,$user_info);
    }
    $result['user_list'] = $r_user_list;
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }
  return $result;
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
function boc_check_use_function($params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => "",
    'user_list'      => null
  );
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    // ユーザー種別を取得する
    $sql = "SELECT user_type FROM %s WHERE user_cd = '%s'";
    $sql = sprintf($sql, TBL_USER, $params['ope_user_cd']);
    $sql_result = GetSqlResults( $db, $sql );
    if (count($sql_result) == 0){
      $user_type = 'guest';
    }
    else{
      $user_type = $sql_result[0]['user_type'];
    }
    $func_name = $params['func_name'];
    // 権限を判定
    if ($func_name == BOC_USE_VOTE){
      if ($user_type == 'guest'){
        throw new Exception("invalid user type.", BOC_INVALID_USER_TYPE);
      } 
    }
    elseif ($func_name == BOC_USE_RACE_MANAGE){
      if ( $user_type == 'guest'
        || $user_type == 'user'){
        throw new Exception("invalid user type.", BOC_INVALID_USER_TYPE);
      } 
    }
    elseif ($func_name == BOC_USE_RACE_REGIST){
      if ( $user_type == 'guest'
        || $user_type == 'user'){
        throw new Exception("invalid user type.", BOC_INVALID_USER_TYPE);
      }
      // ユーザー種別がsuperuser以外なら編集できるのは当日レースのみ
      // 既存レコードが存在するかをチェック
      $sql  = "SELECT * FROM %s";
      $sql .= " WHERE race_cd = '%s'";
      $sql = sprintf($sql, TBL_M_RACE, $params['param1']);
      $sql_result = GetSqlResults( $db, $sql );
      if (count($sql_result)>0){
        // 既存レコードの修正はadminかスーパーユーザーのみ可能
        $sql  = "SELECT * FROM %s";
        $sql .= " WHERE race_cd = '%s'";
        $sql .= " AND race_date >= CURRENT_DATE";
        $sql = sprintf($sql, TBL_M_RACE, $params['param1']);
        $sql_result = GetSqlResults( $db, $sql );
        if ($user_type == 'staff' && count($sql_result) == 0){
          throw new Exception("Staff can manage only today race.", BOC_INVALID_USER_TYPE);
        }
      }
    }
    elseif ($func_name == BOC_USE_RACE_RESULT_REGIST){
      if ( $user_type == 'guest'
        || $user_type == 'user'){
        throw new Exception("invalid user type.", BOC_INVALID_USER_TYPE);
      }
      // ユーザー種別がsuperuser以外なら編集できるのは当日レースのみ
      $sql  = "SELECT * FROM %s";
      $sql .= " WHERE race_cd = '%s'";
      $sql .= " AND race_date >= CURRENT_DATE";
      $sql = sprintf($sql, TBL_M_RACE, $params['param1']);
      $sql_result = GetSqlResults( $db, $sql );
      if ($user_type == 'staff' && count($sql_result) == 0){
        throw new Exception("Staff can manage only today race.", BOC_INVALID_USER_TYPE);
      }
    }
    elseif ($func_name == BOC_USE_SCORE_MANAGE){
      if ( $user_type == 'guest'
        || $user_type == 'user'
        || $user_type == 'staff'){
        throw new Exception("invalid user type.", BOC_INVALID_USER_TYPE);
      }
    }    
    elseif ($func_name == BOC_USE_USER_MANAGE){
      if ( $user_type != 'superuser'){
        throw new Exception("invalid user type.", BOC_INVALID_USER_TYPE);
      }
    }    
    elseif ($func_name == BOC_USE_UPDATE_USER_INFO){
      if ($user_type == 'guest'){
        throw new Exception("invalid user type.", BOC_INVALID_USER_TYPE);
      }
      if ( $user_type != 'superuser'
        && $ope_user_cd != $params['param1']){
        /* スーパーユーザー以外は自分のものしか編集できない */
        throw new Exception("invalid user type.", BOC_INVALID_USER_TYPE);
      }
    }
    elseif ($func_name == BOC_USE_INPUT_USER_SCORE){
      if ( $user_type != 'superuser'){
        throw new Exception("invalid user type.", BOC_INVALID_USER_TYPE);
      }
    }    

  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
    $result[BOC_RESULT_CD] = $ex->getCode();
    $result[BOC_RESULT_MSG] = $ex->getMessage();
  }
  return $result;
}
  

/////////////////////////////////////////////////////////////
// これ以降、Private関数                                                                                 
//

/**
 * メール送信を行う。
 * @param {in}   $mailInfo メール情報
 *               - dest        : 送信先
 *               - sender      : 送信元
 *               - subject     : 件名
 *               - contents    : メール本文
 * @return エラー情報
 *           - err_code                エラーコード
 *           - err_msg                 エラーメッセージ
 */
function boc_SendMail($mailInfo)
{
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => ""
  );
  if (   empty($mailInfo['dest'])
      || empty($mailInfo['sender'])
      || empty($mailInfo['subject'])
      || empty($mailInfo['contents'])
      )
  {
    $result[BOC_RESULT_CD] = BOC_INVALID_PAPAMETER;
    $result[BOC_RESULT_MSG] = 'Invalid parameter.';
  }
  else{
    // メール送信を行う
    /* 文字コード設定 */
    mb_language("Japanese");
    mb_internal_encoding("UTF-8");
    /* Fromヘッダーを設定 */
    $headers = "From: " . $mailInfo['sender'];

    /* メール送信 */
    if (mb_send_mail($mailInfo['dest'], $mailInfo['subject'], $mailInfo['contents'], $headers)){
      /* メール送信成功 */
      info(sprintf("Mail send to %s", $mailInfo['dest']));
    }
    else{
      /* メール送信失敗 */
      $result[BOC_RESULT_CD] = BOC_INVALID_PAPAMETER;
      $result[BOC_RESULT_MSG] = 'Invalid parameter.';
    }
  }

  return $result;
}

/**
 * ユーザー権限をチェックする
 * @param {in}  chk_user_cd   : チェックするユーザーCD
 * @param {in}  require_type  : 要求するユーザー種別:
 *                                staff     : 運営スタッフ
 *                                admin     : 管理者
 *                                superuser : スーパーユーザー
 */
function checkUserType($chk_user_cd, $require_type){
  $result = false;
  
  try{
    // DBに接続する
    $db = getDBConnecton(DB_CONNECTION_STR);
    if (!$db){
      throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
    }

    /* ユーザーCDが未設定ならエラー */
    if(empty($chk_user_cd)){
      return false;
    }

    /* ユーザー種別を取得する */
    $sql = "SELECT user_type FROM %s WHERE user_cd = '%s'";
    $sql = sprintf($sql, TBL_USER, $chk_user_cd);
    $sql_result = GetSqlResults( $db, $sql );
    if (count($sql_result)==0){
      /* ユーザーが存在しなければ権限なし */
      return false;
    }

    // 権限によって判定
    $user_type = $sql_result[0]['user_type'];
    if ($require_type == 'superuser'){
      if ($user_type != 'superuser') return false;
    }
    else if ($require_type == 'admin'){
      if ( $user_type != 'superuser'
        && $user_type != 'admin') return false;
    }
    else if ($require_type == 'staff'){
      if ( $user_type != 'superuser'
        && $user_type != 'admin'
        && $user_type != 'staff') return false;
    }

    // ここまできたらチェックOK
    $result = true;
  }
  catch(Exception $ex){
    error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
  }
  return $result;
}


 
?>
