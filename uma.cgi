#! /usr/local/bin/perl

#----------------------------------------------------------------------
#	 ���ڂ����o�g�����C���� ver 1.17 (Free)
#	 �����	: Alpha-kou.(b-ban2)
#	 E-MAIL	: dabo@dabo.design.co.jp
#	 URL	: http://D-BR.net/
#
#        ������	: �S�[�h��
#        E-MAIL	: zaza99jp@yahoo.co.jp
#	 URL	: http://godon.bbzone.net/
#
# �g�p�O�ɂ܂����p�K���ǂ�ł�������
#	http://D-BR.net/kitei.html
#       http://howaitoman.hp.infoseek.co.jp/kitei.html
# [���̃X�N���v�g���g�p���ċN���������Ȃ鑹�Q�ɂ��ӔC�͕����܂���B]
#----------------------------------------------------------------------

$| = 1;
require './jcode.pl';

########## ���[�J���ϐ��w��
sub kankyou{

# �N�b�L�[���擾
        &get_cookie;

#��{�ݒ�

	$cgifile = './uma.cgi';	# ���̃t�@�C����
	$logfile = './chara.dat';	# �L�����o�^�t�@�C��
	$timefile = './time.dat';	# ���ԋL�^�t�@�C��
	$rankfile = './rank.dat';	# �����L���O�t�@�C��
	$fightfile = './fightlog.dat';	# �O�̎����̋L�^�t�@�C��
        $commentfile	= './comment.dat';	# �R�����g�t�@�C��
        $cntfile = './count.dat';       # �J�E���^�t�@�C��
        $orfile = './orank.dat';	# �I�[�i�[�����L���O�t�@�C��

	$method = 'POST';	# GET or POST���w��
	$max_chara = '30';	# �ΐ�҂��L�����̍ő吔
	$max_fight = '6';	# �킢�̋L�^�̍ő吔
	$max_rank = '20';	# �����L���O�̍ő吔

	$acomment = '<font color=ffffff>���ˋ��n�o�g���Q�͋����n��o�^���ăQ�[���ł��B<br>
�S�`�[���ȏ�W�܂�����ő�P���ԂɂR�񃌁[�X�������ōs���܂��B<br>
�Ȃ��A�d���o�^�⓯���i�n���E�n�喼�j�ł̓o�^�͏o���܂���B<br>
���݂�25���[�X�Ŏ����I�Ɉ��ނ��܂��B</font>';
# �^�C�g�����̃R�����g�i�^�O�\�j
	$url = 'boc-keiba.mints.ne.jp';	# �߂��t�q�k

	$nameleng = '9' ;	# ���O�̒�����S�p�������܂łɂ��邩�B

# �y�[�W�S�́i�ϐ��̖��O��body�^�O���̂܂܂ł��B�j

	$bgcolor = '#2E8B57';	# default:#2E8B57
	$text = 'ffffff';	# default:ffffff
	$link = '0000CD';	# default:0000CD
	$vlink = '6699FF';	# default:6699FF
	$alink = '303030';	# default:303030
        $comcolor = '#2E8B57';  #�R�����g�̔w�i�F
	$background = '';	# �w�i�摜�i��΃p�X�j

	$ysize = 600;		# �����i�𑜓x���Ⴂ�l�̂��߂ɁA�o���邾��600�ɂ��Ă��������B�j

# �^�C�g��
        $title = '���ˋ��n�o�g��';	# �^�C�g��
	$title2 = '���ˋ��n�o�g��';	# �u���E�U�ɕ\�������^�C�g��
	$tcolor = '#FF4500';	# �^�C�g���̐F(default:#FF4500)
	$tsize = '6';		# �^�C�g���T�C�Y(default:6)
        $bbs_name  = '';			# �f���̖��O
	$bbs_url  = '';           # �f���̂t�q�k

# �A�C�R���t�H���_�p�X
        $imgurl  ="http://127.0.0.1/uma/icon/";   # �e���t�@���_�̐�΃p�X


# �Q�[���o�����X���ݒ�
        $battle = '10';            # �P���Ԃɉ����[�X���i20=�P���Ԃ�3��@10=�P���Ԃ�6��j
        $intai = '25';             # �����[�X�ň��ނ����邩
        $max_com = '10';            # �R�����g�̍ő吔
        $max_zi ='35';             #�R�����g�̍ő厚��


# �\������

	$iroformwaku = '#6699FF';# �t�H�[���{�^������̐F(default:#6699FF)
	$ccolor = '#FF0000';	# �ΐ펞�̃L�����̐F
	$mestop = '�g�b�v�y�[�W';
	$mesrec = '�����n�̓o�^';
	$mesrank = '���n�����L���O';
	$meshome = '�z�[���y�[�W';
	$mesrule = '�ށ[ѐ���';

# �ΐ�҂����X�g�̍��ڂ̖��O
	$tableno = 'NO';	        # �ԍ�
	$tablenam = '�n��';     	# ���O
	$tableaut = '�n��';	        # ���
	$tablelif = '�̋�������';	# �̗�
	$tablepow = '�X�s�[�h';  	# �U����
	$tabledef = '�u����';   	# �h���
	$tablespe = '�C��';     	# ���΂₳
	$tabledat = '�o�^����'; 	# �o�^����


### �A�C�R��

	@icon1 = ('uma1','uma2','uma3','uma4','uma5');	  # 'uma1'�̂悤�ɁA�t�@�C�������L�����Ă��������B.gif�͂���܂���B
	@icon2 = ('�ȌI��','������','����','����','��');	# '�ȌI��'�̂悤�ɁA�\�������镶�����L�����Ă��������B


# �~�j�J�E���^�̐ݒu
# �� 0=no 1=�e�L�X�g 
$counter = 1;

########## �ݒ肱���܂�

#### �A�C�R�����X�g�̎擾

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

# �ΐ폈��
         if(int($min/$battle) ne $times[0] && $lines[3]){require './uma_race.cgi';&syori;}
# �o�^����
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
	$value =~ s/;/�G/g;
	$value =~ s/�@//g;
	$value =~ s/ //g;
	$form{$key} = $value;

	}

}#end decode

##### ���O�ǂݍ���
sub readlog{
	open(DB,"$logfile");
	seek(DB,0,0);  @lines = <DB>;  close(DB);
	
	($lno, $lname, $lsakusya, $lhomepage, $llif, $lpow, $ldef, $lspe, $ldate, $lip, $licon, $lwin, $lsyu, $ltotal, $ltyoushi, $lashi, $lname2, $lpow2, $ldef2, $lspe2, $licon2, $ltyoushi2, $lashi2, $lname3, $lpow3, $ldef3, $lspe3, $licon3, $ltyoushi3, $lashi3, $ltname,) = split(/<>/,$lines[0]);

	open(TM,"$timefile");
	seek(TM,0,0);  @times = <TM>;  close(TM);

# ���Ԃ̎擾
	
	$times =time;
	($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime($times);


# ���ԃt�@�C������̎��͂����ŏo��

	if($times[0] eq ""){
	$times[0] = int($min/$battle);
	open(TM,">$timefile") ;
		eval 'flock(TM,2);';
		seek(TM,0,0);	print TM @times;
		eval 'flock(TM,8);';
	close(TM);
	}

}#end


##### �n�o�^����

sub record{

if($lines[${max_chara}-1]){&error(0);}

# �ϐ���u��������
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

# �\�͒l�`�F�b�N
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

# ���O�̒����`�F�b�N
	if((length($formchara) < 1)||(length($formchara) > $nameleng *2)){&error(3)};
        if((length($formchara2) < 1)||(length($formchara2) > $nameleng *2)){&error(3)};
        if((length($formchara3) < 1)||(length($formchara3) > $nameleng *2)){&error(3)};
	if((length($formname) < 1)||(length($formname) > $nameleng *2)){&error(3)};
        if((length($formtname) < 1)||(length($formtname) > $nameleng *2)){&error(3)};
	($formhp =~ /^http:\/\/[a-zA-Z0-9]+/) || ($formhp = '');	#�g�o�̔���

        open(DB,"$logfile");    # �i�n���E�n��j�̏d���`�F�b�N
        seek(DB,0,0);@lines = <DB>; close(DB);   
        foreach $lines (@lines){
($lno, $lname, $lsakusya, $lhomepage, $llif, $lpow, $ldef, $lspe, $ldate, $lip, $licon, $lwin, $lsyu, $ltotal, $ltyoushi, $lashi, $lname2, $lpow2, $ldef2, $lspe2, $licon2, $ltyoushi2, $lashi2, $lname3, $lpow3, $ldef3, $lspe3, $licon3, $ltyoushi3, $lashi3, $ltname,) = split(/<>/,$lines);
      if($lname eq $formchara){&error(5)}
      if($lname eq $formchara2){&error(5)}
      if($lname eq $formchara3){&error(5)}
      elsif($lsakusya eq $formname){&error(5)}
       $lines = "$lno<>$lname<>$lsakusya<>$lhomepage<>$llif<>$lpow<>$ldef<>$lspe<>$ldate<>$lip<>$licon<>$lwin<>$lsyu<>$ltotal<>$ltyoushi<>$lashi<>$lname2<>$lpow2<>$ldef2<>$lspe2<>$licon2<>$ltyoushi2<>$lashi2<>$lname3<>$lpow3<>$ldef3<>$lspe3<>$licon3<>$ltyoushi3<>$lashi3<>$ltname<>\n";}

# �����[�g�z�X�g�擾
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};
        for ($i=0; $i<$#lines+1; $i++){
	@checkip = split(/<>/,$lines[$i]);
#       if($host eq $checkip[9]){&error(4);}
        }

# �o�^�i���o�[

	open(DBTMP,"$logfile");    #chara.dat
	seek(DBTMP,0,0);  @linestmp = <DBTMP>;  close(DBTMP);
	foreach $i (0..(@linestmp-1)) {
	@Buftmp = split('<>', @linestmp[$i]);
	$SDatatmp{$i} = $Buftmp[0];
	}

	@SortDatatmp = sort {($SDatatmp{$b} <=> $SDatatmp{$a}) || ($b cmp $a)} keys(%SDatatmp);

	$lno = $linestmp[$SortDatatmp[0]] +1;

# �o�^����
	$year += 1900;
	$month = sprintf("%02d",$mon +1);
	$mday = sprintf("%02d",$mday);
	$hour = sprintf("%02d",$hour);
	$min = sprintf("%02d",$min);
	$sec = sprintf("%02d",$sec);
	$jikan = "$month/$mday $hour:$min:$sec";

# �N�b�L�[�𔭍s
        &set_cookie;

# ���O�֏������ރX�^�C���̐��`
	$kakiko = "$lno<>$formchara<>$formname<>$formhp<>400<>$formpow<>$formdef<>$formspe<>$jikan<>$host<>$formicon<>0<>$formsyu<>0<>5<>$formashi<>$formchara2<>$formpow2<>$formdef2<>$formspe2<>$formicon2<>5<>$formashi2<>$formchara3<>$formpow3<>$formdef3<>$formspe3<>$formicon3<>5<>$formashi3<>$formtname<>\n";

# ���O�ւ̏�������
	open(DB,">>$logfile") ;
		eval 'flock(DB,2);';
		print DB $kakiko;
		eval 'flock(DB,8);';
	close(DB);
push(@lines,$kakiko);

open(OR,"+<$orfile") || &error('�w�肳�ꂽ�t�@�C�����J���܂���B');
	eval 'flock(OR,2);';

@oranks = <OR>;
                $oranka = "$formname<>0<>\n";
         foreach $check (@oranks){
		@check = split(/<>/,$check);
		if($formname eq $check[0]){$flag=1;last;}
		}
                if($flag ne "1"){push(@oranks,$oranka);}


# �I�[�i�[���O�ւ̏�������
	truncate (OR, 0); 
	seek(OR,0,0);	print OR @oranks;
	close(OR);
	eval 'flock(OR,8);';

# �L�^�������邵

$recflag = '1';

}#end record

##### �R�����g�L������
sub comsyori{

         # �����[�g�z�X�g�擾
	$host = $ENV{'REMOTE_HOST'} || $ENV{'REMOTE_ADDR'};
	if(length($form{'comtext'}) < 1 || length($form{'comtext'}) > $max_zi * 2){&error(6)}
	open(CF,"+<$commentfile") || &error('�w�肳�ꂽ�t�@�C�����J���܂���B');
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


#####���쌠�\��

sub chosaku{
&secretcopyright;
print <<"_CHOSAKU_";

<hr size="1" color=ffffff>
<div align="right"><a href="http://godon.bbzone.net/" target=_blank><font size="2"><font color=ffffff>���ˋ��n�o�g��ver1.10(Free)</font></a></div></font>
<div align="right"><a href="http://sweet.oc.to/" target=_blank><font size="2"><font color=ffffff>�n�摜���^�@�F�@\"Without Dreams(����)"</font></a></div>
<div align="right"><a href="http://www3.to/uma-zura" target=_blank><font size="2"><font color=ffffff>�R��摜�@�F�@"um@-zura"</font></a></div></font>
<div align="right"><a href="http://D-BR.net/" target=_blank><font size="2"><font color=ffffff>�I���W�i����/���ڂ����o�g�����C����ver1.17(Free)</font></a></div>
<!--�L���o�i�[�}���ʒu�A�y�[�W����-->
</body>
</html>
_CHOSAKU_

}#end chosaku


##### �o��
sub html{

if ($title){$acomment = "<BR><BR>$acomment";}

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<!--�L���o�i�[�}���ʒu�A�y�[�W�㕔-->
<center><font color="$tcolor" size="$tsize">$title</font>$acomment<P>
<a href=$bbs_url target=_blank><font color=ffffff>$bbs_name</a></font>
<html>

<DIV align="center"><TABLE width="800" cellpadding="0" cellspacing="10"><TBODY><tr><td valign="top"><CENTER><table border=1 width=220>
_HTML1_

	open(FG,"$fightfile");
	seek(FG,0,0);  @fg = <FG>;  close(FG);
       
        print "<td valign=top bgcolor=$iroformwaku><center><font color=000000><B>���[�X�̋L�^</B></font></center></td>\n";
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
<center><input type="submit" name="rec" value="�����n�̓o�^">
<input type="submit" name="rule" value="�ށ[ѐ���">
<center><input type="submit" name="rank" value="���n�`�[�������L���O">
<input type="submit" name="orank" value="�L�͂Ȑ��Y��">
<form action="$cgifile" method="$method">
<input type="button" value="ΰ���߰��" onClick="top.location.href='$url'">
</td></tr></table>
</form>

_HTML2_
if($counter){
           &counter;
           }
print <<"_HTML1_";

<TD align="center" valign="top" rowspan="1">
<table border="1" width=580 cellpadding="0"><tr><td bgcolor=$iroformwaku><center><font color=000000><B>$tableno</td><td bgcolor=$iroformwaku><center><font color=000000><B>$tablenam</td><td bgcolor=$iroformwaku><center><font color=000000><B>�r���E���q</td><td bgcolor=$iroformwaku><center><font color=000000><B>�R��</td><td bgcolor=$iroformwaku><center><font color=000000><B>$tableaut</td><td bgcolor=$iroformwaku><center><font color=000000><B>�`�[�����E����</td></tr>

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
	print "<tr><td><center>$no</td><td><center>$name<br>$name2<br>$name3<br></td><td><center><img src=\"$imgurl/$sakusen\"><img src=\"$imgurl/$cond\"><br><img src=\"$imgurl/$sakusen2\"><img src=\"$imgurl/$cond2\"><br><img src=\"$imgurl/$sakusen3\"><img src=\"$imgurl/$cond3\"></td><td><center>$icon_pri2</td><td><center>$sakusya</td><td><center><font color=gold><B>$tname</B></font><br><font color=#00FFFF>$total��o���F<B>$win��</B>$lose�s</td></tr>\n";

}else
{print "<tr><td><center>$no</td><td><center>$name<br>$name2<br>$name3<br></td><td><center><img src=\"$imgurl/$sakusen\"><img src=\"$imgurl/$cond\"><br><img src=\"$imgurl/$sakusen2\"><img src=\"$imgurl/$cond2\"><br><img src=\"$imgurl/$sakusen3\"><img src=\"$imgurl/$cond3\"></td><td><center>$icon_pri2</td><td><center>$sakusya</td><td><center><font color=gold><B>$tname</B></font><br><font color=#7FFFD4>$total��o���F0��$lose�s</td></tr>\n";}
}

print <<"_HTML2_";
</table>
</TBODY> 
</TABLE>
</DIV><HR size=1 color=ffffff>
</center>
<form action="$cgifile" method="$method">
<center>�R�����g
<input type=text name=comtext size=75>
<input type=hidden name=comment value=1>
<input type=submit name=comment value="��������">
</form>
<center>
_HTML2_

open(CF,"$commentfile") || &error('�w�肳�ꂽ�t�@�C�����J���܂���B');
	seek(CF,0,0);  @comments = <CF>;  close(CF);

	print "<br><table border=1 width=\"660\" cellpadding=5 cellspacing=0>\n";
	print "<tr align=\"center\"><td>�R�����g</td></tr>\n";
	print "<tr><td bgcolor=\"$comcolor\">\n";

	$i = 0;
	foreach(@comments){
		($com) = split /<>/;
		print "�� �F�w $com �x \n";

		if($i ne $#comments){ print "<hr width=\"100%\" size=1>\n"; }
		$i++;
	}
	print "</table><br>\n";

&chosaku;

}#end html


##### �n�o�^�o��

sub rec{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��
print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body

<center><font color="$tcolor" size="$tsize">$mesrec</font>

_HTML1_

if($recflag){
print <<"_HTML3_";
<P>
�o�^�������܂����B
</P>
_HTML3_

} else {

        open(LL,"$logfile");
	seek(LL,0,0);  @kazu = <LL>;  close(LL);
        
        if($#kazu+2 > $max_chara){
        print "<br><br>���ݍő�o�^���ɒB���Ă���̂œo�^�o���܂���B<BR><BR>";
              }else{

print <<"_HTML3_";

<P>
<table border="1" width="$ysize" cellpadding="5"><tr><td>
<form action="$cgifile" method="$method">
<table width="100%" border="1"><tr><td>
<center>����</td><td><center>�n���i$nameleng�����܂Łj</td><td><center>�ѐF</td><td><center>�r��</td><td><center>�X�s�[�h<br><b>10�`70</b></td><td><center>�u����<br><b>10�`70</b></td><td><center>�C��<br><b>10�`70</b></td></tr><tr><td>
<font size="2">
<center>�P������<br><center>�i100�j</td><td>
<center><input type="text" name="chara" size="16"></td><td>
<center><select name="icon">@iconlist</select></td><td>
<center><select name="ashi">
<option value="1">����
<option value="2">��s
<option value="3">����
<option value="4">�Ǎ�
</select></td><td>
<center><input type="text" name="power" value="$c_power" size="3"></td><td>
<center><input type="text" name="defence" value="$c_def" size="3"></td><td>
<center><input type="text" name="speed" value="$c_spe" size="3"></td></tr><tr><td>
<font size="2"><center>�Q������<br><center>�i100�j</td><td>
<center><input type="text" name="chara2" size="16"></td><td>
<center><select name="icon2">@iconlist</select></td><td>
<center><select name="ashi2">
<option value="1">����
<option value="2">��s
<option value="3">����
<option value="4">�Ǎ�
</select></td><td>
<center><input type="text" name="power2" value="$c_power2" size="3"></td><td>
<center><input type="text" name="defence2" value="$c_def2" size="3"></td><td>
<center><input type="text" name="speed2" value="$c_spe2" size="3"></td></tr><tr><td>
<font size="2"><center>�R������<br><center>�i200�j</td><td>
<center><input type="text" name="chara3" size="16"></td><td>
<center><select name="icon3">@iconlist</select></td><td>
<center><select name="ashi3">
<option value="1">����
<option value="2">��s
<option value="3">����
<option value="4">�Ǎ�
</select></td><td>
<center><input type="text" name="power3" value="$c_power3" size="3"></td><td>
<center><input type="text" name="defence3" value="$c_def3" size="3"></td><td>
<center><input type="text" name="speed3" value="$c_spe3" size="3"></td></tr><tr><td colspan="7">
<select name="syu">
<option value="kisyu1.gif">���@�L
<option value="kisyu2.gif">�́@��
<option value="kisyu3.gif">��@��
<option value="kisyu4.gif">�l�@��
<option value="kisyu5.gif">傁@��
<option value="kisyu6.gif">�p�@�c
<option value="kisyu7.gif">���@��
<option value="kisyu8.gif">���@�R
<option value="kisyu9.gif">�ā@�c
<option value="kisyu10.gif">�y�@���@�G
<option value="kisyu11.gif">���@�c
<option value="kisyu12.gif">���@�K
<option value="kisyu13.gif">���@��
</select>�F�R��A�C�R�� <br>
<input type="text" name="tname" size="16">�F�`�[���̖��O�i�S�p$nameleng�����܂Łj<br>
<input type="text" name="name" value="$c_name" size="16">�F���Ȃ��̖��O�i�S�p$nameleng�����܂Łj<br>
<input type="text" name="hp" value="$c_hp" size="50">�F�z�[���y�[�W(��\��\)<BR></td></tr><tr><td colspan="7">
<li>�e�n�̃X�s�[�h�E�u���́E�C���̍��v��100�ɂȂ�悤�ɂ�<br>
<li>�R��A�C�R����\�\\�͂ɉe�����Ȃ���B<br>
<center><input type="submit" value="�o�^">
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


##### �����L���O�o��
sub rank{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<center><font color='white' size=6>���n�`�[�������L���O</font><P>

<table border="1" width="$ysize">

<tr><td bgcolor=$iroformwaku><center><font color=000000><B>����</td><td bgcolor=$iroformwaku><center><font color=000000><B>�`�[����</td><td bgcolor=$iroformwaku><center><font color=000000><B>�n��</td><td bgcolor=$iroformwaku><center><font color=000000><B>�R��</td><td bgcolor=$iroformwaku><center><font color=000000><B>$tableaut</td></tr>

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
	print "<tr><td><center><B><font color=ffffff size=$ookisa>$div$win��</font>$div2</B></td><td><center><B>$tname</B></td><td><center>$name<br>$name2<br>$name3</td><td><center>$icon_pri2</td><td><center>$sakusya</td></tr>";
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


##### �L�͂Ȑ��Y�Əo��
sub orank{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>�L�͂Ȑ��Y��</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<STYLE TYPE="text/css">
<!--
body,tr,td,th	{ font-size: 10pt }
.score		{ font-size: 10pt;}
body,table{cursor:url(http://howaitoman.hp.infoseek.co.jp/a.cur);}
-->
</style>
<center><br><font color=white size=5><B>�L�͂Ȑ��Y��(�g�b�v�Q�O)</B></font><P>

<table border="1" width="400">

<tr><td bgcolor=#87CEFA><center><font color=000000><B>����</td><td bgcolor=#87CEFA><center><font color=000000><B>���O</td><td bgcolor=#87CEFA><center><font color=000000><B>�����N</td></tr>

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

          if($win[$i] > 699){$syou[$i] = "���E�n���Y�E�̐_";}
          elsif($win[$i] > 499){$syou[$i] = "��Í��n�E�̉�";}
          elsif($win[$i] > 399){$syou[$i] = "���{�n�E�̉�";}
          elsif($win[$i] > 299){$syou[$i] = "���{�n�E�̋~����";}
          elsif($win[$i] > 399){$syou[$i] = "�n���Y�E�̃g�b�v";}
          elsif($win[$i] > 99){$syou[$i] = "�n���Y�Ƌ�";}
          elsif($win[$i] > 74){$syou[$i] = "�n���Y�l";}
          elsif($win[$i] == 77){$syou[$i] = "(߄t�)�ϰ";}
          elsif($win[$i] > 49){$syou[$i] = "���n��i�E�́E�j��!";}
          elsif($win[$i] > 24){$syou[$i] = "�i�E�́E�j��!�n���Y��";}
          elsif($win[$i] > 14){$syou[$i] = "�����Ɣn�𐶎Y����";}
          elsif($win[$i] > 9){$syou[$i] = "�n�D��";}
          elsif($win[$i] > 4){$syou[$i] = "�n�l";}
          else{$syou[$i] = "��ʐl";}
            
           
	print "<tr><td><center><B><font color='white' size=$ookisa[$i]>$win[$i]��</font></B></td><td><center>$sakusya[$i]</td><td><center>$syou[$i]</td></tr>";
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
		print "$cnt�l�̊ϐ��<br>\n";
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

        $cookies="name\<>$formname\,hp\<>$formhp\,power\<>$formpow\,power2\<>$formpow2\,power3\<>$formpow3\,def\<>$formdef\,def2\<>$formdef2\,def3\<>$formdef3\,spe\<>$formspe\,spe2\<>$formspe2\,spe3\<>$formspe3";
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


##### �O�̎����̋L�^
sub log{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML1_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<center><font color="$tcolor" size="$tsize">�킢�̋L�^�ꗗ</font>

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

##### �킢�̋�̓I�ȋL�^
sub fight{

	open(FG,"$fightfile");
	seek(FG,0,0);  @fg = <FG>;  close(FG);

	$no = $form{'no'};
	$no--;
	
	($time , $tname , $fight) = split(/<>/,$fg[$no]);


print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

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

##### ���[������
sub rule{

print "Content-type: text/html\n\n";#�R���e���g�^�C�v�o��

print <<"_HTML_";
<html><head><title>$title2</title><META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=x-sjis"></head>
$body
<center><font color="$tcolor" size="$tsize">�����т���</font>

<hr size="1">

<table border="1" width="$ysize" cellpadding="5"><tr><td>
<font size="2">
�����т���<BR><BR>
�@�E�@���̃Q�[���͔n��o�^���ėV�΂���Q�[������B<BR><BR>
�@�E�@�e�n�ɂP�O�O�|�C���g�̔\\�͒l��U�蕪���Ă����ĂˁB<BR><BR>
�@�E�@�e�\\�͒l�͂P�O�`�V�O�̊Ԃɂ��ĂˁB<BR><BR>
�@�E�@�n���S���ȏ�o�^����A��莞�ԂɂȂ�ƃ��[�X���s�����B<BR><BR>
�@�E�@�P���Ԃɍő�R���[�X�s�����B<BR><BR>
�@�E�@�n�̏����̃����L���O�������B<BR><BR>
�@�E�@���Y�҂̏����̃����L���O�������B<BR><BR>
�@�E�@�X�s�[�h�͂�͂�ŏd�v�I���[�X�ɂ����ď�Ƀ|�C���g�ƂȂ�B<br><br>
�@�E�@�u���͍͂Ō�̃X�p�[�g�ɓ��鎞�ɑ�؂ɂȂ��B<br><br>
�@�E�@�C���͈�������Ɣn���v���悤�ɑ���Ȃ���B<br><br>
�@�E�@���q�͏������n���������n���ω������B<br><br>
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

##########�G���[���b�Z�[�W

###�G���[�̎��̏����B
sub error {

local($no) = @_;

$msg[0] = '����ȏ�o�^�ł��Ȃ���B�f���Œm�点�Ă����Γo�^�ő吔�𑝂₵�܂��B';
$msg[1] = '�\�͒l���P�O�`�V�O�ɂȂ��ĂȂ���B';
$msg[2] = '�e�n�̔\�͒l�̃g�[�^�����P�O�O�ɂȂ��ĂȂ���B';
$msg[3] = "���O�̒�����$nameleng�����ȉ��ɂ��ĂˁB";
$msg[4] = "�d���o�^�s�I";
$msg[5] = "���̔n���A���͔n�喼�͂��łɎg���Ă��܂��B";
$msg[6] = "�����͂R�T���܂łł��B";
$msg[7] = "���łɓ����������݂�����܂��B";
print "Content-type: text/html\n\n";
print <<"_ERROR_";
<html><head><title>ERROR</title></head>
$body
$msg[$no]<BR>
<form action="$cgifile" method="$method">
<input type="submit" value="�߂�">
</form>
</body>
</html>
_ERROR_
exit;
}#END error

sub secretcopyright{
$secret = qq|<!--���̃X�N���v�g�̒m�I���L����b-ban2���ƃS�[�h���ɂ���܂��B-->|;
print $secret;
} #END
