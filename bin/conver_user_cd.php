<?php
/******************************************
 * user_cdハッシュ化処理
 */
require_once(dirname(__FILE__) . '/common/db.php');		          // DBをインポート
require_once(dirname(__FILE__) . '/common/logger.php');		      // loggerをインポート

require_once(dirname(__FILE__) . '/service_config.php');        // サービス設定をインポート

try{
  echo ">>>> Start user_cd convert.\n";
  // DBに接続する
  $db = getDBConnecton(DB_CONNECTION_STR);
  if (!$db){
    throw new Exception('DB接続に失敗', BOC_DB_CONNECT_ERROR);
  }

  /* ユーザー一覧を読み込む */
  $sql = "SELECT * FROM boc.tbl_user;";
  $user_result = GetSqlResults( $db, $sql );
  foreach($user_result as $user_info){
    $tgt_user_cd = $user_info['user_cd'];
    echo "$tgt_user_cd is converting......";
    /* 新しいuser_cdを生成 */
    $new_user_cd = substr(bin2hex(random_bytes(12)), 0, 12);

    /* tbl_user_voteをコンバート */
    $sql = "UPDATE boc.tbl_user_vote SET user_cd = '%s' WHERE user_cd = '%s';";
    /* tbl_userをコンバート */
    $sql .= "UPDATE boc.tbl_user SET user_cd = '%s' WHERE user_cd = '%s';";
    $sql .= "commit;";
    $sql = sprintf($sql, $new_user_cd, $tgt_user_cd, $new_user_cd, $tgt_user_cd);
    $update_result = array();
    $ret = ExecuteSelect( $db, $sql, $update_result );
    if ($ret == false){
      throw new Exception("Failed to convert $tgt_user_cd to $new_user_cd");
    }
    echo "to $new_user_cd converted\n";
  }
  echo "<<<< End user_cd convert.\n";
}
catch(Exception $ex){
  error( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
}

?>
