<?php
/**
 * AOBサービスコントローラー
 */
// セッション開始
session_start();
date_default_timezone_set('Asia/Tokyo');

require_once(dirname(__FILE__) . '/common/logger.php');		        // loggerをインポート

// 各サービスをインポート
require_once(dirname(__FILE__) . '/boc_service.php');		        // loggerをインポート

/* メソッドの取得 */
$method = "";
if (array_key_exists('method', $_REQUEST)){
  $method = $_REQUEST['method'];
}

/* メソッドパラメータの取得 */
$req_params = $_REQUEST;
if (array_key_exists('method_param', $_REQUEST)){
  $dec_string = base64_decode($_REQUEST['method_param']);
  if ($dec_string != FALSE){
    $req_params = json_decode($dec_string, true);
  }
}
if ($method != 'washapp_upload_image'){
  info( sprintf("main req_pram: %s", json_encode($req_params)) );
}

main($method, $req_params);

/**
 * メイン処理
 * @param {in}  $method     : メソッド名 
 * @param {in}  $req_params : メソッドパラメータ
 * @return サービス結果[JSON形式]
 */
function main($method, $req_params){
  $result = array(
    BOC_RESULT_CD    => 0,
    BOC_RESULT_MSG   => ""
  );

  try{
    /* BOCサービスAPI */
    if ($method == 'boc_regist_user'){
      $result = boc_regist_user($req_params);
    }
    elseif ($method == 'boc_send_user_regist_confirm'){
      $result = boc_send_user_regist_confirm($req_params);
    }
    elseif ($method == 'boc_reminder'){
      $result = boc_reminder($req_params);
    }
    elseif ($method == 'boc_get_user_info'){
      $result = boc_get_user_info($req_params);
    }
    elseif ($method == 'boc_get_public_user_info'){
      $result = boc_get_public_user_info($req_params);
    }
    elseif ($method == 'boc_get_user_list'){
      $result = boc_get_user_list($req_params);
    }
    elseif ($method == 'boc_delete_user'){
      $result = boc_delete_user($req_params);
    }
    elseif ($method == 'boc_regist_race'){
      $result = boc_regist_race($req_params);
    }
    elseif ($method == 'boc_delete_race'){
      $result = boc_delete_race($req_params);
    }
    elseif ($method == 'boc_get_race_list'){
      $result = boc_get_race_list($req_params);
    }
    elseif ($method == 'boc_get_race_info'){
      $result = boc_get_race_info($req_params);
    }
    elseif ($method == 'boc_login'){
      $result = boc_login($req_params);
    }
    elseif ($method == 'boc_get_vote_race'){
      $result = boc_get_vote_race($req_params);
    }
    elseif ($method == 'boc_vote'){
      $result = boc_vote($req_params);
    }
    elseif ($method == 'boc_get_vote'){
      $result = boc_get_vote($req_params);
    }
    elseif ($method == 'boc_regist_race_result'){
      $result = boc_regist_race_result($req_params);
    }
    elseif ($method == 'boc_get_race_result'){
      $result = boc_get_race_result($req_params);
    }
    elseif ($method == 'boc_get_ranking_list'){
      $result = boc_get_ranking_list($req_params);
    }
    elseif ($method == 'boc_get_user_info_list'){
      $result = boc_get_user_info_list($req_params);
    }
    elseif ($method == 'boc_check_use_function'){
      $result = boc_check_use_function($req_params);
    }
    else{
      error( sprintf("Invalid method. method:%s", $method) );
      throw new Exception("Invalid method.", BOC_SERVICE_ERROR);
    }
	} catch ( Exception $ex ) {
		warn( sprintf( "%s ： %d ： %s", __FUNCTION__, $ex->getCode(), $ex->getMessage() ) );
		$results[BOC_RESULT_CD] = $ex->getCode();
		$results[BOC_RESULT_MSG]  = $ex->getMessage();
	}

	/* レスポンスをJSON形式で返す */
  $response = json_encode( $result );
	//trace($response);
	header("HTTP/1.1 200 OK");
	header("Status: 200");
	header("Content-Type: application/json; charset=UTF-8");
	echo $response;

}
?>
