#! /usr/local/bin/perl

#----------------------------------------------------------------------
#	 だぼっちバトルロイヤル ver 1.17 (Free)
#	 製作者	: Alpha-kou.(b-ban2)
#	 E-MAIL	: dabo@dabo.design.co.jp
#	 URL	: http://D-BR.net/
#
#        改造者	: ゴードン
#        E-MAIL	: zaza99jp@yahoo.co.jp
#	 URL	: http://godon.bbzone.net/
#
# 使用前にまず利用規定を読んでください
#	http://D-BR.net/kitei.html
#       http://howaitoman.hp.infoseek.co.jp/kitei.html
# [このスクリプトを使用して起きたいかなる損害にも責任は負いません。]
#----------------------------------------------------------------------

$| = 1;
require './jcode.pl';

########## ローカル変数指定
sub kankyou{

# クッキーを取得
        &get_cookie;

#基本設定

	$cgifile = './uma.cgi';	# このファイル名
	$logfile = './chara.dat';	# キャラ登録ファイル
	$timefile = './time.dat';	# 時間記録ファイル
	$rankfile = './rank.dat';	# ランキングファイル
	$fightfile = './fightlog.dat';	# 前の試合の記録ファイル
        $commentfile	= './comment.dat';	# コメントファイル
        $cntfile = './count.dat';       # カウンタファイル
        $orfile = './orank.dat';	# オーナーランキングファイル

	$method = 'POST';	# GET or POSTを指定
	$max_chara = '30';	# 対戦待ちキャラの最大数
	$max_fight = '6';	# 戦いの記録の最大数
	$max_rank = '20';	# ランキングの最大数

	$acomment = '<font color=ffffff>激突競馬バトル２は競走馬を登録してゲームです。<br>
４チーム以上集まったら最大１時間に３回レースが自動で行われます。<br>
なお、重複登録や同じ（馬名・馬主名）での登録は出来ません。<br>
現在は25レースで自動的に引退します。</font>';
# タイトル下のコメント（タグ可能）
	$url = 'boc-keiba.mints.ne.jp';	# 戻り先ＵＲＬ

	$nameleng = '9' ;	# 名前の長さを全角何文字までにするか。

# ページ全体（変数の名前はbodyタグそのままです。）

	$bgcolor = '#2E8B57';	# default:#2E8B57
	$text = 'ffffff';	# default:ffffff
	$link = '0000CD';	# default:0000CD
	$vlink = '6699FF';	# default:6699FF
	$alink = '303030';	# default:303030
        $comcolor = '#2E8B57';  #コメントの背景色
	$background = '';	# 背景画像（絶対パス）

	$ysize = 600;		# 横幅（解像度が低い人のために、出来るだけ600にしてください。）

# タイトル
        $title = '激突競馬バトル';	# タイトル
	$title2 = '激突競馬バトル';	# ブラウザに表示されるタイトル
	$tcolor = '#FF4500';	# タイトルの色(default:#FF4500)
	$tsize = '6';		# タイトルサイズ(default:6)
        $bbs_name  = '';			# 掲示板の名前
	$bbs_url  = '';           # 掲示板のＵＲＬ

# アイコンフォルダパス
        $imgurl  ="http://127.0.0.1/uma/icon/";   # 各自ファルダの絶対パス


# ゲームバランス諸設定
        $battle = '10';            # １時間に何レースか（20=１時間に3回　10=１時間に6回）
        $intai = '25';             # 何レースで引退させるか
        $max_com = '10';            # コメントの最大数
        $max_zi ='35';             #コメントの最大字数


# 表示部分

	$iroformwaku = '#6699FF';# フォームボタン周りの色(default:#6699FF)
	$ccolor = '#FF0000';	# 対戦時のキャラの色
	$mestop = 'トップページ';
	$mesrec = '競走馬の登録';
	$mesrank = '名馬ランキング';
	$meshome = 'ホームページ';
	$mesrule = 'ｹﾞーﾑ説明';

# 対戦待ちリストの項目の名前
	$tableno = 'NO';	        # 番号
	$tablenam = '馬名';     	# 名前
	$tableaut = '馬主';	        # 作者
	$tablelif = 'の競走距離';	# 体力
	$tablepow = 'スピード';  	# 攻撃力
	$tabledef = '瞬発力';   	# 防御力
	$tablespe = '気性';     	# すばやさ
	$tabledat = '登録日時'; 	# 登録日時


### アイコン

	@icon1 = ('uma1','uma2','uma3','uma4','uma5');	  # 'uma1'のように、ファイル名を記入してください。.gifはいりません。
	@icon2 = ('栃栗毛','黒鹿毛','芦毛','白毛','青毛');	# '栃栗毛'のように、表示させる文字を記入してください。


# ミニカウンタの設置
# → 0=no 1=テキスト 
$counter = 1;

########## 設定ここまで

#### アイコンリストの取得

	$ii = 0;
	@iconlist = ();
	foreach $list (@icon2) {
		push @iconlist, "<option value=\"$icon1[$ii].gif\">$list</option>";
		$ii++;	
}

$body = "<body bgcolor=\"$bgcolor\" text=\"$text\" alink=\"$alink\" link=\"$link\" vlink=\"$vlink\" background=\"$background\">";


}#end kankyou

srand( time() ^ ( $$ + ( $$ << 15)) );

&kankyou;
&decode;
&readlog;

# 対戦処理
         if(int($min/$battle) ne $times[0] && $lines[3]){require './uma_race.cgi';&syori;}
# 登録処理
	 if($form{'record'}) {&record;&rec;exit;}
         if($form{'no'}){&fight;exit;}
         if($form{'rule'}){&rule;exit;}
         if($form{'rec'}){&rec;exit;}
         if($form{'rank'}){&rank;exit;}
         if($form{'orank'}){&orank;exit;}
         if($form{'log'}){&log;exit;}
         if($form{'comment'}){&comsyori;}

&html;

exit;


##### デコード＆ローカル変数へ受け渡し
sub decode{

#入力された値をデコード
	if ($ENV{'REQUEST_METHOD'} eq "GET") {
		$buffer = $ENV{'QUERY_STRING'};
	} elsif ($ENV{'REQUEST_METHOD'} eq "POST") {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	}
@pairs = split(/&/,$buffer);
foreach $pair (@pairs) {
	($key, $value) = split(/=/, $pair);
	$value =~ tr/+/ /;
	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
	&jcode'convert(*value, "sjis");
	$value =~ s/</&lt;/g;
	$value =~ s/>/&gt;/g;
	$value =~ s/;/；/g;
	$value =~ s/　//g;
	$value =~ s/ //g;
	$form{$key} = $value;

	}

}#end decode

##### ログ読み込み
sub readlog{
	open(DB,"$logfile");
	seek(DB,0,0);  @lines = <DB>;  close(DB);
	
	($lno, $lname, $lsakusya, $lhomepage, $llif, $lpow, $ldef, $lspe, $ldate, $lip, $licon, $lwin, $lsyu, $ltotal, $ltyoushi, $lashi, $lname2, $lpow2, $ldef2, $lspe2, $licon2, $ltyoushi2, $lashi2, $lname3, $lpow3, $ldef3, $lspe3, $licon3, $ltyoushi3, $lashi3, $ltname,) = split(/<>/,$lines[0]);

	open(TM,"$timefile");
	seek(TM,0,0);  @times = <TM>;  close(TM);

# 時間の取得
	
	$times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);


# 時間ファイルが空の時はここで出力

	if($times[0] eq ""){
	$times[0] = int($min/$battle);
	open(TM,">$timefile") ;
		eval 'flock(TM,2);';
		seek(TM,0,0);	print TM @times;
		eval 'flock(TM,8);';
	close(TM);
	}

}#end


##### 馬登録処理

sub record{

if($lines[${max_chara}-1]){&error(0);}

# 変数を置き換える
	$formchara = $form{'chara'};
        $formchara2 = $form{'chara2'};
        $formchara3 = $form{'chara3'};
	$formname = $form{'name'};
        $formtname = $form{'tname'};
	$formhp = $form{'hp'};
	$formpow = int($form{'power'});
        $formpow2 = int($form{'power2'});
        $formpow3 = int($form{'power3'});
	$formdef = int($form{'defence'});
        $formdef2 = int($form{'defence2'});
        $formdef3 = int($form{'defence3'});
	$formspe = int($form{'speed'});
        $formspe2 = int($form{'speed2'});
        $formspe3 = int($form{'speed3'});
        $formicon = $form{'icon'};
        $formicon2 = $form{'icon2'};
        $formicon3 = $form{'icon3'};
        $formsyu = $form{'syu'};
        $formashi = $form{'ashi'};
        $formashi2 = $form{'ashi2'};
        $formashi3 = $form{'ashi3'};

# 能力値チェック
	if(($formpow > 70)||($formpow < 10)){&error(1)};
	if(($formdef > 70)||($formdef < 10)){&error(1)};
	if(($formspe > 70)||($formspe < 10)){&error(1)};
        if(($formpow2 > 70)||($formpow2 < 10)){&error(1)};
	if(($formdef2 > 70)||($formdef2 < 10)){&error(1)};
	if(($formspe2 > 70)||($formspe2 < 10)){&error(1)};
        if(($formpow3 > 70)||($formpow3 < 10)){&error(1)};
	if(($formdef3 > 70)||($formdef3 < 10)){&error(1)};
	if(($formspe3 > 70)||($formspe3 < 10)){&error(1)};
	$total = $formpow + $formdef + $formspe ;
        if($total ne 100){&error(2)};
        $total2 = $formpow2 + $formdef2 + $formspe2 ;
        if($total2 ne 100){&error(2)};
        $total3 = $formpow3 + $formdef3 + $formspe3 ;
	if($total3 ne 100){&error(2)};

# 名前の長さチェック
	if((length($formchara) < 1)||(length($formchara) > $nameleng *2)){&error(3)};
        if((length($formchara2) < 1)||(length($formchara2) > $nameleng *2)){&error(3)};
        if((length($formchara3) < 1)||(length($formchara3) > $nameleng *2)){&error(3)};
	if((length($formname) < 1)||(length($formname) > $nameleng *2)){&error(3)};
        if((length($formtname) < 1)||(length($formtname) > $nameleng *2)){&error(3)};
	($formhp =~ /^http:\/\/[a-zA-Z0-9]+/) || ($formhp = '');	#ＨＰの判定

        open(DB,"$logfile");    # （馬名・馬主）の重複チェック
        seek(DB,0,0);@lines = <DB>; close(DB);   
        foreach $lines (@lines){
($lno, $lname, $lsakusya, $lhomepage, $llif, $lpow, $ldef, $lspe, $ldate, $lip, $licon, $lwin, $lsyu, $ltotal, $ltyoushi, $lashi, $lname2, $lpow2, $ldef2, $lspe2, $licon2, $ltyoushi2, $lashi2, $lname3, $lpow3, $ldef3, $lspe3, $licon3, $ltyoushi3, $lashi3, $ltname,) = split(/<>/,$lines);
      if($lname eq $formchara){&error(5)}
      if($lname eq $formchara2){&error(5)}
      if($lname eq $formchara3){&error(5)}
      elsif($lsakusya eq $formname){&error(5)}
       $lines = "$lno<>$lname<>$lsakusya<>$lhomepage<>$llif<>$lpow<>$ldef<>$lspe<>$ldate<>$lip<>$licon<>$lwin<>$lsyu<>$ltotal<>$ltyoushi<>$lashi<>$lname2<>$lpow2<>$ldef2<>$lspe2<>$licon2<>$ltyoushi2<>$lashi2<>$lname3<>$lpow3<>$ldef3<>$lspe3<>$licon3<>$ltyoushi3<>$lashi3<>$ltname<>\n";}

# リモートホスト取得
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};
        for ($i=0; $i<$#lines+1; $i++){
	@checkip = split(/<>/,$lines[$i]);
#       if($host eq $checkip[9]){&error(4);}
        }

# 登録ナンバー

	open(DBTMP,"$logfile");    #chara.dat
	seek(DBTMP,0,0);  @linestmp = <DBTMP>;  close(DBTMP);
	foreach $i (0..(@linestmp-1)) {
	@Buftmp = split('<>', @linestmp[$i]);
	$SDatatmp{$i} = $Buftmp[0];
	}

	@SortDatatmp = sort {($SDatatmp{$b} <=> $SDatatmp{$a}) || ($b cmp $a)} keys(%SDatatmp);

	$lno = $linestmp[$SortDatatmp[0]] +1;

# 登録時刻
	$year += 1900;
	$month = sprintf("%02d",$mon +1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$sec = sprintf("%02d",$sec);
	$jikan = "$month/$mday $hour:$min:$sec";

# クッキーを発行
        &set_cookie;

# ログへ書き込むスタイルの整形
	$kakiko = "$lno<>$formchara<>$formname<>$formhp<>400<>$formpow<>$formdef<>$formspe<>$jikan<>$host<>$formicon<>0<>$formsyu<>0<>5<>$formashi<>$formchara2<>$formpow2<>$formdef2<>$formspe2<>$formicon2<>5<>$formashi2<>$formchara3<>$formpow3<>$formdef3<>$formspe3<>$formicon3<>5<>$formashi3<>$formtname<>\n";

# ログへの書き込み
	open(DB,">>$logfile") ;
		eval 'flock(DB,2);';
		print DB $kakiko;
		eval 'flock(DB,8);';
	close(DB);
push(@lines,$kakiko);

open(OR,"+<$orfile") || &error('指定されたファイルが開けません。');
	eval 'flock(OR,2);';

@oranks = <OR>;
                $oranka = "$formname<>0<>\n";
         foreach $check (@oranks){
		@check = split(/<>/,$check);
		if($formname eq $check[0]){$flag=1;last;}
		}
                if($flag ne "1"){push(@oranks,$oranka);}


# オーナーログへの書き込み
	truncate (OR, 0); 
	seek(OR,0,0);	print OR @oranks;
	close(OR);
	eval 'flock(OR,8);';

# 記録したしるし

$recflag = '1';

}#end record

##### コメント記入処理
sub comsyori{

         # リモートホスト取得
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};
	if(length($form{'comtext'}) < 1 || length($form{'comtext'}) > $max_zi * 2){&error(6)}
	open(CF,"+<$commentfile") || &error('指定されたファイルが開けません。');
	eval 'flock(CF,2);';

	@comments = <CF>;

        foreach $line (@comments) {
        &jcode'convert(*line,'sjis');
        local($comm,$host) = split(/<>/,$line);
        if($comm eq $form{'comtext'}){
        &error(7);
        }
        }
	$kakiko = "$form{'comtext'}<>$host\n";

	unshift(@comments, $kakiko);
	splice(@comments, $max_com);

        truncate (CF, 0); 
	seek(CF,0,0);	print CF @comments;
	close(CF);
	eval 'flock(CF,8);';

}#end comsyori


#####著作権表示

sub chosaku{
&secretcopyright;
print <<"_CHOSAKU_";

<hr size="1" color=ffffff>
<div align="right"><a href="http://godon.bbzone.net/" target=_blank><font size="2"><font color=ffffff>激突競馬バトルver1.10(Free)</font></a></div></font>
<div align="right"><a href="http://sweet.oc.to/" target=_blank><font size="2"><font color=ffffff>馬画像原型　：　\"Without Dreams(閉鎖中)"</font></a></div>
<div align="right"><a href="http://www3.to/uma-zura" target=_blank><font size="2"><font color=ffffff>騎手画像　：　"um@-zura"</font></a></div></font>
<div align="right"><a href="http://D-BR.net/" target=_blank><font size="2"><font color=ffffff>オリジナル版/だぼっちバトルロイヤルver1.17(Free)</font></a></div>
<!--広告バナー挿入位置、ページ下部-->
</body>
</html>
_CHOSAKU_

}#end chosaku


##### 出力
sub html{

if ($title){$acomment = "<BR><BR>$acomment";}

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--広告バナー挿入位置、ページ上部-->
<center><font color="$tcolor" size="$tsize">$title</font>$acomment<P>
<a href=$bbs_url target=_blank><font color=ffffff>$bbs_name</a></font>
<html>

<DIV align="center"><TABLE width="800" cellpadding="0" cellspacing="10"><TBODY><tr><td valign="top"><CENTER><table border=1 width=220>
_HTML1_

	open(FG,"$fightfile");
	seek(FG,0,0);  @fg = <FG>;  close(FG);
       
        print "<td valign=top bgcolor=$iroformwaku><center><font color=000000><B>レースの記録</B></font></center></td>\n";
	for ($i=0 ; $i<$max_fight ; $i++){
	$fgno = $i +1;
	
	if($fg[$i]){
	($time , $tname , $fight) = split(/<>/,$fg[$i]);
	print "<tr><td><center><a href=\"$cgifile?no=$fgno\"><font color=ffffff size=2>$time</a></font><br><font color=#7FFFD4 size=2>$tname</font></center></td></tr>\n";
	}
	}

print <<"_HTML2_";

</table>
</center>
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="6"><tr><td bgcolor="$iroformwaku">
<center><input type="submit" name="rec" value="競走馬の登録">
<input type="submit" name="rule" value="ｹﾞーﾑ説明">
<center><input type="submit" name="rank" value="名馬チームランキング">
<input type="submit" name="orank" value="有力な生産家">
<form action="$cgifile" method="$method">
<input type="button" value="ﾎｰムﾍﾟｰｼﾞ" onClick="top.location.href='$url'">
</td></tr></table>
</form>

_HTML2_
if($counter){
           &counter;
           }
print <<"_HTML1_";

<TD align="center" valign="top" rowspan="1">
<table border="1" width=580 cellpadding="0"><tr><td bgcolor=$iroformwaku><center><font color=000000><B>$tableno</td><td bgcolor=$iroformwaku><center><font color=000000><B>$tablenam</td><td bgcolor=$iroformwaku><center><font color=000000><B>脚質・調子</td><td bgcolor=$iroformwaku><center><font color=000000><B>騎手</td><td bgcolor=$iroformwaku><center><font color=000000><B>$tableaut</td><td bgcolor=$iroformwaku><center><font color=000000><B>チーム名・成績</td></tr>

_HTML1_

foreach $line (@lines) {
	($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $name2, $pow2, $def2, $spe2, $icon2, $tyoushi2, $ashi2, $name3, $pow3, $def3, $spe3, $icon3, $tyoushi3, $ashi3, $tname,) = split(/<>/,$line);
	if($homepage){$sakusya = "<a href=\"$homepage\"><font color=yellow>$sakusya</font></a>"}
	$icon_pri2 = "<img src=\"$imgurl/$syu\" align=\"absmiddle\">";

        if   ($tyoushi < 2){ $cond = "1.gif"; }
	elsif($tyoushi < 4){ $cond = "2.gif"; }
	elsif($tyoushi < 7){ $cond = "3.gif"; }
	elsif($tyoushi < 9){ $cond = "4.gif"; }
	elsif($tyoushi < 11){ $cond = "5.gif"; }

        if   ($ashi == 1){$sakusen ="nige.gif";}
        elsif($ashi == 2){$sakusen ="senkou.gif";}
        elsif($ashi == 3){$sakusen ="sashi.gif";}
        elsif($ashi == 4){$sakusen ="oikomi.gif";}

        if   ($tyoushi2 < 2){ $cond2 = "1.gif"; }
	elsif($tyoushi2 < 4){ $cond2 = "2.gif"; }
	elsif($tyoushi2 < 7){ $cond2 = "3.gif"; }
	elsif($tyoushi2 < 9){ $cond2 = "4.gif"; }
	elsif($tyoushi2 < 11){ $cond2 = "5.gif"; }

        if   ($ashi2 == 1){$sakusen2 ="nige.gif";}
        elsif($ashi2 == 2){$sakusen2 ="senkou.gif";}
        elsif($ashi2 == 3){$sakusen2 ="sashi.gif";}
        elsif($ashi2 == 4){$sakusen2 ="oikomi.gif";}

        if   ($tyoushi3 < 2){ $cond3 = "1.gif"; }
	elsif($tyoushi3 < 4){ $cond3 = "2.gif"; }
	elsif($tyoushi3 < 7){ $cond3 = "3.gif"; }
	elsif($tyoushi3 < 9){ $cond3 = "4.gif"; }
	elsif($tyoushi3 < 11){ $cond3 = "5.gif"; }

        if   ($ashi3 == 1){$sakusen3 ="nige.gif";}
        elsif($ashi3 == 2){$sakusen3 ="senkou.gif";}
        elsif($ashi3 == 3){$sakusen3 ="sashi.gif";}
        elsif($ashi3 == 4){$sakusen3 ="oikomi.gif";}

        $lose = $total - $win;
        if($win > 0){
	print "<tr><td><center>$no</td><td><center>$name<br>$name2<br>$name3<br></td><td><center><img src=\"$imgurl/$sakusen\"><img src=\"$imgurl/$cond\"><br><img src=\"$imgurl/$sakusen2\"><img src=\"$imgurl/$cond2\"><br><img src=\"$imgurl/$sakusen3\"><img src=\"$imgurl/$cond3\"></td><td><center>$icon_pri2</td><td><center>$sakusya</td><td><center><font color=gold><B>$tname</B></font><br><font color=#00FFFF>$total回出走：<B>$win勝</B>$lose敗</td></tr>\n";

}else
{print "<tr><td><center>$no</td><td><center>$name<br>$name2<br>$name3<br></td><td><center><img src=\"$imgurl/$sakusen\"><img src=\"$imgurl/$cond\"><br><img src=\"$imgurl/$sakusen2\"><img src=\"$imgurl/$cond2\"><br><img src=\"$imgurl/$sakusen3\"><img src=\"$imgurl/$cond3\"></td><td><center>$icon_pri2</td><td><center>$sakusya</td><td><center><font color=gold><B>$tname</B></font><br><font color=#7FFFD4>$total回出走：0勝$lose敗</td></tr>\n";}
}

print <<"_HTML2_";
</table>
</TBODY> 
</TABLE>
</DIV><HR size=1 color=ffffff>
</center>
<form action="$cgifile" method="$method">
<center>コメント
<input type=text name=comtext size=75>
<input type=hidden name=comment value=1>
<input type=submit name=comment value="書き込む">
</form>
<center>
_HTML2_

open(CF,"$commentfile") || &error('指定されたファイルが開けません。');
	seek(CF,0,0);  @comments = <CF>;  close(CF);

	print "<br><table border=1 width=\"660\" cellpadding=5 cellspacing=0>\n";
	print "<tr align=\"center\"><td>コメント</td></tr>\n";
	print "<tr><td bgcolor=\"$comcolor\">\n";

	$i = 0;
	foreach(@comments){
		($com) = split /<>/;
		print "■ ：『 $com 』 \n";

		if($i ne $#comments){ print "<hr width=\"100%\" size=1>\n"; }
		$i++;
	}
	print "</table><br>\n";

&chosaku;

}#end html


##### 馬登録出力

sub rec{

print "Content-type: text/html\n\n";#コンテントタイプ出力
print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body

<center><font color="$tcolor" size="$tsize">$mesrec</font>

_HTML1_

if($recflag){
print <<"_HTML3_";
<P>
登録完了しました。
</P>
_HTML3_

} else {

        open(LL,"$logfile");
	seek(LL,0,0);  @kazu = <LL>;  close(LL);
        
        if($#kazu+2 > $max_chara){
        print "<br><br>現在最大登録数に達しているので登録出来ません。<BR><BR>";
              }else{

print <<"_HTML3_";

<P>
<table border="1" width="$ysize" cellpadding="5"><tr><td>
<form action="$cgifile" method="$method">
<table width="100%" border="1"><tr><td>
<center>距離</td><td><center>馬名（$nameleng文字まで）</td><td><center>毛色</td><td><center>脚質</td><td><center>スピード<br><b>10～70</b></td><td><center>瞬発力<br><b>10～70</b></td><td><center>気性<br><b>10～70</b></td></tr><tr><td>
<font size="2">
<center>１走距離<br><center>（100）</td><td>
<center><input type="text" name="chara" size="16"></td><td>
<center><select name="icon">@iconlist</select></td><td>
<center><select name="ashi">
<option value="1">逃げ
<option value="2">先行
<option value="3">差し
<option value="4">追込
</select></td><td>
<center><input type="text" name="power" value="$c_power" size="3"></td><td>
<center><input type="text" name="defence" value="$c_def" size="3"></td><td>
<center><input type="text" name="speed" value="$c_spe" size="3"></td></tr><tr><td>
<font size="2"><center>２走距離<br><center>（100）</td><td>
<center><input type="text" name="chara2" size="16"></td><td>
<center><select name="icon2">@iconlist</select></td><td>
<center><select name="ashi2">
<option value="1">逃げ
<option value="2">先行
<option value="3">差し
<option value="4">追込
</select></td><td>
<center><input type="text" name="power2" value="$c_power2" size="3"></td><td>
<center><input type="text" name="defence2" value="$c_def2" size="3"></td><td>
<center><input type="text" name="speed2" value="$c_spe2" size="3"></td></tr><tr><td>
<font size="2"><center>３走距離<br><center>（200）</td><td>
<center><input type="text" name="chara3" size="16"></td><td>
<center><select name="icon3">@iconlist</select></td><td>
<center><select name="ashi3">
<option value="1">逃げ
<option value="2">先行
<option value="3">差し
<option value="4">追込
</select></td><td>
<center><input type="text" name="power3" value="$c_power3" size="3"></td><td>
<center><input type="text" name="defence3" value="$c_def3" size="3"></td><td>
<center><input type="text" name="speed3" value="$c_spe3" size="3"></td></tr><tr><td colspan="7">
<select name="syu">
<option value="kisyu1.gif">武　豊
<option value="kisyu2.gif">河　内
<option value="kisyu3.gif">後　藤
<option value="kisyu4.gif">四　位
<option value="kisyu5.gif">蛯　名
<option value="kisyu6.gif">角　田
<option value="kisyu7.gif">岡　部
<option value="kisyu8.gif">横　山
<option value="kisyu9.gif">柴　田
<option value="kisyu10.gif">ペ　リ　エ
<option value="kisyu11.gif">藤　田
<option value="kisyu12.gif">武　幸
<option value="kisyu13.gif">小　島
</select>：騎手アイコン <br>
<input type="text" name="tname" size="16">：チームの名前（全角$nameleng文字まで）<br>
<input type="text" name="name" value="$c_name" size="16">：あなたの名前（全角$nameleng文字まで）<br>
<input type="text" name="hp" value="$c_hp" size="50">：ホームページ(空白\可\)<BR></td></tr><tr><td colspan="7">
<li>各馬のスピード・瞬発力・気性の合計が100になるようにね<br>
<li>騎手アイコンは\能\力に影響しないよ。<br>
<center><input type="submit" value="登録">
</font></table>
<input type="hidden" name="record" value="1">
</form>
</td></tr></table>
</P>

_HTML3_
}}

print <<"_HTML2_";
</table>
</P>
</center>
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" value="$mestop">
<input type="button" value="$meshome" onClick="top.location.href='$url'">
</td></tr></table>
</form>
_HTML2_
&chosaku;
}#end rec


##### ランキング出力
sub rank{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<center><font color='white' size=6>名馬チームランキング</font><P>

<table border="1" width="$ysize">

<tr><td bgcolor=$iroformwaku><center><font color=000000><B>勝数</td><td bgcolor=$iroformwaku><center><font color=000000><B>チーム名</td><td bgcolor=$iroformwaku><center><font color=000000><B>馬名</td><td bgcolor=$iroformwaku><center><font color=000000><B>騎手</td><td bgcolor=$iroformwaku><center><font color=000000><B>$tableaut</td></tr>

_HTML1_
	open(RK,"$rankfile");
	seek(RK,0,0);  @ranks = <RK>;  close(RK);

foreach $rank (@ranks) {
	($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $name2, $pow2, $def2, $spe2, $icon2, $tyoushi2, $ashi2, $name3, $pow3, $def3, $spe3, $icon3, $tyoushi3, $ashi3, $tname,) = split(/<>/,$rank);
	if($homepage){$sakusya = "<a href=\"$homepage\" target=_blank><font color=yellow>$sakusya</font></a>"}
       $icon_pri2 = "<img src=\"$imgurl/$syu\" align=\"absmiddle\">";
        if($win > 22){$iro = "#FFFF00";}
        elsif($win > 19){$iro = "#00FFFF";}
        elsif($win > 14){$iro = "#00FF00";}
        if($win == 25){$ookisa = "6";}
        else{$ookisa = "5";}
        if($win > 14){$div = "<DIV STYLE='width:100%; filter:Glow(color=$iro)'>";$div2 = "</DIV>";}
	print "<tr><td><center><B><font color=ffffff size=$ookisa>$div$win勝</font>$div2</B></td><td><center><B>$tname</B></td><td><center>$name<br>$name2<br>$name3</td><td><center>$icon_pri2</td><td><center>$sakusya</td></tr>";
	}

print <<"_HTML2_";
</table>
</center>
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" value="$mestop">
<input type="submit" name="rec" value="$mesrec">
<input type="button" value="$meshome" onClick="top.location.href='$url'">
</td></tr></table>
</form>
_HTML2_
&chosaku;
}#end rank


##### 有力な生産家出力
sub orank{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>有力な生産家</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
body,table{cursor:url(http://howaitoman.hp.infoseek.co.jp/a.cur);}
-->
</style>
<center><br><font color=white size=5><B>有力な生産家(トップ２０)</B></font><P>

<table border="1" width="400">

<tr><td bgcolor=#87CEFA><center><font color=000000><B>勝数</td><td bgcolor=#87CEFA><center><font color=000000><B>名前</td><td bgcolor=#87CEFA><center><font color=000000><B>ランク</td></tr>

_HTML1_

open(OK,"$orfile");
	seek(OK,0,0);  @orank = <OK>;  close(OK);

        if($#orank < 20){$oranksuu = $#orank;}
        else{$oranksuu = 19;}
for ($i=0; $i<$oranksuu+1; $i++){
	($sakusya[$i], $win[$i], ) = split(/<>/,$orank[$i]);
	
        if($win[$i] > 99){$iro[$i] = "#FFFF00";}
        elsif($win[$i] > 39){$iro[$i] = "#00FFFF";}
        elsif($win[$i] > 19){$iro[$i] = "#00FF00";}
        else{$iro[$i] = "000000";}
        if($win[$i] > 55){$ookisa[$i] = "4";}
        else{$ookisa[$i] = "3";}

          if($win[$i] > 699){$syou[$i] = "世界馬生産界の神";}
          elsif($win[$i] > 499){$syou[$i] = "大暗黒馬界の王";}
          elsif($win[$i] > 399){$syou[$i] = "日本馬界の王";}
          elsif($win[$i] > 299){$syou[$i] = "日本馬界の救世主";}
          elsif($win[$i] > 399){$syou[$i] = "馬生産界のトップ";}
          elsif($win[$i] > 99){$syou[$i] = "馬生産家業";}
          elsif($win[$i] > 74){$syou[$i] = "馬生産人";}
          elsif($win[$i] == 77){$syou[$i] = "(ﾟдﾟ)ｳﾏｰ";}
          elsif($win[$i] > 49){$syou[$i] = "相馬眼（・∀・）ｲｲ!";}
          elsif($win[$i] > 24){$syou[$i] = "（・∀・）ｲｲ!馬生産家";}
          elsif($win[$i] > 14){$syou[$i] = "もっと馬を生産しる";}
          elsif($win[$i] > 9){$syou[$i] = "馬好き";}
          elsif($win[$i] > 4){$syou[$i] = "馬人";}
          else{$syou[$i] = "一般人";}
            
           
	print "<tr><td><center><B><font color='white' size=$ookisa[$i]>$win[$i]勝</font></B></td><td><center>$sakusya[$i]</td><td><center>$syou[$i]</td></tr>";
	}
       
print <<"_HTML2_";
</table>
</center>
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" value="$mestop">
<input type="submit" name="rec" value="$mesrec">
<input type="button" value="$meshome" onClick="top.location.href='$url'">
</td></tr></table>
</form>
_HTML2_
&chosaku;
}#end orank


#######  カウンタ処理

sub counter{
	local($cnt,$host);

# カウントファイルを読みこみ
	open(IN,"$cntfile") || &error("Open Error : $cntfile");
	eval "flock(IN, 1);";
        $data = <IN>;
	close(IN);

# リモートホスト取得
	$hostt = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

# 別ＩＰ時のみカウントアップ
        ($cnt, $host) = split(/<>/, $data);
        if($host ne $hostt){
        $cnt++;
	open(OUT,"+< $cntfile") || &error("Write Error : $cntfile");
	eval "flock(OUT, 2);";
	truncate(OUT, 0);
	seek(OUT, 0, 0);
	print OUT "$cnt\<>$hostt";
	close(OUT);
	}

# カウンタ表示
	if($counter){
		print "$cnt人の観戦者<br>\n";
	}
}#end counter

#######  クッキーの発行

sub set_cookie{
	$ENV{'TZ'} = "GMT"; # 国際標準時を取得
	local($secg,$ming,$hourg,$mdayg,$mong,$yearg,$wdayg,$ydayg,$isdstg)=localtime(time+60*24*60*60);
	$yearg += 1900;
	if ($secg  < 10)  { $secg  = "0$secg";  }
	if ($ming  < 10)  { $ming  = "0$ming";  }
	if ($hourg < 10)  { $hourg = "0$hourg"; }
	if ($mdayg < 10)  { $mdayg = "0$mdayg"; }
	$month = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec')[$mong];
	$youbi = ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday')[$wdayg];
	$ENV{'TZ'} = "Japan";
	$date_gmt = "$youbi, $mdayg\-$month\-$yearg $hourg:$ming:$secg GMT";

        $cookies="name\<>$formname\,hp\<>$formhp\,power\<>$formpow\,power2\<>$formpow2\,power3\<>$formpow3\,def\<>$formdef\,def2\<>$formdef2\,def3\<>$formdef3\,spe\<>$formspe\,spe2\<>$formspe2\,spe3\<>$formspe3";
	print "Set-Cookie: UMA=$cookies; expires=$date_gmt\n";
}#end set_cookie

#######  クッキーを取得

sub get_cookie{ 
    @pairs = split(/\;/, $ENV{'HTTP_COOKIE'});
    foreach $pair (@pairs) {
      local($name, $value) = split(/\=/, $pair);
      $name =~ s/ //g;
      $DUMMY{$name} = $value;
    }
    @pairs = split(/\,/, $DUMMY{'UMA'});        
    foreach $pair (@pairs) {
      local($name, $value) = split(/\<>/, $pair);
      $COOKIE{$name} = $value;
    }

        $c_name = $COOKIE{'name'};
        $c_hp = $COOKIE{'hp'};
        $c_power = $COOKIE{'power'};
        $c_power2 = $COOKIE{'power2'};
        $c_power3 = $COOKIE{'power3'};
        $c_def = $COOKIE{'def'};
        $c_def2 = $COOKIE{'def2'};
        $c_def3 = $COOKIE{'def3'};
        $c_spe = $COOKIE{'spe'};
        $c_spe2 = $COOKIE{'spe2'};
        $c_spe3 = $COOKIE{'spe3'};


	if($form{'name'}){$c_name = $form{'name'};}
	if($form{'hp'}){$c_hp = $form{'hp'};}
        if($form{'power'}){$c_power = $form{'power'};}
	if($form{'power2'}){$c_power2 = $form{'power2'};}
        if($form{'power3'}){$c_power3 = $form{'power3'};}
	if($form{'def'}){$c_def = $form{'def'};}
        if($form{'def2'}){$c_def2 = $form{'def2'};}
	if($form{'def3'}){$c_def3 = $form{'def3'};}
        if($form{'spe'}){$c_spe = $form{'spe'};}
	if($form{'spe2'}){$c_spe2 = $form{'spe2'};}
        if($form{'spe3'}){$c_spe3 = $form{'spe3'};}

}#end get_cookie


##### 前の試合の記録
sub log{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<center><font color="$tcolor" size="$tsize">戦いの記録一覧</font>

<table border="1" width="$ysize" cellpadding="5">

_HTML1_

print <<"_HTML2_";
</table>
</center>
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" value="$mestop">
<input type="submit" name="rec" value="$mesrec">
<input type="submit" name="rank" value="$mesrank">
<input type="button" value="$meshome" onClick="top.location.href='$url'">
</tr></tr></table>
</form>
_HTML2_
&chosaku;
}#end log

##### 戦いの具体的な記録
sub fight{

	open(FG,"$fightfile");
	seek(FG,0,0);  @fg = <FG>;  close(FG);

	$no = $form{'no'};
	$no--;
	
	($time , $tname , $fight) = split(/<>/,$fg[$no]);


print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<center><font color="$tcolor" size="$tsize">$time</font>

<hr size="1">

<table border="1" width="$ysize" cellpadding="5">

_HTML1_

print "<tr><td>$fight</td></tr>\n";

print <<"_HTML2_";
</table>
<hr size="1">
</center>
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" value="$mestop">
<input type="submit" name="rec" value="$mesrec">
<input type="submit" name="rank" value="$mesrank">
<input type="button" value="$meshome" onClick="top.location.href='$url'">
</td></tr></table>
</form>
_HTML2_
&chosaku;
}

##### ルール説明
sub rule{

print "Content-type: text/html\n\n";#コンテントタイプ出力

print <<"_HTML_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<center><font color="$tcolor" size="$tsize">あそびかた</font>

<hr size="1">

<table border="1" width="$ysize" cellpadding="5"><tr><td>
<font size="2">
あそびかた<BR><BR>
　・　このゲームは馬を登録して遊ばせるゲームだよ。<BR><BR>
　・　各馬に１００ポイントの能\力値を振り分けてあげてね。<BR><BR>
　・　各能\力値は１０～７０の間にしてね。<BR><BR>
　・　馬が４頭以上登録され、一定時間になるとレースが行われるよ。<BR><BR>
　・　１時間に最大３レース行われるよ。<BR><BR>
　・　馬の勝数のランキングがあるよ。<BR><BR>
　・　生産者の勝数のランキングがあるよ。<BR><BR>
　・　スピードはやはり最重要！レースにおいて常にポイントとなる。<br><br>
　・　瞬発力は最後のスパートに入る時に大切になるよ。<br><br>
　・　気性は悪すぎると馬が思うように走らないよ。<br><br>
　・　調子は勝った馬も負けた馬も変化するよ。<br><br>
</font>
</td></tr></table>
<hr size="1">
</center>
<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="3"><tr><td bgcolor="$iroformwaku">
<input type="submit" value="$mestop">
<input type="submit" name="rec" value="$mesrec">
<input type="submit" name="rank" value="$mesrank">
<input type="button" value="$meshome" onClick="top.location.href='$url'">
</td></tr></table>
</form>
_HTML_
&chosaku;
}

##########エラーメッセージ

###エラーの時の処理。
sub error {

local($no) = @_;

$msg[0] = 'これ以上登録できないよ。掲示板で知らせてくれれば登録最大数を増やします。';
$msg[1] = '能力値が１０～７０になってないよ。';
$msg[2] = '各馬の能力値のトータルが１００になってないよ。';
$msg[3] = "名前の長さは$nameleng文字以下にしてね。";
$msg[4] = "重複登録不可！";
$msg[5] = "その馬名、又は馬主名はすでに使われています。";
$msg[6] = "字数は３５字までです。";
$msg[7] = "すでに同じ書き込みがあります。";
print "Content-type: text/html\n\n";
print <<"_ERROR_";
<html><head><title>ERROR</title></head>
$body
$msg[$no]<BR>
<form action="$cgifile" method="$method">
<input type="submit" value="戻る">
</form>
</body>
</html>
_ERROR_
exit;
}#END error

sub secretcopyright{
$secret = qq|<!--このスクリプトの知的所有権はb-ban2氏とゴードンにあります。-->|;
print $secret;
} #END
