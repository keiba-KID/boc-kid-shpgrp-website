<?php
require_once(dirname(__FILE__) . '/logger.php');		          // loggerをインポート


/************************************************
 * DBアクセスライブラリ
 */

/********************************************************
 * PostgreSQLに接続してSelect実行結果を取得する
 * @param $db  [in] DBコネクション
 * @param $sql [in] SQL文字列
 * @return SQL結果配列。エラー発生時はfalseを返す。
 */
function GetSqlResults( $db, $sql )
{
  info("sql=" . $sql);
  $resp	= array();
  $result	= pg_query( $db, $sql );
  if ( !$result ) {
    error("sql=" . $sql);		// TODO
    error( sprintf( "%s ： %s", __FUNCTION__, pg_last_error() ));
    // pg_close($db);				// DB切断
    return false;				// TODO:type error
  }
  // クエリー結果を取得
  for ( $i = 0; $i < pg_num_rows($result); $i++ ) {
    $storeInfo = pg_fetch_array( $result, NULL, PGSQL_ASSOC );
    array_push( $resp, $storeInfo );
  }
  return $resp;
}

/********************************************************
 * PostgreSQLに接続してSelect実行結果を取得する
 * @param $db  [in] DBコネクション
 * @param $sql [in] SQL文字列
 * @return SQL結果配列。エラー発生時はfalseを返す。
 */
function ExecuteSelect( $db, $sql, &$result )
{
  info("sql=" . $sql);
  $ret	= true;
    $resp	= array();
    $result	= pg_query( $db, $sql );
    if ( !$result ) {
      error("sql=" . $sql);
      error( sprintf( "%s ： %s", __FUNCTION__, pg_last_error() ));
      //pg_close($db);
      $ret = false;
    } else {
      // クエリー結果を取得
      for ( $i = 0; $i < pg_num_rows($result); $i++ ) {
          $storeInfo = pg_fetch_array( $result, NULL, PGSQL_ASSOC );
          array_push( $resp, $storeInfo );
      }
      $result = $resp;
    }
    return $ret;
}

/**
 * IroxoriDBコネクションを取得する。
 * @param {in} $connStr : DB接続文字列
 */
function getDBConnecton($connStr)
{
  $db = pg_connect( $connStr );
  if ( !$db ) {
    return false;
  }
  debug( sprintf("Connected DB: %s", $connStr));
  return $db;
}


?>