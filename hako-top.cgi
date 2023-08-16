#----------------------------------------------------------------------
# ���돔�� ver2.30
# �g�b�v���W���[��(ver1.00)
# �g�p�����A�g�p���@���́Ahako-readme.txt�t�@�C�����Q��
#
# ���돔���̃y�[�W: http://www.bekkoame.ne.jp/~tokuoka/hakoniwa.html
#----------------------------------------------------------------------
#----------------------------------------------------------------------
# Hakoniwa R.A. ver030314
# ���C���X�N���v�g(���돔�� ver2.30)
# �g�p�����A�g�p���@���́Aread-renas.txt�t�@�C�����Q��
#
# KEI PAGE: http://www5b.biglobe.ne.jp/~k-e-i/
#----------------------------------------------------------------------


#----------------------------------------------------------------------
# �g�b�v�y�[�W���[�h
#----------------------------------------------------------------------
# ���C��
sub topPageMain {
    # �J��
    unlock();

    # �e���v���[�g�o��
    tempTopPage();
}

# ���C��
sub topPageMain {
	#�A�N�Z�X���O�擾
	if($HtopAxes) {
		axeslog();
	}
	# �J��
	unlock();
	# �e���v���[�g�o��
	tempTopPage(0);
}

sub topPageMainL {
	#�A�N�Z�X���O�擾
	if($HtopAxes) {
		axeslog();
	}
	# �J��
	unlock();
	# �e���v���[�g�o��
	tempTopPage(1);
}

sub topPageMainS {
	#�A�N�Z�X���O�擾
	if($HtopAxes) {
		axeslog();
	}
	# �J��
	unlock();
	# �e���v���[�g�o��
	tempTopPage(2);
}

#=============================================
#���A�N�Z�X���O�擾
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
	my $day = ('��','��','��','��','��','��','�y')[$wday];
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

# �g�b�v�y�[�W
sub tempTopPage {
    # �^�C�g��
    out(<<END);
${HtagTitle_}$Htitle${H_tagTitle}
END

    # �f�o�b�O���[�h�Ȃ�u�^�[����i�߂�v�{�^��
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="�^�[����i�߂�" NAME="TurnButton">
</FORM>
END
    }

    if ($HjavaModeSet eq 'java') {
		$radio = ""; $radio2 = "CHECKED";
	}else{
		$radio = "CHECKED";	$radio2 = "";
	}

    # �t�H�[��
    my($remain) = $HunitTime + $HislandLastTime - time;
    out(<<END);
<DIV ID='Turn'><H1>${HtagHeader_}�^�[��$HislandTurn${H_tagHeader}</H1></DIV>
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
	return "���̃^�[���܂Ŏc��" + hour + "����" + min + "��" + sec + "�b";
}
//-->
</SCRIPT>
<HR>
<table>

<TR>
 <TD class=M VALIGN=TOP WIDTH=400>
<DIV ID='myIsland'>
<H1>${HtagHeader_}�����̓���${H_tagHeader}</H1>
<SCRIPT language="JavaScript">
<!--
function newdevelope(){
//	newWindow = window.open("", "newWindow"); // ���ꂾ�ƂȂ����G���[��
	document.Island.target = "newWindow";  
	document.Island.submit();
}
function develope(){
	document.Island.target = "";
}
//-->
</SCRIPT>
<FORM name="Island" action="$HthisFile" method="POST">
���Ȃ��̓��̖��O�́H<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
�p�X���[�h���ǂ����I�I<BR>
<INPUT TYPE="hidden" NAME="OwnerButton">
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $radio>�ʏ탂�[�h
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $radio2>Java�X�N���v�g���[�h<BR>
<INPUT TYPE="submit" VALUE="�J�����ɍs��" onClick="develope()">�@
<INPUT TYPE="submit" VALUE="�V�������" onClick="newdevelope()">
</FORM>
</DIV>

END
my($Himfflag);
if($HimgLine eq '' || $HimgLine eq $imageDir){
    $Himfflag = '<FONT COLOR=RED>���ݒ�</FONT>';
} else {
    $Himfflag = $HimgLine;
}

   out(<<END);
</TD>

<TD class=M VALIGN=TOP WIDTH=500>
<DIV ID='localImage'>
<H1>${HtagHeader_}�摜�̃��[�J���ݒ�(����)${H_tagHeader}</H1>
���݂̐ݒ�<B>[</b> ${Himfflag} <B>]</B>
�@�@<A HREF=${imageExp} target=_BLANK><FONT SIZE=+1> �� �� </FONT></A>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="IMGLINE">
<INPUT TYPE="submit" VALUE="�ݒ�" name=IMGSET>
</form>

<table>
<TR>
 <TD class=M>
<form action=$HthisFile method=POST>
Mac���[�U�[�p<BR>
<INPUT TYPE=text NAME="IMGLINEMAC">
<INPUT TYPE="submit" VALUE="�ݒ�" name=IMGSET><BR>
<FONT SIZE=-1>Mac�̕��́A��������g�p���ĉ������B</FONT>
</form>
 </TD>
 <TD class=M>
<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="IMGLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="�ݒ����������" name=IMGSET>
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
<H1><A HREF="$baseDir/hako-main.cgi?Visit=">${HtagHeader_}���̓��Ɋό��֍s��${H_tagHeader}</A></H1>
END
}
    out(<<END);
<HR>
END
if($Loghtml){
    out(<<END);
<H1><A HREF="$htmlDir/hakolog0.html" target="_blank">${HtagHeader_}�ŋ߂̏o����${H_tagHeader}</A></H1>
END
} else{
    out(<<END);
<H1>${HtagHeader_}�ŋ߂̏o����${H_tagHeader}</H1>
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
<DIV ID='HistoryLog'><H1>${HtagHeader_}�����̋L�^${H_tagHeader}</H1>
<DIV style="overflow:auto; height:${HdivHeight}px; width:${HdivWidth}px;">
END
    historyPrint();
    out(<<END);
</DIV></DIV>
END
}

# �g�b�v�y�[�W�p���O�\��
sub logPrintTop {
    my($i);
    for($i = 0; $i < $HtopLogTurn; $i++) {
	logFilePrint($i, 0, 0);
    }
}

# Point���Ƀ\�[�g
sub islandSort {
    my($flag, $i, $tmp);

    # �l���������Ƃ��͒��O�̃^�[���̏��Ԃ̂܂�
    my @idx = (0..$#Hislands);
    @idx = sort { $Hislands[$b]->{'pts'} <=> $Hislands[$a]->{'pts'} || $a <=> $b } @idx;
    @Hislands = @Hislands[@idx];
}

# �L�^�t�@�C���\��
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
	out("<NOBR>${HtagNumber_}�^�[��${1}${H_tagNumber}�F${2}</NOBR><BR>\n");
    }
    close(HIN);
}

# Hakoniwa Cup���O�\��
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
	out("<NOBR>${HtagNumber_}�^�[��${1}${H_tagNumber}�F${2}</NOBR><BR>\n");
    }
    close(CIN);
}

sub rankingMain {
        # �J��
        unlock();

        # �e���v���[�g�o��
        tempRankingPage();
}

sub tempRankingPage{

      # hakoniwaRA JS ver4.47����ڐA
	my $i;
	for($i = 0; $i < $HislandNumber; $i++) {
		my $rena = $Hislands[$i]->{'rena'}; # �R����
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
		    $Hislands[$i]->{'monsfig'} += $_; # ���b�̑������Z�o 
		}
		$Hislands[$i]->{'monsfig'} += $Hislands[$i]->{'monsterlive'};

		foreach (split(/,/, $Hislands[$i]->{'eisei6'})) {
			$Hislands[$i]->{'tuni'} += $_;
			$Hislands[$i]->{'uni'}++ if($_ > 0);
		}
	}

	my @elements   = ( 'pop', 'farm', 'factory', 'mountain', 'fore', 'tare', 'zipro', 'leje', 'monsfig', 'taiji', 'force', 'eisei2', 'uni', 'kei', 'renae', 'shoritu', 'styusho', 'teamforce', 'etc0', 'ene');
	my $hcturn = int($HislandTurn/100) * 100;
	my @bumonName  = ('�l��', '�_��',  '�E��',   '�̌@��',  '�X��', '�ɂ�Ƃ萔', '�Ԃ���', '������',  '���b�o�����ߊl��', '���b�ގ���', '������w�\��', '�ʎZ�ό��q', '���j�[�N�n�`��', '�L�O�萔', '�R���Z�p', 'HC�ʎZ����', 'HC�D����', '�T�b�J�[�`�[����', '�S��', '�d��');
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
	my @bBeforeName = ('', '', '', '', '', '', '', '', '','', '���v', '', '', '', 'Lv', '', '', '���v', '', '');
	my @bAfterName = ("$HunitPop", "0$HunitPop�K��", "0$HunitPop�K��", "0$HunitPop�K��", "$HunitTree", '���H', '����', '����', "$HunitMonster","$HunitMonster", 'pts.', "$HunitPop", "���/$tuni����", '����', "", "��($rstwint��$rstloset�s$rstdrowt��)", "��", 'pts.', '�����{�ړ�','�����v');

	out(<<END);
<DIV ID='Ranking'>
$HtempBack
<H1>�e�����NO.1</H1>
<P>
�ڎw��<B>ALL NO.1</B>�I�I�N���b�N����ƁA<B>�ό�</B>���邱�Ƃ��ł��܂��B
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
<TR><TD ALIGN="center"><A STYlE="text-decoration:none" HREF="${HthisFile}?Sight=${id}" alt="ID=${id}" title="ID=${id}">${HtagName_}${name}��${H_tagName}</TD></TR>
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
        # �J��
        unlock();

        # �e���v���[�g�o��
        tempVisitPage();
}

sub tempVisitPage{

    # �^�C�g��
    out(<<END);
${HtagTitle_}$Htitle${H_tagTitle}
END

    # �f�o�b�O���[�h�Ȃ�u�^�[����i�߂�v�{�^��
    if($Hdebug == 1) {
        out(<<END);
<FORM action="$HthisFile" method="POST">
<INPUT TYPE="submit" VALUE="�^�[����i�߂�" NAME="TurnButton">
</FORM>
END
    }

    if ($HjavaModeSet eq 'java') {
		$radio = ""; $radio2 = "CHECKED";
	}else{
		$radio = "CHECKED";	$radio2 = "";
	}

        out(<<END);

<H1>${HtagHeader_}�^�[��$HislandTurn${H_tagHeader}</H1>

<HR>

<H1>${HtagHeader_}�����̓���${H_tagHeader}</H1>
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
���Ȃ��̓��̖��O�́H<BR>
<SELECT NAME="ISLANDID">
$HislandList
</SELECT><BR>
�p�X���[�h���ǂ����I�I<BR>
<INPUT TYPE="hidden" NAME="OwnerButton">
<INPUT TYPE="password" NAME="PASSWORD" VALUE="$HdefaultPassword" SIZE=32 MAXLENGTH=32><BR>
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=cgi $radio>�ʏ탂�[�h
<INPUT TYPE="radio" NAME=JAVAMODE VALUE=java $radio2>Java�X�N���v�g���[�h<BR>
<INPUT TYPE="submit" VALUE="�J�����ɍs��" onClick="develope()">�@
<INPUT TYPE="submit" VALUE="�V�������" onClick="newdevelope()">
</FORM>

<HR>

END
    tempVisitPage2();
}

sub tempVisitPage2{

    my($mStr1) = '';

    $mStr1 = "<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>" if($HhideMoneyMode != 0);

	islandSort();

	my($loopInit) = $viewFirst;
	my($loopEnd) = $viewFirst + $viewNumber;
	$viewFirst = $loopInit = 0 if($viewFirst < 0);
	$loopEnd = $HislandNumber if($loopEnd > $HislandNumber);
	$loopEnd = $HislandNumber if($viewFlag eq 'ALL');
	my($first) = $loopInit + 1;

        out(<<END);

<DIV ID='islandView'><H1>${HtagHeader_}�����̏�($first�ʁ`$loopEnd��)${H_tagHeader}</H1>

<P>
���̖��O���N���b�N����ƁA<B>�ό�</B>���邱�Ƃ��ł��܂��B
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
	if($viewFlag ne 'ALL') { # "�S���\��"����Ă���Ƃ��͎g��Ȃ�
	    out("<FORM action=\"$HthisFile\" method=\"GET\">");
	    out("<INPUT TYPE=\"submit\" VALUE=\"�O��$viewNumber��\" NAME=\"view$prev\">") if($next != $viewNumber);
	    out("<INPUT TYPE=\"submit\" VALUE=\"����$nextCnt��\" NAME=\"view$next\">") if($next != -1);
	    out("<INPUT TYPE=\"submit\" VALUE=\"�S�\\��\" NAME=\"viewALL\">");
	    out("</form>");
	}
	out(<<END);

<TABLE BORDER>
<TR>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}����${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�l��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�ʐ�${H_tagTH}</NOBR></TH>
$mStr1
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�H��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�_��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�E��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�̌@��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}���d��${H_tagTH}</NOBR></TH>
<TH $HbgTitleCell align=center nowrap=nowrap><NOBR>${HtagTH_}�R���Z�p${H_tagTH}</NOBR></TH>
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
	$farm = ($farm == 0) ? "�ۗL����" : "${farm}0$HunitPop";
	$factory = ($factory == 0) ? "�ۗL����" : "${factory}0$HunitPop";
	$mountain = ($mountain == 0) ? "�ۗL����" : "${mountain}0$HunitPop";
        $HunitPts = 'pts.';
	$pts = ($pts == 0) ? "0" : "${pts}";
	$monsi = ($monsterlive == 0) ? "" : "${monsterlive}$HunitMonster";
	$monsm = ($monsterlive == 0) ? "" : "${monsterlive}$HunitMonster�o����!!";
	$rieki = ($island->{'pika'} < 0) ? "$island->{'pika'}$HunitMoney" : "�{$island->{'pika'}$HunitMoney";
	$zouka = ($island->{'hamu'} < 0) ? "$island->{'hamu'}$HunitPop" : "�{$island->{'hamu'}$HunitPop";
	$seicho = ($island->{'monta'} < 0) ? "$island->{'monta'}pts." : "�{$island->{'monta'}pts.";
	$eisei2 = ($eisei2nd == 0) ? "�ʎZ�ό��Ґ��P���l����<br>" : "�ʎZ�ό��Ґ�${eisei2nd}���l<br>";

	$hcturn = int($HislandTurn/100)*100;

	if($island->{'absent'}  == 0) {
		$name = "${HtagName_}$island->{'name'}��${H_tagName}";
	} else {
	    $name = "${HtagName2_}$island->{'name'}��($island->{'absent'})${H_tagName2}";
	}

	my(@uniName) = ('[�V�g�~�J�G��or�K���̏��_��]', '[��s]', '[��ꂽ�N����]', '[��峂̒E���k]', '[�Ő�]', '[�n��]', '[�X��]', '[����]', '[����]', '[����]', '[�Ñ���]', '[�V���or����]');
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
		$Complete = "�S12��ޒ�$island->{'uni'}���";
	}

	if ($island->{'uni'}) {
		$unique = "<span class='shuto'><IMG SRC=\"prize10.gif\" TITLE=\"����̓�����j�[�N�n�`�F${unilist}�^$Complete\" WIDTH=16 HEIGHT=16> $island->{'tuni'}����</span>";
	} else {
		$unique = "";
	}

	my($mshp, $msap, $msdp, $mssp, $mswin, $msexe, $tet) = split(/,/, $island->{'eisei5'});
	my $force = $mshp+$msap+$msdp+$mssp;
	$island->{'force'} = $force;
	$mspet = "<IMG SRC=\"ms.gif\" ALT=\"�}�X�R�b�g���̂�(HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe)\" WIDTH=16 HEIGHT=16>Sum($force)" if($mshp);
	$mspet = "<IMG SRC=\"tet.gif\" ALT=\"���_�b�e�g��(HP$mshp.AP$msap.DP$msdp.SP$mssp/$mswin�C���j/�o���l$msexe)\" WIDTH=16 HEIGHT=16>Sum($force)" if($tet);
	$mspet = "" if(!$mshp && !$tet);

	# �g�b
	my($sto, $std, $stk, $stwin, $stdrow, $stlose, $stwint, $stdrowt, $stloset, $styusho, $stshoka) = split(/,/, $island->{'eisei4'});
	$siaisu = $stwint + $stdrowt + $stloset;
	$siaisu = 1 if($siaisu == 0);
	$island->{'shoritu'} = int($stwint / $siaisu * 100);
	$island->{'teamforce'} = $sto + $std + $stk;
	$island->{'styusho'} = $styusho;
	$kachiten = $stwin*3 + $stdrow;

	my $nn = ('���K��', '�\�I��P��҂�', '�\�I��Q��҂�', '�\�I��R��҂�', '�\�I��S��҂�', '�\�I�I���҂�',	'���X������҂�', '��������҂�', '������҂�',
			'�D���I', '���K��', '�\�I����', '���X��������', '����������', '��Q��')[$stshoka];
    	$nn = '���K��' if($nn eq '');

	$ssss = "";
	$ssss = "<IMG SRC=\"sc.gif\" ALT=\"$nn(�U($sto)��($std)KP($stk)�`�[������(���_$kachiten/$stwin��$stlose�s$stdrow��/�ʎZ$stwint��$stloset�s$stdrowt��/�D��$styusho��)\" WIDTH=16 HEIGHT=\"16\"> " if ($stshoka > 0);


	$island->{'ene'} = (split(/,/, $island->{'eisei3'}))[0];
	my(@ZA) = split(/,/, $island->{'etc6'});
	foreach(@ZA){
	    $island->{'monsfig'} += $_; # ���b�̑������Z�o 
	}
	$island->{'monsfig'} += $island->{'monsterlive'};
	
	# �����L���O�����ARA JS ver4.47����ڐA���A�����W
		my @elements   = ( 'pop', 'farm', 'factory', 'mountain', 'fore', 'tare', 'zipro', 'leje', 'monsfig', 'taiji', 'force', 'eisei2', 'uni', 'kei', 'rena', 'shoritu', 'styusho', 'teamforce', 'etc0', 'ene');
		my @bumonName  = ('�l��', '�_��',  '�E��',   '�̌@��',  '�X��', '�ɂ�Ƃ萔', '�Ԃ���', '������',  '���b�o�����ߊl��', '���b�ގ���', '������w�\��', '�ʎZ�ό��q', '���j�[�N�n�`��', '�L�O�萔', '�R���Z�p', 'HC�ʎZ����', 'HC�D����', '�T�b�J�[�`�[����', '�S��', '�d��');
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
			$bumons = "<IMG SRC=\"prize11.gif\" ALT=\"����܁F$bName\" WIDTH=16 HEIGHT=16>$bumonCount��";
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

        # �^�[���t�̕\��
        my($alt);
        while($turns =~ s/([0-9]*),//) {
            $alt .= "$1${Hprize[0]} ";
        }
        $prize .= "<IMG SRC=\"prize0.gif\" ALT=\"$alt\" WIDTH=16 HEIGHT=16> " if ($alt ne '');

	# ���O�ɏ܂̕�����ǉ�
	my($f) = 1;
	my($i);
	for($i = 1; $i < 10; $i++) {
	    if($flags & $f) {
		$prize .= "<IMG SRC=\"prize${i}.gif\" ALT=\"${Hprize[$i]}\" WIDTH=16 HEIGHT=16> ";
	    }
	    $f = $f << 1;
	}

	# �|�������b���X�g
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
	    $prize .= "<IMG SRC=\"${HmonsterImage[$max]}\" ALT=\"$mNameList\" WIDTH=16 HEIGHT=16> $island->{'taiji'}$HunitMonster�ގ�";
	}


        # �o�����̉��b���X�g
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

	#��������ǉ�
	my($oStr) = '';
	if($island->{'onm'} eq ''){
	    $oStr = "<TD $HbgTotoCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagTH_}�R�����g : ${H_tagTH}$island->{'comment'}</NOBR></TD>";
	} elsif($msjotai == 1) {
	    $oStr = "<TD $HbgTotoCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagLbbsSS_}$island->{'onm'} : ${H_tagLbbsSS}<font color=red><B>$HcurrentName���ւ̉����ˌ�����\\����(�c��$nokotan�^�[��)</B></font></NOBR></TD>";
	} elsif($msjotai == 2) {
	    $oStr = "<TD $HbgTotoCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagLbbsSS_}$island->{'onm'} : ${H_tagLbbsSS}<font color=seagreen><B>$HcurrentName���ւ̉����ˌ�����\�\\(�c��$nokotan�^�[��)</B></font></NOBR></TD>";
	} else {
	    $oStr = "<TD $HbgTotoCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagLbbsSS_}$island->{'onm'} : ${H_tagLbbsSS}$island->{'comment'}</NOBR></TD>";
	}
	#�����܂�

	# �d�C�n
	my($ene, $shouhi, $sabun, $chikuden, $ene) = split(/,/, $island->{'eisei3'});
	$sabun = $ene-$shouhi;
	$sabun2 = "<font color=red>�s�����I</font>" if ($sabun < 0);
	$sabun2 = "" if ($sabun >= 0);
	$eleinfo = "<IMG SRC=\"ele.gif\" ALT=\"�g�p��(����$shouhi�����v�^�ߕs��$sabun�����v)\" WIDTH=16 HEIGHT=\"16\">$sabun2";
	$island->{'ene'} = $ene;

	# �l�H�q���ł��グ
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
	$me_sat .= "<IMG SRC=\"kisho.gif\" ALT=\"�C�ۉq��\" WIDTH=16 HEIGHT=\"16\">$eis1%" if ($eis1 >= 1);
	$me_sat .= "<IMG SRC=\"kansoku.gif\" ALT=\"�ϑ��q��\" WIDTH=16 HEIGHT=\"16\">$eis2%" if ($eis2 >= 1);
	$me_sat .= "<IMG SRC=\"geigeki.gif\" ALT=\"�}���q��\" WIDTH=16 HEIGHT=\"16\">$eis3%" if ($eis3 >= 1);
	$me_sat .= "<IMG SRC=\"gunji.gif\" ALT=\"�R���q��\" WIDTH=16 HEIGHT=\"16\">$eis4%" if ($eis4 >= 1);	
	$me_sat .= "<IMG SRC=\"bouei.gif\" ALT=\"�h�q�q��\" WIDTH=16 HEIGHT=\"16\">$eis5%" if ($eis5 >= 1);	
	$me_sat .= "<IMG SRC=\"ire.gif\" ALT=\"�C���M�����[\" WIDTH=16 HEIGHT=\"16\">$eis6%" if ($eis6 >= 1);	
	$me_sat .= "<IMG SRC=\"cst.gif\" ALT=\"�F���X�e�[�V�����^$cstpop$HunitPop�؍�\" WIDTH=16 HEIGHT=\"16\">$csten%" if ($eis7 >= 1);	
	$me_sat = "" if ($eis1 == 0 && $eis2 == 0 && $eis3 == 0 && $eis4 == 0 && $eis5 == 0 && $eis6 == 0 && $eis7 == 0);

	# �q��n
	my($Farmcpc) = "";
	$Farmcpc .= "<IMG SRC=\"niwatori.gif\" ALT=\"�ɂ�Ƃ�\" WIDTH=16 HEIGHT=\"16\">$island->{'tare'}���H" if ($island->{'tare'} > 0);	
	$Farmcpc .= "<IMG SRC=\"buta.gif\" ALT=\"�Ԃ�\" WIDTH=16 HEIGHT=\"16\">$island->{'zipro'}����" if ($island->{'zipro'} > 0);
	$Farmcpc .= "<IMG SRC=\"ushi.gif\" ALT=\"����\" WIDTH=16 HEIGHT=\"16\">$island->{'leje'}����" if ($island->{'leje'} > 0);

	my($toto1, $toto2, $toto3, $toto4, $toto5, $toto6, $toto7) = split(/,/, $island->{'etc8'});
	my $omamori = "";
	   $omamori = "<IMG SRC=\"omamori.gif\" ALT=\"toto�I����($toto1)/�����c��($toto2)\" WIDTH=16 HEIGHT=\"16\">�c��($toto2)" if (($toto2 > 0)||($toto1 > 0));

	# ��
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
	my $n = ('�̏���', '�̊ȈՏZ��', '�̏Z��', '�̍����Z��', '�̍��@', '�̑卋�@', '�̍������@', '�̏�', '�̋���', '�̉�����', '�̖���', '�̓V���')[$hlv];
	my $zeikin = int($island->{'pop'}*($hlv+1)*$eisei1/100);
	$house .= "<IMG SRC=\"house${hlv}.gif\" ALT=\"$onm$n\" WIDTH=16 HEIGHT=\"16\">�ŗ�$eisei1��($zeikin$HunitMoney)" if($eisei1 > 0);

	my $totoyoso2 = $island->{'totoyoso2'};
	$shutoname = "��s�F$totoyoso2<br>" if($totoyoso2 == 0);
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
<NOBR><font size="-1">���Ɨ�</font>:($unemployed</span>)</NOBR><br>
<NOBR><span class="eisei"><font size="-1">$eisei2</font></span></NOBR>
<NOBR><span class="monsm"><font size="-2">(�O�^�[��$seicho$zouka$rieki)</font></span></NOBR>

</center>
</TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$island->{'pop'}$HunitPop</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$island->{'area'}$HunitArea</NOBR></TD>
$mStr1
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$island->{'food'}$HunitFood</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$farm</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$factory</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$mountain</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>$ene�����v</NOBR></TD>
<TD $HbgPoinCell align=right nowrap=nowrap><NOBR>�k��$renae</NOBR></TD>
</TR>
<TR>
<TD $HbgCommentCell COLSPAN=9 align=left nowrap=nowrap><NOBR>${HtagtTH_}info�F<font size="-1">$ssss$unique$house$monsliveimg<span class="monsm">$monsm</span>$mspet<span class="unemploy1">$Farmcpc</span><span class="eisei">$me_sat</span></font>$eleinfo${H_tagtTH}</NOBR></TD>
</TR>

<TR>
<TD $HbgCommentCell COLSPAN=5 align=left nowrap=nowrap><NOBR>${HtagtTH_}Prize�F<font size="-1">$bumons$prize$omamori</font>${H_tagtTH}</NOBR></TD>
<TD $HbgTotoCell COLSPAN=4 align=left nowrap=nowrap><NOBR><font size="-1">${HtagtTH_}�\\�z�P�F${H_tagtTH}$island->{'eis8'}</font></NOBR></TD>
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
    # �J��
    unlock();

    # �e���v���[�g�o��
    tempStylePage();
}

sub tempStylePage {

        out(<<END);
<DIV ID='changeInfo'>
$HtempBack
END

my($Hcssfflag);
if($HcssLine eq '' || $HcssLine eq $cssDir){
    $Hcssfflag = '<FONT COLOR=RED>���ݒ�</FONT>';
} else {
    $Hcssfflag = $HcssLine;
}

   out(<<END);

<H1>${HtagHeader_}�X�^�C���V�[�g�̐ݒ�${H_tagHeader}</H1>
<TABLE>
<TR>
<TD>�X�^�C���V�[�g�ݒ�̐����F<br>
�ݒ肵�����X�^�C���V�[�g���J��<br>
�ݒ�{�^���������ƁA�K������܂��B<br>
���ӂƂ��āA�p�X���ɔ��p�J�i�������Ă��܂��Ǝg�p�ł��Ȃ��̂ŁA<br>
�f�X�N�g�b�v�ɂ͒u���Ȃ��ƌ������ł��B<br>
�܂�A�Q�ƃ{�^�������������A���̃e�L�X�g�G���A�ɓ��镶����ɁA<br>
���p�J�i���������Ă���ƑʖڂȂ̂ł��B<br>
�������p�J�i�������Ă��܂�����ACSS�t�@�C����ʂ̏ꏊ�Ɉړ����ĉ������B<br>

</TD>
</TR>
</TABLE>
<br>

<TABLE>
<TR>
 <TD class=M>
���݂̐ݒ�<B>[</b> ${Hcssfflag} <B>]</B>
<form action=$HthisFile method=POST>
<INPUT TYPE=file NAME="CSSLINE">
<INPUT TYPE="submit" VALUE="�ݒ�" name=CSSSET>
</form>

<form action=$HthisFile method=POST>
Mac���[�U�[�p<BR>
<INPUT TYPE=text NAME="CSSLINEMAC">
<INPUT TYPE="submit" VALUE="�ݒ�" name=CSSSET><BR>
<FONT SIZE=-1>Mac�̕��́A��������g�p���ĉ������B</FONT>
</form>

<form action=$HthisFile method=POST>
<INPUT TYPE=hidden NAME="CSSLINE" value="deletemodenow">
<INPUT TYPE="submit" VALUE="�ݒ����������" name=CSSSET>
</form>

 </TD>
</TR>
</TABLE>
</DIV>
END

}

1;
