#----------------------------------------------------------------------
# 箱庭諸島 ver2.30
# トップモジュール(ver1.00)
# 使用条件、使用方法等は、hako-readme.txtファイルを参照
#
# 箱庭諸島のページ: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Hakoniwa R.A. ver030314
# メインスクリプト(箱庭諸島 ver2.30)
# 使用条件、使用方法等は、read-renas.txtファイルを参照
#
# KEI PAGE: http://www5b.biglobe.ne.jp/~k-e-i/
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# トップページモード
#----------------------------------------------------------------------
# メイン
sub topPageMain {
    # 開放
    unlock();

    # テンプレート出力
    tempTopPage();
}

# メイン
sub topPageMain {
	#アクセスログ取得
	if($HtopAxes) {
		axeslog();
	}
	# 開放
	unlock();
	# テンプレート出力
	tempTopPage(0);
}

sub topPageMainL {
	#アクセスログ取得
	if($HtopAxes) {
		axeslog();
	}
	# 開放
	unlock();
	# テンプレート出力
	tempTopPage(1);
}

sub topPageMainS {
	#アクセスログ取得
	if($HtopAxes) {
		axeslog();
	}
	# 開放
	unlock();
	# テンプレート出力
	tempTopPage(2);
}

#=============================================
#■アクセスログ取得
#=============================================
sub axeslog {
	my @lines;


	my $cookie;
	$cookie = jcode::euc($ENV{'HTTP_COOKIE'});
	if($cookie =~ /OWNISLANDID=\(([^\)]*)\)/) {
		$cookie = $1;
	}
	
	my $agent   = $ENV{'HTTP_USER_AGENT'};
	my $addr	= $ENV{'REMOTE_ADDR'};
	my $host	= $ENV{'REMOTE_HOST'};
	my $referer = $ENV{'HTTP_REFERER'};
	if (($host eq $addr) || ($host eq '')) {
		$host = gethostbyaddr(pack('C4',split(/\./,$addr)),2) || $addr;
	}
	$ENV{'TZ'} = 'JST-9';
	my($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime(time);
	my $day = ('日','月','火','水','木','金','土')[$wday];
	$year = $year + 1900;
	$mon = $mon + 1;
	my $date = sprintf("%04d/%02d/%02d(%s) %02d:%02d:%02d",$year,$mon,$mday,$day,$hour,$min,$sec);

	open(IN, "$HaxesLogfile");
	my @lines = <IN>;
	close(IN);
	
	while ($HaxesMax <= @lines) { pop @lines; }
	unshift(@lines, "[$date] - $referer - $host - $addr - $agent - $cookie\n");
	
	if(open(OUT, ">$HaxesLogfile")){
		foreach $line (@lines) {
			print OUT jcode::sjis($line);
		}
		close(OUT);
	} else {
		tempProblem();
		return;
	}
}

1;

# トップページ
sub tempTopPage {
    # タイトル
    out(<<END);
${HtagTitle_}$Htitle${H_tagTitle}
END

    # デバッグモードなら「ターンを進める」ボタン
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="ターンを進める" NAME="TurnButton">
</FORM>
END
    }

    if ($HjavaModeSet eq 'java') {
		$radio = ""; $radio2 = "CHECKED";
	}else{
		$radio = "CHECKED";	$radio2 = "";
	}

    # フォーム
    my($remain) = $HunitTime + $HislandLastTime - time;
    out(<<END);
<DIV ID='Turn'><H1>${HtagHeader_}ターン$HislandTurn${H_tagHeader}</H1></DIV>
<FORM name="RemainForm"><INPUT name="RemainTime" size="40" type="text" class="timer" readonly></FORM><SCRIPT language="JavaScript">
<!--
nextTurn = ${remain};
loadDate = new Date();
timerID = setTimeout('dispRemainTime()', 100);

function dispRemainTime() {
	clearTimeout(timerID);
	document.RemainForm.RemainTime.value = getRemainTime();
	timerID = setTimeout('dispRemainTime()', 1000);
}

function getRemainTime() {
	now = new Date();msec = now.getTime() - loadDate.getTime();
	msec -= msec % 1000; msec /= 1000;msec = nextTurn - msec;
	if (msec < 0) {msec = 0;}
	sec = msec % 60; msec = (msec - sec) / 60;
	min = msec % 60; hour = (msec - min) / 60;
	if (hour < 10) {hour = "0" + hour;}
	if (min < 10) {min = "0" + min;}
	if (sec < 10) {sec = "0" + sec;}
	return "次のターンまで残り" + hour + "時間" + min + "分" + sec + "秒";
}
//-->
</SCRIPT>
<HR>
<table>

<TR>
 <TD class=M VALIGN=TOP WIDTH=400>
<DIV ID='myIsland'>
<H1>${HtagHeader_}自分の島へ${H_tagHeader}</H1>
<SCRIPT language="JavaScript">
<!--
function newdevelope(){
//	newWindow = window.open("", "newWindow"); // これだとなぜかエラーに
	document.Island.target = "newWindow";  
	document.Island.submit();
}
function develope(){
	document.Island.target = "";
}
//-->
</SCRIPT>
<FORM name="Island" action="$HthisFile" method="POST">
あなたの島の名前は？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
パスワードをどうぞ！！<BR>
<INPUT TYPE="hidden" NAME="OwnerButton">
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $radio>通常モード
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $radio2>Javaスクリプトモード<BR>
<INPUT TYPE="submit" VALUE="開発しに行く" onClick="develope()">　
<INPUT TYPE="submit" VALUE="新しい画面" onClick="newdevelope()">
</FORM>
</DIV>

END
my($Himfflag);
if($HimgLine eq '' || $HimgLine eq $imageDir){
    $Himfflag = '<FONT COLOR=RED>未設定</FONT>';
} else {
    $Himfflag = $HimgLine;
}

   out(<<END);
</TD>

<TD class=M VALIGN=TOP WIDTH=500>
<DIV ID='localImage'>
<H1>${HtagHeader_}画像のローカル設定(推奨)${H_tagHeader}</H1>
現在の設定<B>[</b> ${Himfflag} <B>]</B>
　　<A HREF=${imageExp} target=_BLANK><FONT SIZE=+1> 説 明 </FONT></A>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET>
</form>

<table>
<TR>
 <TD class=M>
<form action=$HthisFile method=POST>
Macユーザー用<BR>
<INPUT TYPE=text NAME="IMGLINEMAC">
<INPUT TYPE="submit" VALUE="設定" name=IMGSET><BR>
<FONT SIZE=-1>Macの方は、こちらを使用して下さい。</FONT>
</form>
 </TD>
 <TD class=M>
<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="IMGLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="設定を解除する" name=IMGSET>
</form>
 </TD>
</TR>
</table>
</DIV>
 </TD>
</TR>

</table>

<HR>
END
if($topindicate){
    tempVisitPage2();
} else{
    out(<<END);
<H1><A HREF="$baseDir/hako-main.cgi?Visit=">${HtagHeader_}他の島に観光へ行く${H_tagHeader}</A></H1>
END
}
    out(<<END);
<HR>
END
if($Loghtml){
    out(<<END);
<H1><A HREF="$htmlDir/hakolog0.html" target="_blank">${HtagHeader_}最近の出来事${H_tagHeader}</A></H1>
END
} else{
    out(<<END);
<H1>${HtagHeader_}最近の出来事${H_tagHeader}</H1>
END
    logPrintTop();
}
    out(<<END);
<DIV ID='HakoniwaCup'><H1>${HtagHeader_}Hakoniwa Cup$hcturn${H_tagHeader}</H1>
<DIV style="overflow:auto; height:${HdivHeight2}px; width:${HdivWidth2}px;">
END
    hcPrint();
    out(<<END);
</DIV></DIV>
<DIV ID='HistoryLog'><H1>${HtagHeader_}発見の記録${H_tagHeader}</H1>
<DIV style="overflow:auto; height:${HdivHeight}px; width:${HdivWidth}px;">
END
    historyPrint();
    out(<<END);
</DIV></DIV>
END
}

# トップページ用ログ表示
sub logPrintTop {
    my($i);
    for($i = 0; $i < $HtopLogTurn; $i++) {
	logFilePrint($i, 0, 0);
    }
}

# Point順にソート
sub islandSort {
    my($flag, $i, $tmp);

    # 人口が同じときは直前のターンの順番のまま
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{'pts'} <=> $Hislands[$a]->{'pts'} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# 記録ファイル表示
sub historyPrint {
    open(HIN, "${HdirName}/hakojima.his");
    my(@line, $l);
    while($l = <HIN>) {
	chomp($l);
	push(@line, $l);
    }
    @line = reverse(@line);

    foreach $l (@line) {
	$l =~ /^([0-9]*),(.*)$/;
	out("<NOBR>${HtagNumber_}ターン${1}${H_tagNumber}：${2}</NOBR><BR>\n");
    }
    close(HIN);
}

# Hakoniwa Cupログ表示
sub hcPrint {
    open(CIN, "${HdirName}/hakojima.lhc");
    my(@line, $l);
    while($l = <CIN>) {
	chomp($l);
	push(@line, $l);
    }
    @line = reverse(@line);

    foreach $l (@line) {
	$l =~ /^([0-9]*),(.*)$/;
	out("<NOBR>${HtagNumber_}ターン${1}${H_tagNumber}：${2}</NOBR><BR>\n");
    }
    close(CIN);
}

sub rankingMain {
        # 開放
        unlock();

        # テンプレート出力
        tempRankingPage();
}

sub tempRankingPage{

      # hakoniwaRA JS ver4.47から移植
	my $i;
	for($i = 0; $i < $HislandNumber; $i++) {
		my $rena = $Hislands[$i]->{'rena'}; # 軍事力
		$Hislands[$i]->{'renae'} = int($rena / 10 ) + 1;
 		$Hislands[$i]->{'ene'} = (split(/,/, $Hislands[$i]->{'eisei3'}))[0];

		my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $Hislands[$i]->{'eisei4'});
		$Hislands[$i]->{'kachiten'} = $stwin*3 + $stdrow;
		$Hislands[$i]->{'kachitent'} = $stwint*3 + $stdrowt;
		my $siaisu = $stwint + $stdrowt + $stloset;
		$siaisu = 1 if($siaisu == 0);
		$Hislands[$i]->{'shoritu'} = int($stwint / $siaisu * 100);
		$Hislands[$i]->{'teamforce'} = $sto + $std + $stk;
		$Hislands[$i]->{'styusho'} = $styusho;

		my($mshp, $msap, $msdp, $mssp) = (split(/,/, $Hislands[$i]->{'eisei5'}))[0..3];
		$Hislands[$i]->{'force'} = $mshp + $msap + $msdp + $mssp;

		my(@ZA) = split(/,/, $Hislands[$i]->{'etc6'});
		$Hislands[$i]->{'monsfig'} = 0;
		foreach(@ZA){
		    $Hislands[$i]->{'monsfig'} += $_; # 怪獣の総数を算出 
		}
		$Hislands[$i]->{'monsfig'} += $Hislands[$i]->{'monsterlive'};

		foreach (split(/,/, $Hislands[$i]->{'eisei6'})) {
			$Hislands[$i]->{'tuni'} += $_;
			$Hislands[$i]->{'uni'}++ if($_ > 0);
		}
	}

	my @elements   = ( 'pop', 'farm', 'factory', 'mountain', 'fore', 'tare', 'zipro', 'leje', 'monsfig', 'taiji', 'force', 'eisei2', 'uni', 'kei', 'renae', 'shoritu', 'styusho', 'teamforce', 'etc0', 'ene');
	my $hcturn = int($HislandTurn/100) * 100;
	my @bumonName  = ('人口', '農場',  '職場',   '採掘場',  '森林', 'にわとり数', 'ぶた数', 'うし数',  '怪獣出現＆捕獲数', '怪獣退治数', '生物大学能力', '通算観光客', 'ユニーク地形数', '記念碑数', '軍事技術', 'HC通算勝率', 'HC優勝回数', 'サッカーチーム力', '鉄道', '電力');
	my @islands;
	my @ids;
	$i = 0;
	foreach (@elements) {
		$islands{$_} = $Hislands[$HidToNumber{$HrankingID[$i]}];
		$ids{$_} = $islands{$_}->{'id'};
		$i++;
	}
	my $tuni = $islands{'uni'}->{'tuni'};
	my($kstwin, $kstdrow, $kstlose) = (split(/,/, $islands{'kachiten'}->{'eisei4'}))[3..5]; # 
	my($ktstwint, $ktstdrowt, $ktstloset) = (split(/,/, $islands{'kachitent'}->{'eisei4'}))[6..8]; # 
	my($rstwint, $rstdrowt, $rstloset) = (split(/,/, $islands{'shoritu'}->{'eisei4'}))[6..8]; # 
	my @bBeforeName = ('', '', '', '', '', '', '', '', '','', '合計', '', '', '', 'Lv', '', '', '合計', '', '');
	my @bAfterName = ("$HunitPop", "0$HunitPop規模", "0$HunitPop規模", "0$HunitPop規模", "$HunitTree", '万羽', '万頭', '万頭', "$HunitMonster","$HunitMonster", 'pts.', "$HunitPop", "種類/$tuniヶ所", 'ヶ所', "", "％($rstwint勝$rstloset敗$rstdrowt分)", "回", 'pts.', 'ｋｍ＋移動','万ｋＷ');

	out(<<END);
<DIV ID='Ranking'>
$HtempBack
<H1>各部門別NO.1</H1>
<P>
目指せ<B>ALL NO.1</B>！！クリックすると、<B>観光</B>することができます。
</P>
END

	foreach (0..$#elements) {
		my $id = $islands{$elements[$_]}->{'id'};
		my $name = $islands{$elements[$_]}->{'name'};
		my $element = $islands{$elements[$_]}->{$elements[$_]};

		out("<TABLE ALIGN=\"center\" width=\"100%\"><TR>\n") if(!($_ % 5));
		out(<<END);
<td width="9%">
<TABLE BORDER=1 width="100%">
<TR><TD class="RankingCell" ALIGN="center" COLSPAN="2">
<span class="bumon">${bumonName[$_]}NO.1</span></TD></TR>
END

		if(($element ne '') && ($element != 0)) {
			out(<<END);
<TR><TD ALIGN="center"><A STYlE="text-decoration:none" HREF="${HthisFile}?Sight=${id}" alt="ID=${id}" title="ID=${id}">${HtagName_}${name}島${H_tagName}</TD></TR>
<TR><TD ALIGN="center">${bBeforeName[$_]}${element}${bAfterName[$_]}</TD></TR>
</TABLE></TD>
END
		} else {
			out(<<END);
<TR><TD ALIGN="center">${HtagName_} - ${H_tagName}</TD></TR>
<TR><TD ALIGN="center"> - </TD></TR>
</TABLE></TD>
END
		}
		out("</TR></TABLE>\n") if(!(($_ + 1) % 5));
	}
	out("</TR></TABLE>\n") if((($#elements + 1) % 5));
	out("</DIV>\n");

}

sub visitMain{
        # 開放
        unlock();

        # テンプレート出力
        tempVisitPage();
}

sub tempVisitPage{

    # タイトル
    out(<<END);
${HtagTitle_}$Htitle${H_tagTitle}
END

    # デバッグモードなら「ターンを進める」ボタン
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="ターンを進める" NAME="TurnButton">
</FORM>
END
    }

    if ($HjavaModeSet eq 'java') {
		$radio = ""; $radio2 = "CHECKED";
	}else{
		$radio = "CHECKED";	$radio2 = "";
	}

        out(<<END);

<H1>${HtagHeader_}ターン$HislandTurn${H_tagHeader}</H1>

<HR>

<H1>${HtagHeader_}自分の島へ${H_tagHeader}</H1>
<SCRIPT language="JavaScript">
<!--
function newdevelope(){
//	newWindow = window.open("", "newWindow");
	document.Island.target = "newWindow"; 
	document.Island.submit();
}
function develope(){
	document.Island.target = "";
}
function MM_displayStatusMsg(msgStr) {
    window.status=msgStr;
}

function Navi(jj, img, title, title2) {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "visible";

		    StyElm.style.marginLeft = 0;
		    StyElm.style.marginTop = jj*102-170;

	    StyElm.innerHTML = "<table width=100%><tr><td class='M'><img class='NaviImg' src=" + img + "></td><td class='M'><div class='NaviText'><div class='NaviTitle'>" + title + " </div><hr>" + title2 + " </div></td></tr></table>";

}
function NaviClose() {
	StyElm = document.getElementById("NaviView");
	StyElm.style.visibility = "hidden";
}
//-->
</SCRIPT>
<FORM name="Island" action="$HthisFile" method="POST">
あなたの島の名前は？<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
パスワードをどうぞ！！<BR>
<INPUT TYPE="hidden" NAME="OwnerButton">
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $radio>通常モード
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $radio2>Javaスクリプトモード<BR>
<INPUT TYPE="submit" VALUE="開発しに行く" onClick="develope()">　
<INPUT TYPE="submit" VALUE="新しい画面" onClick="newdevelope()">
</FORM>

<HR>

END
    tempVisitPage2();
}

sub tempVisitPage2{

    my($mStr1) = '';

    $mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}資金${H_tagTH}</NOBR></TH>" if($HhideMoneyMode != 0);

	islandSort();

	my($loopInit) = $viewFirst;
	my($loopEnd) = $viewFirst + $viewNumber;
	$viewFirst = $loopInit = 0 if($viewFirst < 0);
	$loopEnd = $HislandNumber if($loopEnd > $HislandNumber);
	$loopEnd = $HislandNumber if($viewFlag eq 'ALL');
	my($first) = $loopInit + 1;

        out(<<END);

<DIV ID='islandView'><H1>${HtagHeader_}諸島の状況($first位～$loopEnd位)${H_tagHeader}</H1>

<P>
島の名前をクリックすると、<B>観光</B>することができます。
</P> 
END

	my($prev, $next, $nextCnt);
	if($viewFirst - $viewNumber < 0) {
	    $prev = 0;
	} else {
	    $prev = $viewFirst - $viewNumber;
	}
	if($viewFirst + $viewNumber >= $HislandNumber) {
	    $next = -1;
	} else {
	    $next = $viewFirst + $viewNumber;
	    $nextCnt = $viewNumber;
	    $nextCnt = $HislandNumber - $next if($next + $nextCnt > $HislandNumber);
	}
	if($viewFlag ne 'ALL') { # "全島表示"されているときは使わない
	    out("<FORM action=\"$HthisFile\" method=\"GET\">");
	    out("<INPUT TYPE=\"submit\" VALUE=\"前の$viewNumber島\" NAME=\"view$prev\">") if($next != $viewNumber);
	    out("<INPUT TYPE=\"submit\" VALUE=\"次の$nextCnt島\" NAME=\"view$next\">") if($next != -1);
	    out("<INPUT TYPE=\"submit\" VALUE=\"全表\示\" NAME=\"viewALL\">");
	    out("</form>");
	}
	out(<<END);

<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}順位${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}島${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}人口${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}面積${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}食料${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}農場${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}職場${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}採掘場${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}発電力${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}軍事技術${H_tagTH}</NOBR></TH>
</TR>
END

    my($island, $j, $farm, $factory, $mountain, $name, $id, $prize, $ii);
    my($pts);
    my($unemployed);
    my($rena);
    my($eis1, $eis2, $eis3);
    my($navinum) = 0;
    for($ii = $loopInit; $ii < $loopEnd; $ii++) {
	$j = $ii + 1;
	$island = $Hislands[$ii];
	$navinum++;

	$id = $island->{'id'};
	$farm = $island->{'farm'};
	$factory = $island->{'factory'};
	$mountain = $island->{'mountain'};
	$rena = $island->{'rena'};
	$renae = int($rena / 10 ) + 1;
	$pts = $island->{'pts'};
	$eisei2 = $island->{'eisei2'};
	$eisei2nd = int($eisei2 / 100 );
	$monsterlive = $island->{'monsterlive'};
        $unemployed = ($island->{'pop'} - ($farm + $factory + $mountain) * 10) / $island->{'pop'} * 100;
        $unemployed = '<span class="' . ($unemployed < 0 ? 'unemploy1' : 'unemploy2') . '">' . sprintf("%.2f%%", $unemployed) . '</span>';
	$farm = ($farm == 0) ? "保有せず" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "保有せず" : "${factory}0$HunitPop";
	$mountain = ($mountain == 0) ? "保有せず" : "${mountain}0$HunitPop";
        $HunitPts = 'pts.';
	$pts = ($pts == 0) ? "0" : "${pts}";
	$monsi = ($monsterlive == 0) ? "" : "${monsterlive}$HunitMonster";
	$monsm = ($monsterlive == 0) ? "" : "${monsterlive}$HunitMonster出現中!!";
	$rieki = ($island->{'pika'} < 0) ? "$island->{'pika'}$HunitMoney" : "＋$island->{'pika'}$HunitMoney";
	$zouka = ($island->{'hamu'} < 0) ? "$island->{'hamu'}$HunitPop" : "＋$island->{'hamu'}$HunitPop";
	$seicho = ($island->{'monta'} < 0) ? "$island->{'monta'}pts." : "＋$island->{'monta'}pts.";
	$eisei2 = ($eisei2nd == 0) ? "通算観光者数１万人未満<br>" : "通算観光者数${eisei2nd}万人<br>";

	$hcturn = int($HislandTurn/100)*100;

	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}島${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}島($island->{'absent'})${H_tagName2}";
	}

	my(@uniName) = ('[天使ミカエルor幸福の女神像]', '[首都]', '[壊れた侵略者]', '[王蟲の脱け殻]', '[闇石]', '[地石]', '[氷石]', '[風石]', '[炎石]', '[光石]', '[古代遺跡]', '[天空城or魔塔]');
	my(@uniData) = split(/,/, $island->{'eisei6'});
	my $unilist = '';
	$island->{'uni'} = 0;
	$island->{'tuni'} = 0;
	foreach (0..$#uniName) {
		$unilist .= "$uniName[$_]" if($uniData[$_] > 0);
		$island->{'tuni'} += $uniData[$_];
		$island->{'uni'}++ if($uniData[$_] > 0);
	}
        my($Complete,$Complete2) = ('', '');
        if($island->{'uni'} == $#uniName+1){
		$Complete ='Complete!!';
	} else{
		$Complete = "全12種類中$island->{'uni'}種類";
	}

	if ($island->{'uni'}) {
		$unique = "<span class='shuto'><IMG SRC=\"prize10.gif\" TITLE=\"入手の難しいユニーク地形：${unilist}／$Complete\" WIDTH=16 HEIGHT=16> $island->{'tuni'}ヶ所</span>";
	} else {
		$unique = "";
	}

	my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});
	my $force = $mshp+$msap+$msdp+$mssp;
	$island->{'force'} = $force;
	$mspet = "<IMG SRC=\"ms.gif\" ALT=\"マスコットいのら(HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe)\" WIDTH=16 HEIGHT=16>Sum($force)" if($mshp);
	$mspet = "<IMG SRC=\"tet.gif\" ALT=\"超神獣テトラ(HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin匹撃破/経験値$msexe)\" WIDTH=16 HEIGHT=16>Sum($force)" if($tet);
	$mspet = "" if(!$mshp && !$tet);

	# ＨＣ
	my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});
	$siaisu = $stwint + $stdrowt + $stloset;
	$siaisu = 1 if($siaisu == 0);
	$island->{'shoritu'} = int($stwint / $siaisu * 100);
	$island->{'teamforce'} = $sto + $std + $stk;
	$island->{'styusho'} = $styusho;
	$kachiten = $stwin*3 + $stdrow;

	my $nn = ('練習中', '予選第１戦待ち', '予選第２戦待ち', '予選第３戦待ち', '予選第４戦待ち', '予選終了待ち',	'準々決勝戦待ち', '準決勝戦待ち', '決勝戦待ち',
			'優勝！', '練習中', '予選落ち', '準々決勝負け', '準決勝負け', '第２位')[$stshoka];
    	$nn = '練習中' if($nn eq '');

	$ssss = "";
	$ssss = "<IMG SRC=\"sc.gif\" ALT=\"$nn(攻($sto)守($std)KP($stk)チーム成績(勝点$kachiten/$stwin勝$stlose敗$stdrow分/通算$stwint勝$stloset敗$stdrowt分/優勝$styusho回)\" WIDTH=16 HEIGHT=\"16\"> " if ($stshoka > 0);


	$island->{'ene'} = (split(/,/, $island->{'eisei3'}))[0];
	my(@ZA) = split(/,/, $island->{'etc6'});
	foreach(@ZA){
	    $island->{'monsfig'} += $_; # 怪獣の総数を算出 
	}
	$island->{'monsfig'} += $island->{'monsterlive'};
	
	# ランキング処理、RA JS ver4.47から移植＆アレンジ
		my @elements   = ( 'pop', 'farm', 'factory', 'mountain', 'fore', 'tare', 'zipro', 'leje', 'monsfig', 'taiji', 'force', 'eisei2', 'uni', 'kei', 'rena', 'shoritu', 'styusho', 'teamforce', 'etc0', 'ene');
		my @bumonName  = ('人口', '農場',  '職場',   '採掘場',  '森林', 'にわとり数', 'ぶた数', 'うし数',  '怪獣出現＆捕獲数', '怪獣退治数', '生物大学能力', '通算観光客', 'ユニーク地形数', '記念碑数', '軍事技術', 'HC通算勝率', 'HC優勝回数', 'サッカーチーム力', '鉄道', '電力');
		my $bumonCount = 0;
		my $bName = '';
		foreach (0..$#HrankingID) {
			my $rID = $HrankingID[$_];
			my $element = $island->{$elements[$_]};
			if(($island->{'id'} == $rID) && ($element ne '') && ($element != 0)) {
				$bumonCount++;
				$bName .= '[' . $bumonName[$_] . ']';
			}
		}
		my $bumons;
		if ($bumonCount) {
			$bumons = "<IMG SRC=\"prize11.gif\" ALT=\"部門賞：$bName\" WIDTH=16 HEIGHT=16>$bumonCount冠";
		} else {
			$bumons = "";
		}

	$prize = $island->{'prize'};
	my($flags, $monsters, $turns);
	$prize =~ /([0-9]*),([0-9]*),(.*)/;
	$flags = $1;
	$monsters= $2;
	$turns = $3;
	$prize = '';

        # ターン杯の表示
        my($alt);
        while($turns =~ s/([0-9]*),//) {
            $alt .= "$1${Hprize[0]} ";
        }
        $prize .= "<IMG SRC=\"prize0.gif\" ALT=\"$alt\" WIDTH=16 HEIGHT=16> " if ($alt ne '');

	# 名前に賞の文字を追加
	my($f) = 1;
	my($i);
	for($i = 1; $i < 10; $i++) {
	    if($flags & $f) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
	    }
	    $f = $f << 1;
	}

	# 倒した怪獣リスト
	$f = 1;
	my($max) = -1;
	my($mNameList) = '';
	for($i = 0; $i < $HmonsterNumber; $i++) {
	    if($monsters & $f) {
		$mNameList .= "[$HmonsterName[$i]] ";
		$max = $i;
	    }
	    $f = $f << 1;
	}
	if($max != -1) {
	    $prize .= "<IMG SRC=\"${HmonsterImage[$max]}\" ALT=\"$mNameList\" WIDTH=16 HEIGHT=16> $island->{'taiji'}$HunitMonster退治";
	}


        # 出現中の怪獣リスト
        $f = 1;
        $max = -1;
        $mNameList = '';
        my($monslivetype) = $island->{'monsterlivetype'};
        my($monsliveimg);
        for($i = 0; $i < $HmonsterNumber; $i++) {
            if($monslivetype & $f) {
                $mNameList .= "[$HmonsterName[$i]] ";
                $max = $i;
            }
	    $f = $f << 1;;
        }
        if($max != -1) {
            $monsliveimg = "<IMG SRC=\"${HmonsterImage[$max]}\" ALT=\"$mNameList\" WIDTH=16 HEIGHT=16> ";
        }


	my($mStr1) = '';
	if($HhideMoneyMode == 1) {
	    $mStr1 = "<TD $HbgInfoCell align=right nowrap=nowrap><NOBR>$island->{'money'}$HunitMoney</NOBR></TD>";
	} elsif($HhideMoneyMode == 2) {
	    my($mTmp) = aboutMoney($island->{'money'});
	    $mStr1 = "<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$mTmp</NOBR></TD>";
	}

	my($msjotai, $nokotan, $msid) = split(/,/, $island->{'etc7'});
	$HcurrentNumber = $HidToNumber{$msid};
	my($island) = $Hislands[$HcurrentNumber];
	$HcurrentName = $island->{'name'};

	$island = $Hislands[$ii];

	#ここから追加
	my($oStr) = '';
	if($island->{'onm'} eq ''){
	    $oStr = "<TD $HbgTotoCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagTH_}コメント : ${H_tagTH}$island->{'comment'}</NOBR></TD>";
	} elsif($msjotai == 1) {
	    $oStr = "<TD $HbgTotoCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagLbbsSS_}$island->{'onm'} : ${H_tagLbbsSS}<font color=red><B>$HcurrentName島への援助射撃許可を申\請中(残り$nokotanターン)</B></font></NOBR></TD>";
	} elsif($msjotai == 2) {
	    $oStr = "<TD $HbgTotoCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagLbbsSS_}$island->{'onm'} : ${H_tagLbbsSS}<font color=seagreen><B>$HcurrentName島への援助射撃が可\能\(残り$nokotanターン)</B></font></NOBR></TD>";
	} else {
	    $oStr = "<TD $HbgTotoCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagLbbsSS_}$island->{'onm'} : ${H_tagLbbsSS}$island->{'comment'}</NOBR></TD>";
	}
	#ここまで

	# 電気系
	my($ene, $shouhi, $sabun, $chikuden, $ene) = split(/,/, $island->{'eisei3'});
	$sabun = $ene-$shouhi;
	$sabun2 = "<font color=red>不足中！</font>" if ($sabun < 0);
	$sabun2 = "" if ($sabun >= 0);
	$eleinfo = "<IMG SRC=\"ele.gif\" ALT=\"使用状況(消費$shouhi万ｋＷ／過不足$sabun万ｋＷ)\" WIDTH=16 HEIGHT=\"16\">$sabun2";
	$island->{'ene'} = $ene;

	# 人工衛星打ち上げ
	my($me_sat) = "";
	$eis1 = $island->{'eis1'};
	$eis2 = $island->{'eis2'};
	$eis3 = $island->{'eis3'};
	$eis4 = $island->{'eis4'};
	$eis5 = $island->{'eis5'};
	$eis6 = $island->{'eis6'};
	$eis7 = $island->{'eis7'};
	$cstpop = int($eis7/100);
	$csten = $eis7%100+1;
	$me_sat .= "<IMG SRC=\"kisho.gif\" ALT=\"気象衛星\" WIDTH=16 HEIGHT=\"16\">$eis1%" if ($eis1 >= 1);
	$me_sat .= "<IMG SRC=\"kansoku.gif\" ALT=\"観測衛星\" WIDTH=16 HEIGHT=\"16\">$eis2%" if ($eis2 >= 1);
	$me_sat .= "<IMG SRC=\"geigeki.gif\" ALT=\"迎撃衛星\" WIDTH=16 HEIGHT=\"16\">$eis3%" if ($eis3 >= 1);
	$me_sat .= "<IMG SRC=\"gunji.gif\" ALT=\"軍事衛星\" WIDTH=16 HEIGHT=\"16\">$eis4%" if ($eis4 >= 1);	
	$me_sat .= "<IMG SRC=\"bouei.gif\" ALT=\"防衛衛星\" WIDTH=16 HEIGHT=\"16\">$eis5%" if ($eis5 >= 1);	
	$me_sat .= "<IMG SRC=\"ire.gif\" ALT=\"イレギュラー\" WIDTH=16 HEIGHT=\"16\">$eis6%" if ($eis6 >= 1);	
	$me_sat .= "<IMG SRC=\"cst.gif\" ALT=\"宇宙ステーション／$cstpop$HunitPop滞在\" WIDTH=16 HEIGHT=\"16\">$csten%" if ($eis7 >= 1);	
	$me_sat = "" if ($eis1 == 0 && $eis2 == 0 && $eis3 == 0 && $eis4 == 0 && $eis5 == 0 && $eis6 == 0 && $eis7 == 0);

	# 牧場系
	my($Farmcpc) = "";
	$Farmcpc .= "<IMG SRC=\"niwatori.gif\" ALT=\"にわとり\" WIDTH=16 HEIGHT=\"16\">$island->{'tare'}万羽" if ($island->{'tare'} > 0);	
	$Farmcpc .= "<IMG SRC=\"buta.gif\" ALT=\"ぶた\" WIDTH=16 HEIGHT=\"16\">$island->{'zipro'}万頭" if ($island->{'zipro'} > 0);
	$Farmcpc .= "<IMG SRC=\"ushi.gif\" ALT=\"うし\" WIDTH=16 HEIGHT=\"16\">$island->{'leje'}万頭" if ($island->{'leje'} > 0);

	my($toto1, $toto2, $toto3, $toto4, $toto5, $toto6, $toto7) = split(/,/, $island->{'etc8'});
	my $omamori = "";
	   $omamori = "<IMG SRC=\"omamori.gif\" ALT=\"toto的中回数($toto1)/お守り残数($toto2)\" WIDTH=16 HEIGHT=\"16\">残り($toto2)" if (($toto2 > 0)||($toto1 > 0));

	# 家
	my $house = "";
	my $eisei1 = $island->{'eisei1'};
	my $hlv;
	foreach (0..9) {
		$hlv = 9 - $_;
		last if(($pts > $HouseLevel[$hlv])||($hlv == 0));
	}
	if(($pts > $HouseLevel[9]) && 
	   ($uniData[1]>0) && ($uniData[2]>0) && ($uniData[3]>0) &&
	   ($uniData[5]>0) && ($uniData[6]>0) && ($uniData[7]>0) && 
	   ($uniData[8]>0) && ($uniData[10]>0) && ($uniData[11]>0) && ($toto2>0)) {
		if(($uniData[9]>0) || ($uniData[4]>0)) {
		$hlv = 11;
		$hlv = 10 if($uniData[4] >= $uniData[9]);
		}
	}

	my $onm = $island->{'onm'};
	my $n = ('の小屋', 'の簡易住宅', 'の住宅', 'の高級住宅', 'の豪邸', 'の大豪邸', 'の高級豪邸', 'の城', 'の巨城', 'の黄金城', 'の魔塔', 'の天空城')[$hlv];
	my $zeikin = int($island->{'pop'}*($hlv+1)*$eisei1/100);
	$house .= "<IMG SRC=\"house${hlv}.gif\" ALT=\"$onm$n\" WIDTH=16 HEIGHT=\"16\">税率$eisei1％($zeikin$HunitMoney)" if($eisei1 > 0);

	my $totoyoso2 = $island->{'totoyoso2'};
	$shutoname = "首都：$totoyoso2<br>" if($totoyoso2 == 0);
	$shutoname = "" if($totoyoso2 == 555);

	out(<<END);

<TR>
<TD $HbgNumberCell ROWSPAN=4 align=center nowrap=nowrap><NOBR>${HtagNumber_}$j${H_tagNumber}</NOBR></TD>
<TD $HbgNameCell ROWSPAN=4 align=left nowrap=nowrap>
<div id="NaviView"></div>
<center>
<A class="M" HREF="${HthisFile}?Sight=${id}" \"alt="ID=${id}">
$name
</A><br>
<span class="shuto"><font size="-1">$shutoname</font></span>
<NOBR>ID:(<span class="house"><B>$id</B></span>) <span class="point">$pts</span>$HunitPts</NOBR><br>
<NOBR><font size="-1">失業率</font>:($unemployed</span>)</NOBR><br>
<NOBR><span class="eisei"><font size="-1">$eisei2</font></span></NOBR>
<NOBR><span class="monsm"><font size="-2">(前ターン$seicho$zouka$rieki)</font></span></NOBR>

</center>
</TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
$mStr1
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$farm</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$factory</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$mountain</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$ene万ｋＷ</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>Ｌｖ$renae</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagtTH_}info：<font size="-1">$ssss$unique$house$monsliveimg<span class="monsm">$monsm</span>$mspet<span class="unemploy1">$Farmcpc</span><span class="eisei">$me_sat</span></font>$eleinfo${H_tagtTH}</NOBR></TD>
</TR>

<TR>
<TD $HbgCommentCell COLSPAN=5 align=left nowrap=nowrap><NOBR>${HtagtTH_}Prize：<font size="-1">$bumons$prize$omamori</font>${H_tagtTH}</NOBR></TD>
<TD $HbgTotoCell COLSPAN=4 align=left nowrap=nowrap><NOBR><font size="-1">${HtagtTH_}予\想１：${H_tagtTH}$island->{'eis8'}</font></NOBR></TD>
</TR>
<TR>
$oStr
</TR>

END
    }
	out(<<END);
</table>
</DIV>
END

}

sub styleMain {
    # 開放
    unlock();

    # テンプレート出力
    tempStylePage();
}

sub tempStylePage {

        out(<<END);
<DIV ID='changeInfo'>
$HtempBack
END

my($Hcssfflag);
if($HcssLine eq '' || $HcssLine eq $cssDir){
    $Hcssfflag = '<FONT COLOR=RED>未設定</FONT>';
} else {
    $Hcssfflag = $HcssLine;
}

   out(<<END);

<H1>${HtagHeader_}スタイルシートの設定${H_tagHeader}</H1>
<TABLE>
<TR>
<TD>スタイルシート設定の説明：<br>
設定したいスタイルシートを開き<br>
設定ボタンを押すと、適応されます。<br>
注意として、パス名に半角カナが入ってしまうと使用できないので、<br>
デスクトップには置けないと言う事です。<br>
つまり、参照ボタンを押した時、横のテキストエリアに入る文字列に、<br>
半角カナが混じっていると駄目なのです。<br>
もし半角カナが入ってしまったら、CSSファイルを別の場所に移動して下さい。<br>

</TD>
</TR>
</TABLE>
<br>

<TABLE>
<TR>
 <TD class=M>
現在の設定<B>[</b> ${Hcssfflag} <B>]</B>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="CSSLINE">
<INPUT TYPE="submit" VALUE="設定" name=CSSSET>
</form>

<form action=$HthisFile method=POST>
Macユーザー用<BR>
<INPUT TYPE=text NAME="CSSLINEMAC">
<INPUT TYPE="submit" VALUE="設定" name=CSSSET><BR>
<FONT SIZE=-1>Macの方は、こちらを使用して下さい。</FONT>
</form>

<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="CSSLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="設定を解除する" name=CSSSET>
</form>

 </TD>
</TR>
</TABLE>
</DIV>
END

}

1;
