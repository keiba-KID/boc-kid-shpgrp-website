#!/usr/bin/perl

#----------------------------------------------------------------------
#	 ���ڂ����o�g�����C���� ver 1.17 (Free)
#	 �����	: Alpha-kou.
#	 E-MAIL	: dabo@dabo.design.co.jp
#	 URL	: http://D-BR.net/
#
#        ������	: �S�[�h��
#        E-MAIL	: zaza99jp@yahoo.co.jp
#	 URL	: http://godon.bbzone.net/
#
# �g�p�O�ɂ܂����p�K���ǂ�ł�������
#	http://D-BR.net/kitei.html
#       http://godon.bbzone.net/kitei.html
# [���̃X�N���v�g���g�p���ċN���������Ȃ鑹�Q�ɂ��ӔC�͕����܂���B]
#----------------------------------------------------------------------

$| = 1;
require './jcode.pl';

########## ���[�J���ϐ��w��
sub kankyou{

# �N�b�L�[���擾
        &get_cookie;

# �����e
        $mente = 0;     # �����e�̎���1��
        $mentecom = '�����e���Ă܂��B';  #�����e���̃R�����g

# ��{�ݒ�

	$cgifile = './uma5.cgi';	# ���̃t�@�C����
	$logfile = './chara.dat';	# �n�o�^�t�@�C��
        $time2file = './time2.dat';	# ���[�O���ԋL�^�t�@�C��
	$fightfile = './fightlog.dat';	# �O�̎����̋L�^�t�@�C��
        $commentfile = './comment.dat';	# �R�����g�t�@�C��
        $cntfile = './count.dat';       # �J�E���^�t�@�C��
        $orfile = './orank.dat';	# �I�[�i�[�����L���O�t�@�C��
        $tanefile = './tane.dat';	# �퉲�n�t�@�C��
        $tamefile = './tame.dat';	# �ɐB�Ĕn�t�@�C��
        $syurankfile = './syurank.dat';	# �퉲�n�����L���O�t�@�C��
        $mesrankfile = './mesrank.dat';	# �ɐB�Ĕn�����L���O�t�@�C��
        $winfile = './win.dat';         # �`�����s�I���t�@�C��
        $lockfile = './lock.dat';         # ���b�N�t�@�C��
        $pastfile = './past.dat';         # ���D���n�t�@�C��
        $recordsfile = './record.dat';    # ���R�[�h�t�@�C��
        $backupfile = './backup.dat';    # �o�b�N�A�b�v�t�@�C��
        $gaisenfile = './gaisen.dat';    # �M����ܔn�t�@�C��
        $gaifightfile = './gaifight.dat';    # �M����܌��ʃt�@�C��
        $kisyufile = './kisyu.dat';    # �R��t�@�C��

	$method = 'POST';	# GET or POST���w��
	$max_chara = '100';	# �o�^�n�̍ő吔
	$max_fight = '3';	# �킢�̋L�^�̍ő吔
        $max_jyoui = '7';	# �s�n�o�ɕ\�������ʔn�̓���
        $jyouiga = '0';         # �s�n�o�ɕ\�������ʔn�ɉ����ڂ܂ŃA�C�R����\�����邩

	$title = '���ˋ��n���[�O';	# �s�n�o�y�[�W�ɕ\�������^�C�g��
	$title2 = '���ˋ��n���[�O';	# �u���E�U�ɕ\�������^�C�g��
	$acomment = '';		        # �^�C�g�����̃R�����g�i�^�O�\�j
	$url = '';                      # �z�[���y�[�W�̂t�q�k

	$nameleng = '9';	# ���O�̒�����S�p�������܂łɂ��邩�B�i�n�j
        $nameleng2 = '5';      # ���O�̒�����S�p�������܂łɂ��邩�B�i�l�j

# �y�[�W�S�́i�ϐ��̖��O��body�^�O���̂܂܂ł��B�j

	$bgcolor = 'ffffff';    # default:ffffff     # �w�i�F
	$text = '000000';       # default:000000
	$link = '0000CD';       # default:0000CD
	$vlink = '6699FF';      # default:6699FF
	$alink = '303030';      # default:303030
        $iroformwaku = 'green'; # �t�H�[���{�^������̐F
	$background = '';       # �w�i�摜
        $backgaisenmon = '';    # �M���厞�̔w�i�摜
        $ncolor = 'green';      # �j���[�X���̃R�����g�̐F
        $news = '�j���[�X';     # �j���[�X���̃^�C�g��
        $counter = '0';         # �J�E���^�[��ݒu���邩�i0:���Ȃ��A1:����j

	$tcolor = '#FF4500';	# �^�C�g���̐F
	$tsize = '6';		# �^�C�g���T�C�Y
        $bbs_name  = '';	# �f���̖��O
	$bbs_url  = '';         # �f���̂t�q�k

# �Q�[���o�����X���ݒ�
        $ktime     = '5';    # �����̕ς�鎞��(0�`23)
        $racemax   = '50';   # �P�V�[�Y�������[�X��
        $racemax2  = $racemax - 1;
        $playday   =  '7';   # �P�V�[�Y���������i���j
        $kankaku   =  '3';   # ���[�X�Ԋu�i���j
        $max_com   = '10';   # �R�����g�̍ő吔
        $max_zi    = '35';   # �R�����g�̍ő厚��
        $taneosu   = '35';   # ���͉����ȏ�Ŏ퉲�n�ɂȂ邩�B
        $tanemesu  = '30';   # �Ă͉����ȏ�ŔɐB�Ĕn�ɂȂ邩�B
        $osuintai  = '25';   # �퉲�n�͉��΂Ŏ퉲�n�����ނ��邩�B
        $mesuintai = '15';   # �ɐB�Ĕn�͉��΂ŔɐB�Ĕn�����ނ��邩�B
        $shyoka    = '2';    # ���[�O�����ڂ��琢��]����\�����邩�B
        $iconuse   = '0';    # �A�C�R�����g�p���邩�i0:���Ȃ��A1:����j
        $imgurl    = '';     # �e���t�@���_�̐�΃p�X�i�Ō�� / �͕K�v����܂���B�j

# �A�C�R�����X�g
        @icon1 = ('one','two');#�A�C�R���̃t�@�C����(.gif�͏����Ȃ��ėǂ��ł��B)

        @icon2 = ('�P��','�Q��');#�A�C�R����

# �j�b�N�X(�オ�퉲�n�A�����ɐB�Ĕn�̌����̎��j�b�N�X)�A��)�G���o�W�F�ƃO���C�\������
# �퉲�n�E�ɐB�Ĕn�̋�ʂ��Ȃ����ɂ͏�Ɖ��𔽑΂ɂ������̂������K�v������܂��B
#(�X�s�[�h)

        @spo = ('�G���o�W�F','�G���o�W�F','�O���C�\������','�{�����Z��','�_���e','�_���e','�m�[�U���_���T�[','�v�����X���[�M�t�g','�m�[�U���_���T�[','�e�f�B','�l�C�e�B���_���T�[','�m�[�U���_���T�[','�{�[���h���[���[','�n�C�y���I��','�}���m�E�H�[','�t�@�C���g�b�v','�j�W���X�L�[','�m�[�U���_���T�[');
        @spm = ('�O���C�\������','�{�����Z��','�G���o�W�F','�G���o�W�F','�m�[�U���_���T�[','�v�����X���[�M�t�g','�_���e','�_���e','�e�f�B','�m�[�U���_���T�[','�m�[�U���_���T�[','�l�C�e�B���_���T�[','�n�C�y���I��','�{�[���h���[���[','�t�@�C���g�b�v','�}���m�E�H�[','�m�[�U���_���T�[','�j�W���X�L�[');

#(�u����)

        @syo = ('�p�[�\����','�{�����Z��','�l���@�[�x���h','�p�[�\����','�j�W���X�L�[','�j�W���X�L�[','�j�W���X�L�[','���b�h�S�b�h','���C�Y�A�l�C�e�B��','�l���@�[�x���h','�m�[�U���_���T�[','�m�[�U���_���T�[','�m�[�U���_���T�[','�m�[�U���_���T�[','���b�h�S�b�h','���{�[','�n�C�y���I��','�w�C���g�D���[�Y��');
        @sym = ('�{�����Z��','�p�[�\����','�p�[�\����','�l���@�[�x���h','�l���@�[�x���h','���C�Y�A�l�C�e�B��','���b�h�S�b�h','�j�W���X�L�[','�j�W���X�L�[','�j�W���X�L�[','���b�h�S�b�h','���{�[','�n�C�y���I��','�w�C���g�D���[�Y��','�m�[�U���_���T�[','�m�[�U���_���T�[','�m�[�U���_���T�[','�m�[�U���_���T�[');

$body = "<body bgcolor=\"$bgcolor\" text=\"$text\" alink=\"$alink\" link=\"$link\" vlink=\"$vlink\" background=\"$background\">";

}#end kankyou

srand( time() ^ ( $$ + ( $$ << 15)) );

&kankyou;
&decode;
&readlog;

# �ΐ폈��
         if($form{'race'} && $lines[1]){require './uma_race.cgi';&syori;&fight;exit;}
# �o�^����
	 if($form{'record'}) {require './uma_umu.cgi';&record;&rec;exit;}
         if($form{'no'}){require './uma_race.cgi';&fight;exit;}
         if($form{'rule'}){&rule;exit;}
         if($form{'rec'}){require './uma_umu.cgi';&seisan;&rec;exit;}
         if($form{'log'}){&log;exit;}
         if($form{'comment'}){&comsyori;}
         if($form{'orank'}){require './uma_rank.cgi';&orank;exit;}
         if($form{'syurank'}){require './uma_rank.cgi';&syurank;exit;}
         if($form{'mode'} eq 'chara' || $form{'chara'}){&chara;exit;}
         if($form{'mode'} eq 'hinba' || $form{'hinba'}){&hinba;exit;}
         if($form{'login'}){&login;exit;}
         if($form{'itiran'}){&itiran;exit;}
         if($form{'mode'} eq 'icon'){&icon;exit;}
         if($form{'mode'} eq 'ketou'){require './uma_umu.cgi';&ketou;exit;}
         if($form{'mode'} eq 'mketou'){require './uma_umu.cgi';&mketou;exit;}
         if($form{'past'}){require './uma_rank.cgi';&past;exit;}
         if($form{'rtime'}){require './uma_rank.cgi';&rtime;exit;}
         if($form{'nameda'}){require './uma_umu.cgi';&umaname;&rec;exit;}
     if($form{'kisyu'} || $form{'mode'} eq 'kisyu'){require './uma_rank.cgi';&kisyu;exit;}
         
&html;
exit;

##### �f�R�[�h�����[�J���ϐ��֎󂯓n��
sub decode{

#���͂��ꂽ�l���f�R�[�h
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
        $value =~ s/ //g;
        $value =~ s/�@//g;
	$form{$key} = $value;
	}

}#end decode

##### ���O�ǂݍ���
sub readlog{
	open(DB,"$logfile");
	seek(DB,0,0);  @lines = <DB>;  close(DB);
	
	($lno, $lname, $lsakusya, $lhomepage, $llif, $lpow, $ldef, $lspe, $ldate, $lip, $licon, $lwin, $lsyu, $ltotal, $ltyoushi, $lashi, $losu, $lmesu, $lsei, $lketou, $lbaku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$lines[0]);

	open(TM,"$timefile");
	seek(TM,0,0);  @times = <TM>;  close(TM);

# ���Ԃ̎擾

        $times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

###### ���[�O�����̍X�V
        if($ktime >= 24 || $ktime < 0){$ktime=5;}
        open(ST,"$time2file");
	seek(ST,0,0);  @st = <ST>;  close(ST);
        $hour = int(sprintf("%02d",$hour));
        $day = sprintf("%02d",$mday);
        $playdays = $playday + 1;
        ($hiniti, $hi, $zikan, $rigu, $sedai) = split(/<>/, @st[0]);
      if((($hi < $day || $hi - $day > 20) && $hour >= $ktime) || (abs($hi - $day) >= 2 && abs($hi - $day) <= 20)){
        $hiniti++;
        &backup;
      if($hiniti == $playdays){&koushin;$hiniti=1;$rigu++;$sedai=0;}    # ���[�O�X�V����
        $zikann = "$hiniti<>$day<>$hour<>$rigu<>$sedai<>";
        open(ST,">$time2file") ;
		eval 'flock(ST,2);';
		seek(ST,0,0);	print ST $zikann;
		eval 'flock(ST,8);';
	close(ST);
      }

}#end 

sub backup{      # �P���P��o�b�N�A�b�v����

        open(LL,"$logfile");
	seek(LL,0,0);  @ll = <LL>;  close(LL);

        open(BK,"$backupfile");
	seek(BK,0,0);  @bk = <BK>;  close(BK);

        if($#ll >= $#bk){
        open(BK,">$backupfile") ;
        eval 'flock(BK,2);';
	seek(BK,0,0);	print BK @ll;
	eval 'flock(BK,8);';
        close(BK);
        }
}#end backup

##### �R�����g�L������
sub comsyori{

         # �����[�g�z�X�g�擾
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

	if(length($form{'comtext'}) < 1 || length($form{'comtext'}) > $max_zi * 2){&error("������$max_zi���܂łł��B");}

        $year += 1900;
	$month = sprintf("%02d",$mon +1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$ljikan = "$month/$mday $hour:$min";

	open(CF,"+<$commentfile") || &error("�w�肳�ꂽ�t�@�C�����J���܂���B");
	eval 'flock(CF,2);';

	@comments = <CF>;

        foreach $line (@comments) {
        &jcode'convert(*line,'sjis');
        local($comm, $host, $name, $time, $kekka) = split(/<>/,$line);
        if($comm eq $form{'comtext'}){&error("���łɓ����������݂�����܂��B");}
        if($time eq $ljikan){&error("�����������Ԃ������ď�������ŉ������B");}
        }

        $comkati = $form{'comkati'};
        $commake = $form{'commake'};
        $comsa = $form{'comsa'};
        $comuma = $form{'comuma'};
        if($comkati eq $comuma){
        $kekka = "$comkati ��-$comsa-�� $commake";
        }elsif($commake eq $comuma){
        $kekka = "$commake ��-$comsa-�� $comkati";
        }
        if($comkati eq ""){$kekka = "";}
        if($form{'comname'} eq "�O�l"){
        $kakiko = "$form{'comtext'}<>$host<>�M����܌���<>$ljikan<>$kekka<>\n";
        }else{
	$kakiko = "$form{'comtext'}<>$host<>$form{'comname'}<>$ljikan<>$kekka<>\n";
        }
	unshift(@comments, $kakiko);
	splice(@comments, $max_com);

        truncate (CF, 0); 
	seek(CF,0,0);	print CF @comments;
	close(CF);
	eval 'flock(CF,8);';

}#end comsyori

#####���쌠�\��

sub chosaku{
&secretcopyright;

print <<"_HTML2_";

<div align="center">
<form action="$cgifile" method="$method">
<table cellpadding="5"><tr><td bgcolor="$iroformwaku">
<center><input type="submit" value="�g�b�v�y�[�W">
<input type="submit" name="rec" value="�V�K�o�^">
<input type="submit" name="orank" value="�e�탉���L���O">
<input type="submit" name="itiran" value="�����n�ꗗ">
<input type="submit" name="past" value="���D���n">
<input type="submit" name="rtime" value="���R�[�h">
<input type="submit" name="rule" value="�ށ[ѐ���">
<input type="button" value="ΰ��߰��" onClick="top.location.href='$url'">
</td></tr></table>
</form>

_HTML2_

print <<"_CHOSAKU_";

<hr size="1">
<div align="right"><a href="http://godon.bbzone.net/" target=_blank>���ˋ��n���[�Over1.01��(Free)</a>
<br>

<a href="http://D-BR.net/" target=_blank>�I���W�i����/���ڂ����o�g�����C����ver1.17(Free)</a></div>
<!--�L���o�i�[�}���ʒu�A�y�[�W����-->
</html>
_CHOSAKU_

}#end chosaku

##### �o��
sub html{

        if($mente eq "1"){&error("�����ݒ�ύX���ł��B<br><br>$mentecom");}

if ($title){$acomment = "<BR><BR>$acomment";}

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis">
$body

<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
</head>

<center><font color="$tcolor" size=6><B>$title</B></font>$acomment<P>
<a href=$bbs_url target=_blank>$bbs_name</a>
_HTML1_

        open(ST,"$time2file");
	seek(ST,0,0);  @st = <ST>;  close(ST);
        @st = split(/<>/,@st[0]);

        if($st[0] == 1){$hizuke = "����";}
     elsif($st[0] == $playday){$hizuke = "�ŏI��";}
                     else{$hizuke = "$st[0]����";}

        if($st[4] >= 500){$reveru = "[����]���F�����̍ŋ�����]";}
     elsif($st[4] >= 300){$reveru = "[����]���F�ŋ�����]";}
     elsif($st[4] >= 100){$reveru = "[����]���F�ꓪ�����Ă���]";}
     elsif($st[4] >= 2){$reveru = "[����]���F��������]";}
                     else{$reveru = "[����]���F�n�㐢��]";}
print "<P>�i��$st[3]��j<font size=5><b>$hizuke</b></font>�i$playday����$racemax���[�X�j";

if($counter){
           &counter;
           }
        if($st[0] >= $shyoka){
        print "$reveru";}
print "�i$ktime���X�V�j";
	open(FG,"$fightfile");                # ���[�X�̋L�^
	seek(FG,0,0);  @fg = <FG>;  close(FG);
       
        print "<DIV align=center><TABLE width=700 cellpadding=0 cellspacing=10><TBODY><tr><td valign=top><table border=2 width=220><td valign=top bgcolor=green><center>���[�X�̋L�^</center></td>\n";
	for ($i=0 ; $i<$max_fight ; $i++){
	$fgno = $i +1;
	
	if($fg[$i]){
	($time , $name , $name2 , $fight) = split(/<>/,$fg[$i]);
	print "<tr><td><center><a href=\"$cgifile?no=$fgno\">$time</a><br>$name�u�r$name2</center></td>\n";
	}
	}
        print "</table></center>";

        print "<DIV align=center><td><table border=2 width=500><tr><td width=30 bgcolor=green><center>����</td><td width=170 bgcolor=green><center>�n��</td><td width=150 bgcolor=green><center>�n�喼</td><td width=75 bgcolor=green><center>��</td><td width=75 bgcolor=green><center>�s</td></tr>";

        open(XD,"$logfile");
	seek(XD,0,0);  @nowue = <XD>;  close(XD);    # ���݂̏��

        for ($i=0 ; $i<$max_jyoui ; $i++){
	($nowno[$i], $nowname[$i], $nowsakusya[$i], $nowhomepage[$i], $nowlif[$i], $nowpow[$i], $nowdef[$i], $nowspe[$i], $nowdate[$i], $nowip[$i], $nowicon[$i], $nowwin[$i], $nowsyu[$i], $nowtotal[$i], $nowtyoushi[$i], $nowashi[$i], $nowosu[$i], $nowmesu[$i], $nowsei[$i], $nowketou[$i], $nowbaku[$i], $nowpass[$i], $gazou[$i], $rennsyou[$i], $maxren[$i], $records[$i], $records16[$i], $records18[$i], $records22[$i], $records24[$i], $nowst[$i], $titi[$i], $tiha[$i], $tititi[$i], $titiha[$i], $tihati[$i], $tihaha[$i], $hati[$i], $haha[$i], $hatiti[$i], $hatiha[$i], $hahati[$i], $hahaha[$i], $checkketou1[$i], $checkketou2[$i], $checkketou3[$i], $tokusyu[$i], $formkon[$i], $dmy, $dmy, $dmy) = split (/<>/, $nowue[$i]);
        $nowlose[$i] = $nowtotal[$i] - $nowwin[$i];

        if($nowhomepage[$i]){$nowsakusya[$i] = "<a href=\"$nowhomepage[$i]\" target=_blank>$nowsakusya[$i]</a>";}
        }
        for ($i=0 ; $i<$max_jyoui ; $i++){
        $jj = $i+1;
        if($i<$jyouiga && $iconuse eq "1"){$ga[$i] = "<img src = $imgurl/$gazou[$i]>";}
        print "<tr><td><center>$jj��</td><td>$ga[$i]<center>$nowname[$i]</td><td><center>$nowsakusya[$i]</td><td><B><center>$nowwin[$i]</B>��</td><td><center>$nowlose[$i]�s</td></tr>";
        }

        print "</table><tr><td>";

        print <<"_HTML1_";
<DIV align=center>
<table border=2 width=200><tr><td>
<form action="$cgifile" method="$method">
<center><input type="text" name="loginname" value="$c_name" size="16">�F���O<br>
<input type="password" name="loginpass" value="$c_pass" size="10">�F�p�X���[�h<BR><br>
<input type="submit" name="login" value="���O�C��"></center></td></tr></table></td>

_HTML1_

        open(WI,"$winfile");
	seek(WI,0,0);  @nowwin = <WI>;  close(WI);    # �`�����s�I���𒲂ׂ�

        ($nowno, $nowname, $nowsakusya, $nowhomepage, $nowlif, $nowpow, $nowdef, $nowspe, $nowdate, $nowip, $nowicon, $nowwin, $nowsyu, $nowtotal, $nowtyoushi, $nowashi, $nowosu, $nowmesu, $nowsei, $nowketou, $nowbaku, $nowpass, $nowgazou, $nowrennsyou, $nowmaxren, $records, $records16, $records18, $records22, $records24, $nowst, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/, @nowwin[0]);
        $nowlose = $nowtotal - $nowwin;
        if($nowrennsyou < 0){$nowrennsyou = 0;}
        if($nowhomepage){$nowsakusya = "<a href=\"$nowhomepage\" target=_blank>$nowsakusya</a>";}
        if($nowrennsyou eq ""){$nowrennsyou = 0;}
        if(@nowwin[0] eq ""){
        print "<DIV align=center><td><br><center><table border=2 width=400 cellspacing=0 cellpadding=5><tr align=center><td><font color=\"DD9966\"><B><br>���ݓo�^�ґ҂�<br><br></B></td></tr></table><br>";
        }else{
        if($iconuse){$use="<img src=$imgurl/$nowgazou>";}else{$use = "";}
        print "<DIV align=center><td><br><center><table border=2 width=400 cellspacing=0 cellpadding=5><tr align=center><td><font color=\"DD9966\"><B>���݂̃`�����s�I���@�@�@<font color=gold>$nowrennsyou</B>�A����</font><br></font>$use $nowname �y �n�� : $nowsakusya �z $nowwin�� $nowlose�s<br></td></tr></table><br>";
        }
print <<"_HTML2_";
</table>
</TBODY> 
</table>
</DIV>

<center>
_HTML2_

open(CF,"$commentfile") || &error('�w�肳�ꂽ�t�@�C�����J���܂���B');
	seek(CF,0,0);  @comments = <CF>;  close(CF);

	print "<br><table border=2 width=\"760\" cellpadding=5 cellspacing=0>\n";
	print "<tr align=\"center\"><td bgcolor=green>�R�����g�i������$max_zi���܂łł��B�j</td></tr>\n";
	print "<tr><td>\n";
        
	$i = 0;
	foreach $comments (@comments){
		($com, $host, $name, $time, $kekka) = split (/<>/, $comments);
        
	if($name eq "$news" && $kekka eq ""){print "<font color=$ncolor>��$name �w $com �x ($time)</font>\n";}
     elsif($name eq "$news" && $kekka ne ""){print "<font color=$ncolor>��$name �w $com �x �y $kekka �z($time)</font>\n";}
     elsif($kekka eq ""){   print "��$name �w $com �x  ($time)\n";}
        else{   print "��$name �w $com �x �y $kekka �z ($time)\n";}

		if($i ne $#comments){ print "<hr width=\"100%\" size=1>\n"; }
		$i++;
	}
	print "</table><br></table></center>\n";

&chosaku;

}#end html

##### ���O�C�����
sub login{

         $loginname = $form{'loginname'};
         $loginpass = $form{'loginpass'};
         $logpass = "0";

         if($loginname eq "" || $loginpass eq ""){&error('���͂���Ă܂���B');}

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis">
$body

<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
</head>

_HTML1_

       open(LO,"$logfile");
       seek(LO,0,0);  @login = <LO>;  close(LO);

        foreach $login (@login) {
	($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketoui, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$login);

   if($loginname eq $sakusya && $loginpass eq $pass){

        $check = "$login";
        @check = split(/<>/,$check);
        @iro="";

   for ($k=16; $k<43; $k++){
         if($k == 42 || $k == 38){($check, $ketou, $tokusyu) = split(/<mm>/,$check[$k]);}
         else{($check, $tokusyu) = split(/<mm>/,$check[$k]);}
         if($tokusyu ne ""){$check[$k]="$check<img src=\"$imgurl/$tokusyu.gif\">";}else{
         $check[$k]="$check";}
    if($k == 17){$k = 30;}
    }

    for ($k=31; $k<43; $k++){
         ($check, $tokusyu) = split(/<mm>/,$check[$k]);
      for ($kk=31; $kk<43; $kk++){
         ($check2, $tokusyu2) = split(/<mm>/,$check[$kk]);
         if($check eq $check2 && $k ne $kk){push(@iro, $k);}
       else{
         if($tokusyu ne ""){$check[$k]="$check<img src=\"$imgurl/$tokusyu.gif\">";}else{
         $check[$k]="$check";}}
      }
   }
       foreach $line (@iro) {
        ($check, $tokusyu) = split(/<mm>/,$check[$line]);
         if($tokusyu ne ""){$check[$line]="<font color=red>$check</font><img src=\"$imgurl/$tokusyu.gif\">";}else{
         $check[$line]="<font color=red>$check</font>";}
       }

           if($win > 34 && $sei eq "��"){$kongo = "�퉲�n";}
        elsif($win > 29 && $sei eq "��"){$kongo = "�ɐB�Ĕn";}
        elsif($icon eq "uma10.gif" || $icon eq "uma9.gif"){$kongo = "�U���n";}
        elsif($win > 19){$kongo = "��n";}
        elsif($win > 9){$kongo = "�G�p";}
         else{$kongo = "��";}
        
        if($icon eq "uma1.gif"){$iconn="����";}
        elsif($icon eq "uma2.gif"){$iconn="������";}
        elsif($icon eq "uma3.gif"){$iconn="�ȌI��";}
        elsif($icon eq "uma4.gif"){$iconn="�I��";}
        elsif($icon eq "uma5.gif"){$iconn="���ԌI��";}
        elsif($icon eq "uma6.gif"){$iconn="����";}
        elsif($icon eq "uma7.gif"){$iconn="��";}
        elsif($icon eq "uma8.gif"){$iconn="����(�Z)";}
        elsif($icon eq "uma9.gif"){$iconn="����(��)";}
        else{$iconn="����";}

        $icon_pri = "<img src=\"$imgurl/$icon\" alt=\"$iconn\">";
        
        if   ($tyoushi < 2){ $cond = "1.gif"; }
	elsif($tyoushi < 4){ $cond = "2.gif"; }
	elsif($tyoushi < 7){ $cond = "3.gif"; }
	elsif($tyoushi < 9){ $cond = "4.gif"; }
	elsif($tyoushi < 11){$cond = "5.gif"; }

        $pows = ($pow-20)*20;
        $defs = ($def-20)*20;
        $spes = ($spe-20)*20;
        $sts = ($st-20)*20;
        $kon = ($formkon)*20;

        $lose = $total - $win;
        ($hunt, $byout, $nant) = split(/<t>/,$records);
        if($hunt eq ""){$hjuy20 = "���o��";}
        else{$hjuy20 = "$hunt��$byout��$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records16);
        if($hunt eq ""){$hjuy16 = "���o��";}
        else{$hjuy16 = "$hunt��$byout��$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records18);
        if($hunt eq ""){$hjuy18 = "���o��";}
        else{$hjuy18 = "$hunt��$byout��$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records22);
        if($hunt eq ""){$hjuy22 = "���o��";}
        else{$hjuy22 = "$hunt��$byout��$nant";}
        ($hunt, $byout, $nant) = split(/<t>/,$records24);
        if($hunt eq ""){$hjuy24 = "���o��";}
        else{$hjuy24 = "$hunt��$byout��$nant";}

        $sup = int(800+ (40 * $st));   # �Œ�
        $inf = int($sup - (13 * $spe));   # �ŒZ

print <<"_HTML_";

<center>
<table border="2" width=640 cellpadding="0">
<tr><td width=170><br><center>�n���F<b>$name</b>($sei)<br><br>
$icon_pri<br><br>
<img src=\"$imgurl/$cond\"><br><br>
�n��F<b>$sakusya</b><br>
</td><td rowspan=2>

<table border=1 cellspacing=0 cellpadding=4>
<tr>
<td rowspan=4 bgcolor=#1E90FF width=150>$check[16]

<p><a href=\"$cgifile?mode=chara\" target=\~_blank\">�퉲�n�ꗗ</font></a>
<br><a href=\"$cgifile?mode=ketou\" target=\~_blank\">�퉲�n�����ڍ�</font></a>

</td>
<td rowspan=2 bgcolor=#1E90FF width=150>$check[31]</td>
<td bgcolor=#1E90FF width=150>$check[33]</td></tr><tr>
<td bgcolor=#FF69B4>$check[34]</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>$check[32]</td>
<td bgcolor=#1E90FF>$check[35]</td></tr><tr>
<td bgcolor=#FF69B4>$check[36]</td>
</tr><tr>
<td rowspan=4 bgcolor=#FF69B4>$check[17]
<P><a href=\"$cgifile?mode=hinba\" target=\~_blank\">�ɐB�Ĕn�ꗗ</font></a>
<br><a href=\"$cgifile?mode=mketou\" target=\~_blank\">�ɐB�Ĕn�����ڍ�</font></a>

</td>
<td rowspan=2 bgcolor=#1E90FF>$check[37]</td>
<td bgcolor=#1E90FF>$check[39]</td></tr><tr>
<td bgcolor=#FF69B4>$check[40]</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>$check[38]</td>
<td bgcolor=#1E90FF>$check[41]</td></tr><tr>
<td bgcolor=#FF69B4>$check[42]</td>
</tr>
</table>

</td></tr>
<tr><td><center>$total��o���F$win��$lose�s

</td></tr></table>

<table border=1 width=630 background=$imgurl/memori.gif><tr><td>
<table border=0  width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#00008B width=$pows></td><td>�X�s�[�h</td></tr></table>
<table border=0 width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#000080 width=$defs></td><td>�u����</td></tr></table>
<table border=0 width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#00008B width=$spes></td><td>�C��</td></tr></table>
<table border=0 width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#000080 width=$sts></td><td>�X�^�~�i</td></tr></table>
<table border=0 width=630 cellspacing=3 align=center><tr></center>
<td bgcolor=#000080 width=$kon></td><td>��������</td></tr></table>
</td></tr></table><center>

<table border=1 width=640 cellpadding=0>
<tr>
<td bgcolor=green width=120><center>�K������</td>
<td bgcolor=green><center>1600m</td>
<td bgcolor=green><center>1800m</td>
<td bgcolor=green><center>2000m</td>
<td bgcolor=green><center>2200m</td>
<td bgcolor=green><center>2400m</td>
</tr><tr>
<td><center>$inf�`$sup</td>
<td><center>$hjuy16</td>
<td><center>$hjuy18</td>
<td><center>$hjuy20</td>
<td><center>$hjuy22</td>
<td><center>$hjuy24</td>
</tr>
</table>
<P>

_HTML_

   $logpass = "1";last;}
       }# end foreach
       
       if(!$logpass){$wawa=1;&error('�p�X���[�h�����O���Ⴂ�܂��B');}

       ($gmonth, $gday, $ghour, $gmin) = split(/<g>/,$date);   # �ŏI���[�X����

	$times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);

	$tmonth = sprintf("%02d",$mon +1);     # ���݂̎���
	$tday = sprintf("%02d",$mday);
	$thour = sprintf("%02d",$hour);
	$tmin = sprintf("%02d",$min);

print "<form action=$cgifile method=$method>";

      if($gmonth == $tmonth && $gday == $tday && $ghour == $thour && abs($gmin - $tmin) < $kankaku){
$mate = $kankaku - abs($gmin - $tmin);

print "<br>����$mate���҂��ĂĂˁB<br><br>";

       }elsif($no eq "-1"){
print <<"_HTML_";

<P>��L�̔n�͈��ނ��܂����B<P>
<input type="hidden" name="logint" value="$loginname">
<input type="hidden" name="tourou" value="5">
<input type="submit" name="rec" value="���V�[�Y���p�̋����n�̓o�^"><P>
_HTML_

       }elsif($no eq "-2"){

       open(KK,"$kisyufile");
       seek(KK,0,0);  @kk = <KK>;  close(KK);
       @kisyu="";
       for ($i=0; $i<$#kk+1; $i++){
       ($name[$i], $comm[$i], $win[$i], $lose[$i], $omona[$i], $omona2[$i], $dmy) = split(/<>/,$kk[$i]);
       $kisyu[$i]=$name[$i];
       }

       @sakusen = ('�哦','����','��s','����','�Ǎ�');
print"<P>�D���n�Ƃ��ĊM����܂ɒ��킷�邱�Ƃ����܂�܂����B<P>\n";
print"<select name=syu>\n";
foreach (@kisyu) {
		if ($_ eq "$syu") { print "<option value=\"$_\" selected>$_\n"; }
		else { print "<option value=\"$_\">$_\n"; }
	}
print"</select><a href=\"$cgifile?mode=kisyu\" target=\"_blank\">�R��ꗗ</a>\n";
print"<select name=sakusen>\n";
foreach (@sakusen) {
		if ($_ eq "$ashi") { print "<option value=\"$_\" selected>$_\n"; }
		else { print "<option value=\"$_\">$_\n"; }
	}
print"</select>\n";
print"<input type=hidden name=logint value=$loginname>\n";
print"<input type=hidden name=gaisen value=7>\n";
print"<input type=submit name=race value=�M����܂ɒ���><br><br>\n";


       }elsif($name eq "������"){

print <<"_HTML_";

<P>$sei�̎e�����܂�܂����B���O�����ĉ������B�i$nameleng�����ȉ��j<P>
<input type="text" name="umaname" size=25>
<input type="hidden" name="comsaku" value="$loginname">
<input type="submit" name="nameda" value="���O����"><br><br>
_HTML_

       }elsif($total < $racemax){

       open(KK,"$kisyufile");
       seek(KK,0,0);  @kk = <KK>;  close(KK);
       @kisyu="";
       for ($i=0; $i<$#kk+1; $i++){
       ($name[$i], $comm[$i], $win[$i], $lose[$i], $omona[$i], $omona2[$i], $dmy) = split(/<>/,$kk[$i]);
       $kisyu[$i]=$name[$i];
       }

       @sakusen = ('�哦','����','��s','����','�Ǎ�');
print"<select name=syu>\n";
foreach (@kisyu) {
		if ($_ eq "$syu") { print "<option value=\"$_\" selected>$_\n"; }
		else { print "<option value=\"$_\">$_\n"; }
	}
print"</select><a href=\"$cgifile?mode=kisyu\" target=\"_blank\">�R��ꗗ</a>\n";
print"<select name=sakusen>\n";
foreach (@sakusen) {
		if ($_ eq "$ashi") { print "<option value=\"$_\" selected>$_\n"; }
		else { print "<option value=\"$_\">$_\n"; }
	}
print"</select>\n";
print"<input type=hidden name=logint value=$loginname>\n";
print"<input type=submit name=race value=���[�X�J�n><P>\n";

       }else{

print "<br>�V�[�Y���I��($kongo)<br>";

      }
print <<"_HTML2_";

<center>�R�����g
<input type="text" name="comtext" size=75>
<input type="hidden" name="comname" value="$loginname">
<input type="submit" name="comment" value="��������">
<input type="submit" value="�g�b�v�y�[�W"></form>

_HTML2_

&chosaku;

}#end login

##### �����n�ꗗ
sub itiran{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--�L���o�i�[�}���ʒu�A�y�[�W�㕔-->
<center><font color="$tcolor" size="5"><B>�����n�ꗗ</B></font><P>
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<table border="1" width="790">

<tr>
<td bgcolor=green width=50><center>����</td>
<td bgcolor=green width=180><center>�n���i���ʁj</td>
<td bgcolor=green width=50><center>ڰ�</td>
<td bgcolor=green width=50><center>����</td>
<td bgcolor=green width=50><center>����</td>
<td bgcolor=green width=50><center>�A��</td>
<td bgcolor=green width=60><center>����</td>
<td bgcolor=green width=70><center>���</td>
<td bgcolor=green width=70><center>�r��</td>
<td bgcolor=green width=70><center>�ѐF</td>
<td bgcolor=green width=110><center>�n��</td>
</tr>

_HTML1_

        open(LL,"$logfile");
	seek(LL,0,0);  @itiran = <LL>;  close(LL);
if($#itiran > 20){
$gg = 19;
}else{$gg = $#itiran;}
$ggg=$gg+1;
       for ($g=0; $g<$ggg; $g++){
       ($no[$g], $name[$g], $sakusya[$g], $homepage[$g], $lif[$g], $pow[$g], $def[$g], $spe[$g], $date[$g], $ip[$g], $icon[$g], $win[$g], $syu[$g], $total[$g], $tyoushi[$g], $ashi[$g], $osu[$g], $mesu[$g], $sei[$g], $ketou[$g], $baku[$g], $pass[$g], $gazou[$g], $rennsyou[$g], $maxren[$g], $records[$g], $records16[$g], $records18[$g], $records22[$g], $records24[$g], $st[$g], $titi[$g], $tiha[$g], $tititi[$g], $titiha[$g], $tihati[$g], $tihaha[$g], $hati[$g], $haha[$g], $hatiti[$g], $hatiha[$g], $hahati[$g], $hahaha[$g], $checkketou1[$g], $checkketou2[$g], $checkketou3[$g], $dmy, $formkon[$g], $dmy, $dmy, $dmy) = split(/<>/,$itiran[$g]);

        if($homepage[$g]){$sakusya[$g] = "<a href=\"$homepage[$g]\" target=_blank>$sakusya[$g]</a>";}
        @keiroo = ('','����','������','�ȌI��','�I��','���ԌI��','����','��','����(�Z)','����(��)','����');
        for ($y=1; $y<11; $y++){
        if($icon[$g] eq "uma$y.gif"){$icon[$g] = $y;}
        }
        $keiro[$g] =  "$keiroo[$icon[$g]]";
        if($total[$g] == $racemax){$gcolor[$g]=green}
        $lose[$g] = $total[$g] - $win[$g];
        if($total[$g] eq "0"){$ritu[$g] = "���o��";}else{
        $ritu[$g] = sprintf("%03d", ($win[$g]/$total[$g]) * 1000);}
        $gg = $g+1;

	print "<tr><td><center>$gg��</td><td><center><b>$name[$g]($sei[$g])</b></td><td><center><font color=$gcolor[$g]>$total[$g]</font></td><td><center>$win[$g]</td><td><center>$lose[$g]</td><td><center>$maxren[$g]</td><td><center>.$ritu[$g]</td><td><center>$syu[$g]</td><td><center>$ashi[$g]</td><td><center>$keiro[$g]</td><td><center>$sakusya[$g]</td></tr>\n";
                }

        print "</table><P><center>";

    if($#itiran > 20){
        print "<select>";
        for ($g=20; $g<$#itiran+1; $g++){
	($no[$g], $name[$g], $sakusya[$g], $homepage[$g], $lif[$g], $pow[$g], $def[$g], $spe[$g], $date[$g], $ip[$g], $icon[$g], $win[$g], $syu[$g], $total[$g], $tyoushi[$g], $ashi[$g], $osu[$g], $mesu[$g], $sei[$g], $ketou[$g], $baku[$g], $pass[$g], $gazou[$g], $rennsyou[$g], $maxren[$g], $records[$g], $records16[$g], $records18[$g], $records22[$g], $records24[$g], $st[$g], $titi[$g], $tiha[$g], $tititi[$g], $titiha[$g], $tihati[$g], $tihaha[$g], $hati[$g], $haha[$g], $hatiti[$g], $hatiha[$g], $hahati[$g], $hahaha[$g], $checkketou1[$g], $checkketou2[$g], $checkketou3[$g], $dmy, $formkon[$g], $dmy, $dmy, $dmy) = split(/<>/,$itiran[$g]);
        $gg = $g + 1;
        $lose[$g] = $total[$g] - $win[$g];
        print "<option>[$gg] $total[$g]���[�X $win[$g]�� $lose[$g]�s $name[$g] �i$sakusya[$g]�j\n";
     }
	print "</select></table>";
        }
&chosaku;

}#end itiran


##### �A�C�R���ꗗ
sub icon{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<!--�L���o�i�[�}���ʒu�A�y�[�W�㕔-->
<center><font color="red" size="5"><b>�A�C�R���ꗗ</b></font><P>

_HTML1_

print "<table width=400 border=1><tr>";
          $iconsuu=0;
      for ($i=0; $i<$#icon1+1; $i++){
          $iconsuu++;
          if($iconsuu eq "4"){$iconsuu=0;
      print "<td><br><center><img src=$imgurl/$icon1[$i].gif><br><center>$icon2[$i]</font></td></tr><tr>";
          }else{
      print "<td><br><center><img src=$imgurl/$icon1[$i].gif><br><center>$icon2[$i]</font></td>";
          }
      }

print "</table></TBODY></TABLE></DIV>";

&chosaku;

}#end icon

##### �퉲�n�ꗗ
sub chara{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--�L���o�i�[�}���ʒu�A�y�[�W�㕔-->
<center><font color="$tcolor" size="5"><B>�퉲�n�ꗗ</B></font><P>
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<form action="$cgifile" method="$method">
<input type="hidden" name="chara" value=1>
<input type="submit" name="toshi"  value="�N��">
�@�@<input type="submit" name="syu"  value="���O">
�@�@<input type="submit" name="ketou"  value="����">
�@�@<input type="submit" name="uma"  value="�ѐF">
�@�@<input type="submit" name="sp"  value="��߰��">
�@�@<input type="submit" name="syun"  value="�u����">
�@�@<input type="submit" name="ki"  value="�C��">
�@�@<input type="submit" name="kon"  value="��������">
�@�@<input type="submit" name="teki"  value="�����K��">
�@�@<input type="submit" name="baku"  value="������">
</form>

<table border="1" width="720"><tr>
<td bgcolor=green><center>�N��</td>
<td bgcolor=green width=140><center>���O</td>
<td bgcolor=green width=140><center>����</td>
<td bgcolor=green><center>�ѐF</td>
<td bgcolor=green><center>��߰��</td>
<td bgcolor=green><center>�u����</td>
<td bgcolor=green><center>�C��</td>
<td bgcolor=green><center>��������</td>
<td bgcolor=green><center>�����K��</td>
<td bgcolor=green><center>������</td></tr>
_HTML1_

        open(TK,"$tanefile");
        seek(TK,0,0);  @tk = <TK>;  close(TK);
        if($form{'toshi'}){$snumber = 8;}
     elsif($form{'syu'}){$snumber = 0;}
     elsif($form{'ketou'}){$snumber = 1;}
     elsif($form{'kon'}){$snumber = 2;}
     elsif($form{'uma'}){$snumber = 6;}
     elsif($form{'sp'}){$snumber = 3;}
     elsif($form{'syun'}){$snumber = 4;}
     elsif($form{'ki'}){$snumber = 5;}
     elsif($form{'teki'}){$snumber = 9;} 
     elsif($form{'baku'}){$snumber = 7;}
      else{$snumber = 0;}

        if($snumber == 0 || $snumber == 1 || $snumber == 6 || $snumber == 7){
   @sortdata = sort { (split(/<>/,$a))[$snumber] cmp (split(/<>/,$b))[$snumber] } @tk;}
        else{
   @sortdata = sort { (split(/<>/,$b))[$snumber] <=> (split(/<>/,$a))[$snumber] } @tk;}

        foreach $line (@sortdata) {
	($tanename, $kettou, $formkon, $supi, $syun, $kisei, $keiro, $baku, $toshi, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha) = split(/<>/,$line);

        ($tane, $tokusyu) = split(/<mm>/,$tanename);

        if($keiro eq "uma1.gif"){$iconn="����";}
        elsif($keiro eq "uma2.gif"){$iconn="������";}
        elsif($keiro eq "uma3.gif"){$iconn="�ȌI��";}
        elsif($keiro eq "uma4.gif"){$iconn="�I��";}
        elsif($keiro eq "uma5.gif"){$iconn="���ԌI��";}
        elsif($keiro eq "uma6.gif"){$iconn="����";}
        elsif($keiro eq "uma7.gif"){$iconn="��";}
        elsif($keiro eq "uma8.gif"){$iconn="����(�Z)";}
        elsif($keiro eq "uma9.gif"){$iconn="����(��)";}
        else{$iconn="����";}

        $icon_pri = "<img src=\"$imgurl/$keiro\" align=\"absmiddle\" alt=\"$iconn\">";

        &nouhan;

print "<tr><td><center>$toshi��</td><td><center><B>$tane</B></td><td><center>$kettou�n</td><td><center>$icon_pri</td><td><center>$s</td><td><center>$ss</td><td><center>$sss</td><td><center>$sssss</td><td><center>$ssss</td><td><center>$baku</td></tr>";
      }

print "</table>";

&chosaku;

}#end chara


##### �ɐB�Ĕn�ꗗ
sub hinba{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--�L���o�i�[�}���ʒu�A�y�[�W�㕔-->
<center><font color="$tcolor" size="5"><B>�ɐB�Ĕn�ꗗ</B></font><P>
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>

<form action="$cgifile" method="$method">
<input type="hidden" name="hinba" value=1>
<input type="submit" name="toshi"  value="�N��">
�@�@<input type="submit" name="syu"  value="���O">
�@�@<input type="submit" name="ketou"  value="����">
�@�@<input type="submit" name="uma"  value="�ѐF">
�@�@<input type="submit" name="sp"  value="��߰��">
�@�@<input type="submit" name="syun"  value="�u����">
�@�@<input type="submit" name="ki"  value="�C��">
�@�@<input type="submit" name="kon"  value="��������">
�@�@<input type="submit" name="teki"  value="�����K��">
</form>

<table border="1" width="680"><tr>
<td bgcolor=green><center>�N��</td>
<td bgcolor=green width=150><center>���O</td>
<td bgcolor=green width=150><center>����</td>
<td bgcolor=green><center>�ѐF</td>
<td bgcolor=green><center>��߰��</td>
<td bgcolor=green><center>�u����</td>
<td bgcolor=green><center>�C��</td>
<td bgcolor=green><center>��������</td>
<td bgcolor=green><center>�����K��</td>
</tr>
_HTML1_

        open(TK,"$tamefile");
        seek(TK,0,0);  @mk = <TK>;  close(TK);
        if($form{'toshi'}){$mnumber = 8;}   #
     elsif($form{'syu'}){$mnumber = 0;}
     elsif($form{'ketou'}){$mnumber = 1;}
     elsif($form{'kon'}){$mnumber = 2;}
     elsif($form{'uma'}){$mnumber = 6;}
     elsif($form{'sp'}){$mnumber = 3;}      #
     elsif($form{'syun'}){$mnumber = 4;}    #
     elsif($form{'ki'}){$mnumber = 5;}      #
     elsif($form{'teki'}){$mnumber = 9;}    #
     elsif($form{'baku'}){$mnumber = 7;}
      else{$mnumber = 0;}

        if($mnumber == 0 || $mnumber == 1 || $mnumber == 6 || $mnumber == 7){
   @sortdata = sort { (split(/<>/,$a))[$mnumber] cmp (split(/<>/,$b))[$mnumber] } @mk;}
        else{
   @sortdata = sort { (split(/<>/,$b))[$mnumber] <=> (split(/<>/,$a))[$mnumber] } @mk;}

        foreach $line (@sortdata) {
	($tanename, $kettou, $formkon, $supi, $syun, $kisei, $keiro, $baku, $toshi, $st, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha) = split(/<>/,$line);
         ($tane, $tokusyu) = split(/<mm>/,$tanename);
        ($checkname2, $checkketou2) = split(/<mm>/,$haha);
        $hinhaha    = $checkketou2; # ���
        ($checkname3, $checkketou3) = split(/<mm>/,$hahaha);
        $hinhahaha  = $checkketou3; # ����

                if($keiro eq "uma1.gif"){$iconn="����";}
        elsif($keiro eq "uma2.gif"){$iconn="������";}
        elsif($keiro eq "uma3.gif"){$iconn="�ȌI��";}
        elsif($keiro eq "uma4.gif"){$iconn="�I��";}
        elsif($keiro eq "uma5.gif"){$iconn="���ԌI��";}
        elsif($keiro eq "uma6.gif"){$iconn="����";}
        elsif($keiro eq "uma7.gif"){$iconn="��";}
        elsif($keiro eq "uma8.gif"){$iconn="����(�Z)";}
        elsif($keiro eq "uma9.gif"){$iconn="����(��)";}
        else{$iconn="����";}

        $icon_pri = "<img src=\"$imgurl/$keiro\" align=\"absmiddle\" alt=\"$iconn\">";

        &nouhan;

print "<tr><td><center>$toshi��</td><td><center><B>$tane</B></td><td><center><B>$kettou�n</B><br><font size=1>$hinhaha�n<br>$hinhahaha�n</font></td><td><center>$icon_pri</td><td><center>$s</td><td><center>$ss</td><td><center>$sss</td><td><center>$sssss</td><td><center>$ssss</td></tr>";
      }
print "</table>";

&chosaku;

}#end hinba

#######  �J�E���^����

sub counter{
	local($cnt,$host);

# �J�E���g�t�@�C����ǂ݂���
	open(IN,"$cntfile") || &error("Open Error : $cntfile");
	eval "flock(IN, 1);";
        $data = <IN>;
	close(IN);

# �����[�g�z�X�g�擾
	$hostt = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};

# �ʂh�o���̂݃J�E���g�A�b�v
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

# �J�E���^�\��
	if($counter){
		print "<p>$cnt�l�̊ϐ��\n";
	}
}#end counter

#######  �N�b�L�[�̔��s

sub set_cookie{
	$ENV{'TZ'} = "GMT"; # ���ەW�������擾
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

       $cookies="name\<>$formname\,hp\<>$formhp\,pass\<>$formpass";
	print "Set-Cookie: UMA=$cookies; expires=$date_gmt\n";
}#end set_cookie

#######  �N�b�L�[���擾

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
        $c_pass = $COOKIE{'pass'};
        
	if($form{'name'}){$c_name = $form{'name'};}
	if($form{'hp'}){$c_hp = $form{'hp'};}
        if($form{'pass'}){$c_pass = $form{'pass'};}
        
}#end get_cookie


##### ���[�O�X�V����
sub koushin{

        open(LL,"$logfile");                        # �D���n
	seek(LL,0,0);  @yuusyou = <LL>;  close(LL);

       ($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketou, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,@yuusyou[0]);

        $endname = "$name";
        $endman = "$sakusya";
        $endmake = $total - $win;
        $endwin = $win;

        open(ST,"$time2file");
	seek(ST,0,0);  @st = <ST>;  close(ST);
        ($hiniti, $hi, $zikan, $rigu) = split(/<>/, @st[0]);
        $endrigu = $rigu;

        open(PST,"$pastfile");
	seek(PST,0,0);  @pst = <PST>;  close(PST);
        
        $pasts = "@yuusyou[0]";
@pst = reverse(@pst);
        push(@pst,$pasts);
@pst = reverse(@pst);
        open(PST,">$pastfile") ;             # ���D���n�ɋL�^
        eval 'flock(PST,2);';
	seek(PST,0,0);	print PST @pst;
	eval 'flock(PST,8);';
        close(PST);

        $shiki = 7;&shinkiro;                # �j���[�X�ɋL�^

###### �퉲�n�̔N���+1
        @umao = "";
        open(RO,"$tanefile");
	seek(RO,0,0);  @syubo = <RO>;  close(RO);

        foreach $lines (@syubo) {      # �N���+1�ɂ���B
	($name, $ketou, $formkon, $pow, $def, $spe, $icon, $baku, $toshi, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha) = split(/<>/,$lines);
        if($toshi < $osuintai){         # ����
           $toshi++;
    $syubouma = "$name<>$ketou<>$formkon<>$pow<>$def<>$spe<>$icon<>$baku<>$toshi<>$st<>$titi<>$tiha<>$tititi<>$titiha<>$tihati<>$tihaha<>\n";
        push(@umao,$syubouma);
        }} # if ��foreach
        open(RO,">$tanefile") ;
		eval 'flock(RO,2);';
		seek(RO,0,0);	print RO @umao;
		eval 'flock(RO,8);';
	close(RO);

###### �ɐB�Ĕn�̔N���+1
        @umam = "";
        open(RM,"$tamefile");
	seek(RM,0,0);  @hansyo = <RM>;  close(RM);

        foreach $lines (@hansyo) {      # �N���+1�ɂ���B
	($name, $ketou, $formkon, $pow, $def, $spe, $icon, $baku, $toshi, $st, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha) = split(/<>/,$lines);
        if($toshi < $mesuintai){         # ����
           $toshi++;
    $hansyouma = "$name<>$ketou<>$formkon<>$pow<>$def<>$spe<>$icon<>$baku<>$toshi<>$st<>$hati<>$haha<>$hatiti<>$hatiha<>$hahati<>$hahaha<>\n";

        push(@umam,$hansyouma);
        }}
        open(RM,">$tamefile") ;
		eval 'flock(RM,2);';
		seek(RM,0,0);	print RM @umam;
		eval 'flock(RM,8);';
	close(RM);

        open(RO,"$tanefile");
	seek(RO,0,0);  @umao = <RO>;  close(RO);

        @liness = "";
        open(LK,"$logfile");
	seek(LK,0,0);  @lines = <LK>;  close(LK);

              foreach $lines (@lines) {      # �o�����E���������O�ɂ���B
	($no, $name, $sakusya, $homepage, $lif, $pow, $def, $spe, $date, $ip, $icon, $win, $syu, $total, $tyoushi, $ashi, $osu, $mesu, $sei, $ketou, $baku, $pass, $gazou, $rennsyou, $maxren, $records, $records16, $records18, $records22, $records24, $st, $titi, $tiha, $tititi, $titiha, $tihati, $tihaha, $hati, $haha, $hatiti, $hatiha, $hahati, $hahaha, $checkketou1, $checkketou2, $checkketou3, $tokusyu, $formkon, $dmy, $dmy, $dmy) = split(/<>/,$lines);
        $reiketu = 1;
        if($sei eq "��" && $total > 0){
        $reiketu = 0;
        foreach $line (@umao) {
	($names, $keto, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy, $dmy) = split(/<>/,$line);
        if($ketou eq $keto){$reiketu = 1;last;}
        }}
###### �퉲�n�E�ɐB�Ĕn�ɏ�������
        if(($win >= $taneosu && $sei eq "��") || ($win >= $tanemesu && $sei eq "��") || $reiketu eq "0"){

        if($pow >= 40){$pows=$pow;
           while($pows >= 37){
           $pows--;}}
        elsif($pow >= 39){$pows=$pow;
           while($pows >= 36){
           $pows--;}}
        elsif($pow >= 37){$pows=$pow;
           while($pows >= 35){
           $pows--;}}
        elsif($pow >= 35){$pows = 35;}
         else{$pows = $pow;}
        if($def >= 40){$defs=$def;
           while($defs >= 37){
           $defs--;}}
        elsif($def >= 39){$defs=$def;
           while($defs >= 36){
           $defs--;}}
        elsif($def >= 37){$defs=$def;
           while($defs >= 35){
           $defs--;}}
        elsif($def >= 35){$defs = 35;}
         else{$defs = $def;}
        if($spe >= 40){$spes=$spe;
           while($spes >= 37){
           $spes--;}}
        elsif($spe >= 39){$spes=$spe;
           while($spes >= 36){
           $spes--;}}
        elsif($spe >= 37){$spes=$spe;
           while($spes >= 35){
           $spes--;}}
        elsif($spe >= 35){$spes = 35;}
         else{$spes = $spe;}
        if($formkon >= 20){$formkon = 20;}
        if($sei eq "��"){
        $katiuma = "$name<mm>$tokusyu<>$ketou<>$formkon<>$pows<>$defs<>$spes<>$icon<>$baku<>6<>$st<>$osu<>$mesu<>$titi<>$tiha<>$hati<>$haha<>\n";}else{
        ($checkname2, $tokusyu2) = split(/<mm>/,$mesu);
        ($checkname3, $tokusyu3) = split(/<mm>/,$haha);
        $katiuma = "$name<mm>$tokusyu<>$ketou<>$formkon<>$pows<>$defs<>$spes<>$icon<>$baku<>6<>$st<>$osu<>$checkname2<mm>$checkketou1<mm>$tokusyu2<>$titi<>$tiha<>$hati<>$checkname3<mm>$checkketou2<mm>$tokusyu3<>\n";}

if($sei eq "��"){
        open(RO,"$tanefile");
	seek(RO,0,0);  @umao = <RO>;  close(RO);

        push(@umao,$katiuma);
        open(RO,">$tanefile") ;
		eval 'flock(RO,2);';
		seek(RO,0,0);	print RO @umao;
		eval 'flock(RO,8);';
	close(RO);

}elsif($sei eq "��"){
        open(RM,"$tamefile");
	seek(RM,0,0);  @umam = <RM>;  close(RM);

        push(@umam,$katiuma);
        open(RM,">$tamefile") ;
		eval 'flock(RM,2);';
		seek(RM,0,0);	print RM @umam;
		eval 'flock(RM,8);';
	close(RM);
}
}

             if($total > 0){
                 if($endname eq $name){
             $liness = "-2<>$name<>$sakusya<>$homepage<>$lif<>$pow<>$def<>$spe<>$date<>$ip<>$icon<>0<>$syu<>0<>5<>$ashi<>$osu<>$mesu<>$sei<>$ketou<>$baku<>$pass<>$gazou<>0<>0<><><><><><>$st<>$titi<>$tiha<>$tititi<>$titiha<>$tihati<>$tihaha<>$hati<>$haha<>$hatiti<>$hatiha<>$hahati<>$hahaha<>$checkketou1<>$checkketou2<>$checkketou3<>$tokusyu<>$formkon<>$dmy<>$dmy<>$dmy<>\n";
                 }else{
             $liness = "-1<>$name<>$sakusya<>$homepage<>$lif<>$pow<>$def<>$spe<>$date<>$ip<>$icon<>0<>$syu<>0<>5<>$ashi<>$osu<>$mesu<>$sei<>$ketou<>$baku<>$pass<>$gazou<>0<>0<><><><><><>$st<>$titi<>$tiha<>$tititi<>$titiha<>$tihati<>$tihaha<>$hati<>$haha<>$hatiti<>$hatiha<>$hahati<>$hahaha<>$checkketou1<>$checkketou2<>$checkketou3<>$tokusyu<>$formkon<>$dmy<>$dmy<>$dmy<>\n";}

             push(@liness,$liness)
             }
             }

        open(LK,">$logfile") ;             # �����n�ꗗ�ɋL�^
        eval 'flock(LK,2);';
	seek(LK,0,0);	print LK @liness;
	eval 'flock(LK,8);';
        close(LK);

        @kuufile = "";              # �`�����s�I��������
	open(TT,">$winfile") ;
		eval 'flock(TT,2);';
		seek(TT,0,0);	print TT @kuufile;
		eval 'flock(TT,8);';
	close(TT);

        open(LI,">$fightfile") ;             # ���[�X�̋L�^������
		eval 'flock(LI,2);';
		seek(LI,0,0);	print LI @kuufile;
		eval 'flock(LI,8);';
	close(LI);

        open(BK,">$backupfile") ;
               eval 'flock(BK,2);';           # �o�b�N�A�b�v�t�@�C��������
	       seek(BK,0,0);	print BK @kuufile;
	       eval 'flock(BK,8);';
        close(BK);

}#end koushin

##### ���[������
sub rule{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
-->
</style>
<center><font color="$tcolor" size="5"><B>�����т���</B></font>

<hr size="1">
<table border="1" width="660" cellpadding="5"><tr><td><BR>
�@�E�@���̃Q�[���͔n��o�^���ėV�΂���Q�[������B<BR><BR>
�@�E�@�P�V�[�Y����<b>$playday</b>����<b>$racemax</b>���[�X����B<BR><BR>
�@�E�@�P�l�o�^�ł���̂͂P���܂ł���B<BR><BR>
�@�E�@������$ktime���ɕς���B<BR><BR>
�@�E�@���[�X�ƃ��[�X�̊Ԋu��<b>$kankaku</b>���K�v����B<BR><BR>
�@�E�@�퉲�n�ƔɐB�Ĕn��I��łˁB<BR><BR>
�@�E�@�����̃����L���O�������B<BR><BR>
�@�E�@�����̐��Y�ƃ����L���O�������B<BR><BR>
�@�E�@�����̎퉲�n�E�ɐB�Ĕn�����L���O�������B<BR><BR>
�@�E�@���q�͏������n���������n���ω������B<br><br>
�y�����́z�E�E�E�����Ă���\�\\�͂��ǂꂾ���e�ɓ`���邩�ƌ������̂���B<br>
�@�b<br>
�@���`�F���肵�č���\�\\�͂�`����B<br>
�@���a�F��\�\\���肵�č���\�\\�͂�`����B<br>
�@���b�F����܂���肵�ĂȂ����H�ɁE�E�E�i��B<br>
�@���c�F�s����C���B<br><br>
�@�E�@���[�X�̋�����1600m�`2400m����B<BR><BR>
�y�����K���z�E�E�E�C�����ǂ��قǓK���͈͍͂L����B<BR>
�@�b<br>
�@���Z�@�����F1600m�`2000m<br>
�@���Z�������F1700m�`2100m<br>
�@�����@�����F1800m�`2200m<br>
�@�����������F1900m�`2300m<br>
�@�����@�����F2000m�`2400m<br><br>
�y�R������z�E�E�E�R��̓�������B<br>
�@�b<br>
�@���V�n�F�P�E�Q��ڂ̔n��\�\\�̓A�b�v<br>
�@���C�O�F�C�O�i�M����܂�\�\\�̓A�b�v�j<br>
�@���Ĕn�F�Ĕn��\�\\�̓A�b�v<br>
�@�����n�F�v���؂����R��Ől�C���̔n��\�\\�̓A�b�v<br>
�@�����r�F�S�[���O�œ����E��s�n��\�\\�̓A�b�v<br>
�@������j�F2200m�ȏ��\�\\�̓A�b�v<br>
�@�����ԕځF�S�[���O�ō����E�Ǎ��ݔn��\�\\�̓A�b�v<br>
�@���܂荇���F�C����n���Ȃ��߂�<br>
�@�����[�J���F���q�E�����E�����E�V���E���فE�D�y��\�\\�̓A�b�v<br>
�@���D�X�^�[�g�F�D�X�^�[�g�����₷��<br><br>
<table border=1 cellspacing=0 cellpadding=4>
<tr>
<td rowspan=4 bgcolor=#1E90FF width=150>��(�`�n)</td>
<td rowspan=2 bgcolor=#1E90FF width=150>����</td>
<td bgcolor=#1E90FF width=150>������</td></tr><tr>
<td bgcolor=#FF69B4>������</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>����</td>
<td bgcolor=#1E90FF>���ꕃ</td></tr><tr>
<td bgcolor=#FF69B4>�����</td>
</tr><tr>
<td rowspan=4 bgcolor=#FF69B4 width=150>��(�a�n)</td>
<td rowspan=2 bgcolor=#1E90FF>�ꕃ</td>
<td bgcolor=#1E90FF>�ꕃ��</td></tr><tr>
<td bgcolor=#FF69B4>�ꕃ��</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>���(�b�n)</td>
<td bgcolor=#1E90FF>��ꕃ</td></tr><tr>
<td bgcolor=#FF69B4>����(�c�n)</td>
</tr>
</table><br><br>
�y�z�����_�z�E�E�E���������n�𐶎Y���邽�߂̗��_����B<br>
�@�b<br>
�@�������F�������̌������m����͋����n���Y�܂�₷���ƌ������̂���B<br>
�@�b�@�b<br>
�@�b�@���g���v���j�b�N�X�i�`�n�|�a�n�A�`�n�|�b�n�A�`�n�|�c�n�j<br>
�@�b�@�b�@�@�@���X�s�[�h�j�b�N�X�F�X�s�[�h�{�{�{<br>
�@�b�@�b�@�@�@���u���̓j�b�N�X�F�u���́{�{�{<br>
�@�b�@�b<br>
�@�b�@���_�u���j�b�N�X�i�`�n�|�a�n�A�`�n�|�b�n�j<br>
�@�b�@�b�@�@�@���X�s�[�h�j�b�N�X�F�X�s�[�h�{�{<br>
�@�b�@�b�@�@�@���u���̓j�b�N�X�F�u���́{�{<br>
�@�b�@�b<br>
�@�b�@���j�b�N�X�i�`�n�|�a�n�j<br>
�@�b�@�@�@�@�@���X�s�[�h�j�b�N�X�F�X�s�[�h�{<br>
�@�b�@�@�@�@�@���u���̓j�b�N�X�F�u���́{<br>
�@�b<br>
�@���T���i���z���F�퉲�n�ƔɐB�Ĕn�̔N����Ɂ����̔z���B�X�s�[�h�{�{<br>
�@�������z���F�퉲�n�ƔɐB�Ĕn�̔����͂����Ɂ����m�̔z���B�X�s�[�h�{�{�{�A�u���́{�{<br>
�@�����ѓ`���z���F�퉲�n�ƔɐB�Ĕn�̖ѐF�����Ɂ��ѓ��m�̔z���B�X�s�[�h�{�A�u���́{<br>
�@���I�z���F�퉲�n�ƔɐB�Ĕn�̖ѐF�����Ɂ��ѓ��m�̔z���B�X�s�[�h�{�A�C���{<br>
�@�����n�z���F�����������m�̔z���B�X�s�[�h�|�|<br>
�@���C���u���[�h�F�퉲�n�A�ɐB�Ĕn�̌����ɋ��ʂ̑c��̔n������z���B<br>
�@�b�@�@��(�P�~�Q)(�P�~�R)(�Q�~�Q)(�Q�~�R)�F�֎~<br>
�@�b�@�@��(�R�~�R)�F�C���|�A����q�i<img src=\"$imgurl/sp2.gif\"><img src=\"$imgurl/syu2.gif\"><img src=\"$imgurl/ki2.gif\"><img src=\"$imgurl/st2.gif\"><img src=\"$imgurl/kon2.gif\">�j�������Ă�������q�{�{�A�����q�i<img src=\"$imgurl/sp1.gif\"><img src=\"$imgurl/syu1.gif\"><img src=\"$imgurl/ki1.gif\"><img src=\"$imgurl/st1.gif\"><img src=\"$imgurl/kon1.gif\">�j�������Ă�������q�{<br>
�@�b�@�@�@�@�����q�̓����͍�����i�X�s�[�h�A�u���́A�C���A�X�^�~�i�A���������j<br>
�@�b�@�@�@�@������ɂR�O���̊m���ŃX�s�[�h�{�A�u���́{�A�V�O���̊m���ŃX�s�[�h�|�A�u���́|<br>
�@���A�E�g�u���[�h�F�퉲�n�A�ɐB�Ĕn�̌����ɋ��ʂ̑c��̔n�����Ȃ��z���B�C���{�{<br><br>
�y�z����z�@�t�T�C�`�R���R���h�i���{�_�[�r�[�j<br><br>
�E���J�[���A���͐��E�e�n�Ŗ��n�i�M����ܔn�F�}���G���o�[�g���j��y�o�������퉲�n�B�������\\�́A�����͂`<br>
�E��o���[�N�C�[���̎e�ɂ̓{�[���L���O�E�O���[�X�A�h�}�C���ȂǏd�܂Ŋ��􂷂�n������B�������\\��<br>
�E�m�[�U���_���T�[�̃C���u���[�h(�R�~�R)���X�s�[�h�{�A�u���́{�A���������{�A�C���|<br>
�E�j�W���X�L�[�n�ƃm�[�U���_���T�[�n�̓X�s�[�h�j�b�N�X���X�s�[�h�{<br>
<table border=1 cellspacing=0 cellpadding=4>
<tr>
<td rowspan=4 bgcolor=#1E90FF width=150>�J�[���A��<br>(�j�W���X�L�[�n)</td>
<td rowspan=2 bgcolor=#1E90FF width=150>Nijinsky<img src=\"$imgurl/sp1.gif\"></td>
<td bgcolor=#1E90FF width=150><font color=red>�m�[�U���_���T�[</font><img src=\"$imgurl/kon1.gif\"></td></tr><tr>
<td bgcolor=#FF69B4>Flaming Page</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>Foreseer</td>
<td bgcolor=#1E90FF>Round Table</td></tr><tr>
<td bgcolor=#FF69B4>Regal Gleam</td>
</tr><tr>
<td rowspan=4 bgcolor=#FF69B4 width=150>�o���[�N�C�[��<br>(�m�[�U���_���T�[�n)</td>
<td rowspan=2 bgcolor=#1E90FF>Sadler's Wells</td>
<td bgcolor=#1E90FF><font color=red>�m�[�U���_���T�[</font><img src=\"$imgurl/kon1.gif\"></td></tr><tr>
<td bgcolor=#FF69B4>Fairy Bridge</td>
</tr><tr>
<td rowspan=2 bgcolor=#FF69B4>Sun Princess</td>
<td bgcolor=#1E90FF>�C���O���b�V���v�����X</td></tr><tr>
<td bgcolor=#FF69B4>Sunny Valley</td>
</tr>
</table><br><br>
�@�E�@���n�͈��ތ�<b>$taneosu</b>���ȏ�Ŏ퉲�n�ɂȂ��B<BR><BR>
�@�E�@��O�Ƃ��Č������r�₦���ꍇ���̔N�̍ł����т̗ǂ��������n�͎퉲�n�ɂȂ��B<BR><BR>
�@�E�@�Ĕn�͈��ތ�<b>$tanemesu</b>���ȏ�ŔɐB�Ĕn�ɂȂ��B<BR><BR>
�@�E�@�퉲�n��<b>$osuintai</b>�΂Ŏ퉲�n�����ނ����B<BR><BR>
�@�E�@�ɐB�Ĕn��<b>$mesuintai</b>�΂ŔɐB�Ĕn�����ނ����B<BR><BR>
�@�E�@�V�[�Y���D���n�͎��̃V�[�Y���̎n�߂ɊM����܂ɒ���ł����B<BR><BR>
�@�E�@�M����܂ɏ��Ɨ��D���n�́���̐F���ς���B<br><br>
</td></tr></table>

_HTML_
&chosaku;
}

##### �\��
sub nouhan{

        if   ($supi >= 37){$s = "��";}
        elsif($supi >= 35){$s = "��";}
        elsif($supi >= 30){$s = "��";}
        elsif($supi > 26){$s = "��";}
        else            {$s = "�~";}

        if   ($syun >= 37){$ss = "��";}
        elsif($syun >= 35){$ss = "��";}
        elsif($syun >= 30){$ss = "��";}
        elsif($syun > 26){$ss = "��";}
        else            {$ss = "�~";}

        if   ($kisei >= 37){$sss = "��";}
        elsif($kisei >= 35){$sss = "��";}
        elsif($kisei >= 30){$sss = "��";}
        elsif($kisei > 26){$sss = "��";}
        else            {$sss = "�~";}

        if   ($st > 38){$ssss = "������";}
        elsif($st > 36){$ssss = "��������";}
        elsif($st > 34){$ssss = "������";}
        elsif($st > 32){$ssss = "�Z������";}
        else            {$ssss = "�Z����";}

        if   ($formkon >= 20){$sssss = "��";}
        elsif($formkon >= 17){$sssss = "��";}
        elsif($formkon >= 15){$sssss = "��";}
        elsif($formkon >= 13){$sssss = "��";}
        else            {$sssss = "�~";}

}# end nouhan

#####�j���[�X�ɋL�^
sub shinkiro{

# ���Ԃ̎擾
	
	$times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);
        $year += 1900;
	$month = sprintf("%02d",$mon +1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$ljikan = "$month/$mday $hour:$min";

        open(CO,"$commentfile");
	seek(CO,0,0);  @nyusu = <CO>;  close(CO);

      $kekka = "";
      $flag=0;
      if($shiki == 1){

             $shinnbunn = "$winp[0]����$winp[1]���̉�����B���I";}

      elsif($shiki == 2){
             ($nameosu, $tokusyu) = split(/<mm>/,$winz[0]);
             $shinnbunn = "$nameosu�̎Y�$winz[1]���̉�����B���I";}

      elsif($shiki == 3){
             ($namemesu, $tokusyu) = split(/<mm>/,$winzm[0]);
             $shinnbunn = "$namemesu�̎e��$winzm[1]���̉�����B���I";}

      elsif($shiki == 4){

             $shinnbunn = "���т̃T���u���b�g���a���B���O��$formumaname�Ɩ������ꂽ�B";}

      elsif($shiki == 5){

           $shinnbunn = "���ԌI�т̃T���u���b�g���a���B���O��$formumaname�Ɩ������ꂽ�B";}
      
      elsif($shiki == 6){

             $shinnbunn = "$lname[$k]���X�n�g���ň����I";
             $kekka = "$lname[$k] ��-�X�n�g-�� $lname[$kk]";}
      elsif($shiki == 7){

        $shinnbunn = "��$endrigu���$endname�y$endman�z��$endwin��$endmake�s�ŗD���I";}

      elsif($shiki == 8){

       $shinnbunn = "$lname[$j]�̘A����$rennsyou[$j]�ŃX�g�b�v�B�~�߂��̂�$lname[$i]�I";}

	$kakiko = "$shinnbunn<>127.0.0.1<>$news<>$ljikan<>$kekka<>\n";

        foreach $line (@nyusu) {
        ($comm, $host, $name, $time, $kekka) = split(/<>/,$line);
        if($comm eq $shinnbunn){$flag=1;last;}
        }

    if($flag ne "1"){
	unshift(@nyusu, $kakiko);
	splice(@nyusu, $max_com);
    }

        open(CO,">$commentfile") ;
               eval 'flock(CO,2);';
	       seek(CO,0,0);	print CO @nyusu;
	       eval 'flock(CO,8);';
        close(CO);
}

##### �G���[�̎��̏���
sub error{
if($wawa ne "1"){
print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��
}
       $err_msg = @_[0];
         
print <<"_ERROR_";

<html><head><title>ERROR</title></head>
$body
<br><br><br><center>$err_msg
<BR></body></html>
<center><form action="$cgifile" method="$method">
<input type="submit" value="�߂�">
_ERROR_

exit;

}#END error

sub secretcopyright{
$secret = qq|<!--���̃X�N���v�g�̒m�I���L���̓�kou�ƃS�[�h���ɂ���܂��B-->|;
print $secret;
} #END
