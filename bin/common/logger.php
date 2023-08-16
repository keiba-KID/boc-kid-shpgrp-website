<?php
/***********************************************************
 * D-Log ログ出力メソッド：暫定版
 */


/////////////////////////////////////////////////////////
// 定数
//  ログレベル
const _LOG_LEVEL_ERROR	= 0;		# エラー
const _LOG_LEVEL_WARN	= 1;		# 警告
const _LOG_LEVEL_INFO	= 2;		# 情報
const _LOG_LEVEL_TRACE	= 3;		# トレース
const _LOG_LEVEL_DEBUG	= 4;		# デバッグ

const LogLevel =
[
	_LOG_LEVEL_ERROR	=> 'ERROR',
	_LOG_LEVEL_WARN		=> 'WARN',
	_LOG_LEVEL_INFO		=> 'INFO',
	_LOG_LEVEL_TRACE	=> 'TRACE',
	_LOG_LEVEL_DEBUG	=> 'DEBUG'
];

# 出力するログレベル
const LOG_LEVEL		= _LOG_LEVEL_DEBUG;

// ログフォルダ
const _LOG_FOLDER	= "./log/";

// 標準出力にも出力するかどうか
const WITH_OUTOUT_STD = false;

/********************************************************
 * エラーレベルのログ出力を行う
 * @param msg 出力する文字列
 */
function error( $msg ) {
	_logoutput( _LOG_LEVEL_ERROR, $msg );
}

/********************************************************
 * 警告レベルのログ出力を行う
 * @param msg 出力する文字列
 */
function warn( $msg ) {
	_logoutput( _LOG_LEVEL_WARN, $msg );
}

/********************************************************
 * 情報レベルのログ出力を行う
 * @param msg 出力する文字列
 */
function info( $msg ) {
	_logoutput( _LOG_LEVEL_INFO, $msg );
}

/********************************************************
 * トレースレベルのログ出力を行う
 * @param msg 出力する文字列
 */
function trace( $msg ) {
	_logoutput( _LOG_LEVEL_TRACE, $msg );
}

/********************************************************
 * デバッグレベルのログ出力を行う
 * @param msg 出力する文字列
 */
function debug( $msg ) {
	_logoutput( _LOG_LEVEL_DEBUG, $msg );
}

/********************************************************
 * ログ出力
 * @param $logLevel	[in] ログレベル
 * @param $msg		[in] 出力する文字列
 */
function _logoutput( $logLevel, &$msg )
{
	if ( $logLevel > LOG_LEVEL ) {
			return;
	}

	if ( is_dir( _LOG_FOLDER ) == FALSE ) {
		$old_umask = umask(0);
		if ( mkdir( _LOG_FOLDER, 0770 ) == FALSE ) {
			umask( $old_umask );
			return;
		}
		umask( $old_umask );
	}

	$dbg		= debug_backtrace();
	$logFile	= sprintf( "%s%s.log", _LOG_FOLDER, date("Y-m-d") );
	$dateTime	= date( "Y/m/d H:i:s" ).substr( (string)microtime(), 1, 6 );
	$log		= sprintf( "[%s] %5s %s [%s(%d)]\n", $dateTime, LogLevel[$logLevel], $msg, $dbg[1]['file'], $dbg[1]['line'] );
	error_log( $log, 3, $logFile );
}
?>
